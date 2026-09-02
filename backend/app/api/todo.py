from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.todo_schema import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoListResponse,
)

from app.services.todo_service import (
    create_todo,
    get_todo_list,
    update_todo,
    delete_todo,
    generate_todos_from_bookings,
)

router = APIRouter(
    prefix="/api",
    tags=["Travel Todo"],
)


# ================= 创建 Todo =================
@router.post(
    "/travel/{travel_id}/todo",
    response_model=TodoResponse,
)
def create_new_todo(
    travel_id: int,
    request: TodoCreateRequest,
    db: Session = Depends(get_db),
):
    return create_todo(db, travel_id, request)


# ================= 获取 Todo 列表 =================
@router.get(
    "/travel/{travel_id}/todo",
    response_model=TodoListResponse,
)
def read_todo_list(
    travel_id: int,
    db: Session = Depends(get_db),
):
    todos = get_todo_list(db, travel_id)
    return {"todos": todos}


# ================= 修改 Todo =================
@router.patch(
    "/todo/{todo_id}",
    response_model=TodoResponse,
)
def edit_todo(
    todo_id: int,
    request: TodoUpdateRequest,
    db: Session = Depends(get_db),
):
    todo = update_todo(db, todo_id, request)

    if todo is None:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
        )

    return todo


# ================= 删除 Todo =================
@router.delete("/todo/{todo_id}")
def remove_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    success = delete_todo(db, todo_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Todo not found",
        )

    return {"message": "Todo deleted successfully"}


# ================= 根据 Booking 自动生成 Todo（规则版） =================
@router.post(
    "/travel/{travel_id}/todo/generate",
    response_model=TodoListResponse,
)
def generate_todos(
    travel_id: int,
    db: Session = Depends(get_db),
):
    """
    规则版 Todo Generator：
    遍历该旅行下所有 Booking，按订单类型自动生成 Todo。
    酒店 → Check-in + Check-out
    飞机 → 提前2小时到机场
    高铁/火车 → 提前30分钟到站
    演唱会/其他 → 提前30分钟入场
    """
    todos = generate_todos_from_bookings(db, travel_id)

    return {"todos": todos}
