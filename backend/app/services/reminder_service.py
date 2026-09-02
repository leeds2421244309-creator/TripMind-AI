"""
Reminder Service

基于 Todo.deadline 查询：
- today: 今天到期的未完成 Todo
- week: 未来 7 天内到期的未完成 Todo
- overdue: 已过期但未完成的 Todo

不接短信、不接定时任务，纯查询。
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.enums.todo_status import TodoStatus
from app.models.travel_todo import TravelTodo


# ==========================
# 今日提醒
# ==========================
def get_today_todos(db: Session):
    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)

    return (
        db.query(TravelTodo)
        .filter(
            TravelTodo.deadline.isnot(None),
            TravelTodo.deadline >= start,
            TravelTodo.deadline < end,
            TravelTodo.status != TodoStatus.DONE,
        )
        .order_by(TravelTodo.deadline.asc())
        .all()
    )


# ==========================
# 本周提醒（未来 7 天）
# ==========================
def get_week_todos(db: Session):
    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)

    return (
        db.query(TravelTodo)
        .filter(
            TravelTodo.deadline.isnot(None),
            TravelTodo.deadline >= start,
            TravelTodo.deadline < end,
            TravelTodo.status != TodoStatus.DONE,
        )
        .order_by(TravelTodo.deadline.asc())
        .all()
    )


# ==========================
# 逾期提醒
# ==========================
def get_overdue_todos(db: Session):
    now = datetime.utcnow()

    return (
        db.query(TravelTodo)
        .filter(
            TravelTodo.deadline.isnot(None),
            TravelTodo.deadline < now,
            TravelTodo.status != TodoStatus.DONE,
        )
        .order_by(TravelTodo.deadline.asc())
        .all()
    )
