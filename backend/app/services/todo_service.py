"""
Travel Todo Service

包含：
1. 基础 CRUD（用户手动管理 Todo）
2. Rule Engine 驱动的 Todo Generator
   - 聚合 visa / transport / destination / budget / schedule / packing / safety 规则
   - 同时保留 booking 维度的 day-of 提醒（酒店入住/退房、餐厅预约等）
   - 不接 AI，纯 Python 规则
"""

from datetime import timedelta

from sqlalchemy.orm import Session

from app.enums.booking_type import BookingType
from app.enums.todo_source import TodoSource
from app.enums.todo_status import TodoStatus
from app.models.travel_booking import TravelBooking
from app.models.travel_todo import TravelTodo
from app.rules.travel_rules import build_context, generate_rule_todos
from app.schemas.todo_schema import (
    TodoCreateRequest,
    TodoUpdateRequest,
)


# ==========================
# 创建 Todo（用户新增）
# ==========================
def create_todo(
    db: Session,
    travel_id: int,
    request: TodoCreateRequest,
):
    todo = TravelTodo(
        travel_id=travel_id,
        title=request.title,
        description=request.description,
        day_number=request.day_number,
        deadline=request.deadline,
        status=TodoStatus.TODO,
        source=TodoSource.USER,
        sort_order=0,
    )

    db.add(todo)
    db.commit()
    db.refresh(todo)

    return todo


# ==========================
# 获取旅行全部 Todo
# ==========================
def get_todo_list(
    db: Session,
    travel_id: int,
):
    return (
        db.query(TravelTodo)
        .filter(TravelTodo.travel_id == travel_id)
        .order_by(
            TravelTodo.day_number.asc(),
            TravelTodo.sort_order.asc(),
            TravelTodo.deadline.asc(),
        )
        .all()
    )


# ==========================
# 获取单个 Todo
# ==========================
def get_todo(
    db: Session,
    todo_id: int,
):
    return (
        db.query(TravelTodo)
        .filter(TravelTodo.id == todo_id)
        .first()
    )


# ==========================
# 更新 Todo
# ==========================
def update_todo(
    db: Session,
    todo_id: int,
    request: TodoUpdateRequest,
):
    todo = get_todo(db, todo_id)

    if todo is None:
        return None

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    db.refresh(todo)

    return todo


# ==========================
# 删除 Todo
# ==========================
def delete_todo(
    db: Session,
    todo_id: int,
):
    todo = get_todo(db, todo_id)

    if todo is None:
        return False

    db.delete(todo)
    db.commit()

    return True


# ============================================================
# Rule Engine Todo Generator
# 不接 AI，纯 Python 规则
# ============================================================

# 演唱会 / 其他活动：提前 30 分钟入场
_EVENT_LEAD_MINUTES = 30

# 优先级 → sort_order 基数
_PRIORITY_OFFSET = {
    "high": 0,
    "medium": 100,
    "low": 200,
}


def _build_booking_todos(booking: TravelBooking) -> list[dict]:
    """
    根据 booking 类型生成 day-of Todo 模板。

    注意：FLIGHT / TRAIN / BUS / FERRY 的提前到达提醒
    已由 transport_rules 生成，此处不重复。
    """
    templates: list[dict] = []
    start = booking.start_time
    end = booking.end_time

    if booking.booking_type == BookingType.HOTEL:
        templates.append({
            "title": f"酒店办理入住 - {booking.name}",
            "description": (
                f"入住时间 {start.strftime('%m-%d %H:%M') if start else ''}；"
                f"地址：{booking.address or '未填写'}"
            ),
            "deadline": start,
            "day_number": 0,
            "category": "hotel",
            "priority": "medium",
        })
        templates.append({
            "title": f"酒店退房 - {booking.name}",
            "description": "请确认物品齐全，办理退房",
            "deadline": end,
            "day_number": 0,
            "category": "hotel",
            "priority": "medium",
        })

    elif booking.booking_type == BookingType.RESTAURANT:
        templates.append({
            "title": f"餐厅预约 - {booking.name}",
            "description": f"预约时间 {start.strftime('%m-%d %H:%M') if start else ''}",
            "deadline": start,
            "day_number": 0,
            "category": "booking",
            "priority": "low",
        })

    else:
        # 演唱会 / 大巴 / 轮渡 / 其他：提前 30 分钟入场
        # 注意：FLIGHT/TRAIN 已由 transport_rules 处理，不会走到这里
        templates.append({
            "title": f"{booking.name} - 提前30分钟入场",
            "description": "建议提前 30 分钟到达场馆/集合点",
            "deadline": start - timedelta(minutes=_EVENT_LEAD_MINUTES) if start else None,
            "day_number": 0,
            "category": "booking",
            "priority": "low",
        })

    return templates


# ==========================
# 批量生成 Todo（Rule Engine + booking 维度）
# ==========================
def generate_todos_from_bookings(
    db: Session,
    travel_id: int,
):
    """
    生成旅行 Todo，两步聚合：
    1. Rule Engine：visa / transport / destination / budget / schedule / packing / safety
    2. booking 维度：酒店入住退房、餐厅预约等 day-of 提醒
    """
    # 1. 构建上下文
    ctx = build_context(db, travel_id)

    if ctx is None:
        return []

    # 2. 运行 Rule Engine
    rule_todos = generate_rule_todos(ctx)

    # 3. booking 维度 day-of 提醒
    booking_todos: list[dict] = []
    for booking in ctx.bookings:
        booking_todos.extend(_build_booking_todos(booking))

    # 4. 合并所有 Todo 模板
    all_templates = rule_todos + booking_todos

    # 5. 计算排序：按优先级分段，段内按顺序递增
    counters: dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    created_todos: list[TravelTodo] = []

    for template in all_templates:
        priority = template.get("priority", "medium")
        offset = _PRIORITY_OFFSET.get(priority, 100)
        sort_order = offset + counters.get(priority, 0)
        counters[priority] = counters.get(priority, 0) + 1

        todo = TravelTodo(
            travel_id=travel_id,
            title=template["title"],
            description=template.get("description"),
            day_number=template.get("day_number", 0),
            deadline=template.get("deadline"),
            status=TodoStatus.TODO,
            source=TodoSource.RULE,
            sort_order=sort_order,
        )
        db.add(todo)
        created_todos.append(todo)

    db.commit()

    for todo in created_todos:
        db.refresh(todo)

    return created_todos
