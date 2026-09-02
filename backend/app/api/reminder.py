from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.reminder_schema import ReminderListResponse
from app.services.reminder_service import (
    get_overdue_todos,
    get_today_todos,
    get_week_todos,
)

router = APIRouter(
    prefix="/api/reminder",
    tags=["Reminder"],
)


# 今日提醒
@router.get(
    "/today",
    response_model=ReminderListResponse,
)
def read_today_reminders(
    db: Session = Depends(get_db),
):
    todos = get_today_todos(db)
    return {"reminders": todos}


# 本周提醒（未来 7 天）
@router.get(
    "/week",
    response_model=ReminderListResponse,
)
def read_week_reminders(
    db: Session = Depends(get_db),
):
    todos = get_week_todos(db)
    return {"reminders": todos}


# 逾期提醒
@router.get(
    "/overdue",
    response_model=ReminderListResponse,
)
def read_overdue_reminders(
    db: Session = Depends(get_db),
):
    todos = get_overdue_todos(db)
    return {"reminders": todos}
