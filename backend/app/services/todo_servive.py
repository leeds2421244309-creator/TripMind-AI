from sqlalchemy.orm import Session

from app.enums.todo_source import TodoSource
from app.enums.todo_status import TodoStatus
from app.models.travel_todo import TravelTodo
from app.schemas.todo_schema import (
    TodoCreateRequest,
    TodoUpdateRequest,
)


# ================= 创建 Todo =================
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


# ================= 获取旅行全部 Todo =================
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


# ================= 获取单个 Todo =================
def get_todo(
    db: Session,
    todo_id: int,
):
    return (
        db.query(TravelTodo)
        .filter(TravelTodo.id == todo_id)
        .first()
    )


# ================= 更新 Todo =================
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


# ================= 删除 Todo =================
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