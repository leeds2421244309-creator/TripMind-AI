from datetime import datetime

from pydantic import BaseModel, Field

from app.enums.todo_status import TodoStatus
from app.enums.todo_source import TodoSource


# ================= 创建 Todo（用户新增） =================
class TodoCreateRequest(BaseModel):

    title: str = Field(..., description="待办标题")

    description: str | None = Field(
        default=None,
        description="待办备注"
    )

    day_number: int = Field(
        default=0,
        ge=0,
        description="所属旅行天数（Day0、Day1、Day2...）"
    )

    deadline: datetime | None = Field(
        default=None,
        description="提醒时间"
    )


# ================= 修改 Todo =================
class TodoUpdateRequest(BaseModel):

    title: str | None = None

    description: str | None = None

    day_number: int | None = Field(
        default=None,
        ge=0
    )

    deadline: datetime | None = None

    status: TodoStatus | None = None

    sort_order: int | None = None


# ================= 返回 Todo =================
class TodoResponse(BaseModel):

    id: int

    travel_id: int

    title: str

    description: str | None

    day_number: int

    deadline: datetime | None

    status: TodoStatus

    source: TodoSource

    sort_order: int

    class Config:
        from_attributes = True


# ================= Todo 列表 =================
class TodoListResponse(BaseModel):

    todos: list[TodoResponse]