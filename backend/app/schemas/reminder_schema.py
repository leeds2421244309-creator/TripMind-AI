from pydantic import BaseModel

from app.schemas.todo_schema import TodoResponse


# Reminder 列表响应（Reminder 本质是按 deadline 过滤后的 Todo）
class ReminderListResponse(BaseModel):
    reminders: list[TodoResponse]
