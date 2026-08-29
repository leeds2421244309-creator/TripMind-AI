from pydantic import BaseModel, Field


class TravelGenerateRequest(BaseModel):

    destination: str = Field(
        ...,#必须填写
        description="旅行目的地"
    )

    days: int = Field(
        ...,
        ge=1,
        le=30,
        description="旅行天数"
    )

    budget: int = Field(
        ...,
        ge=0,
        description="预算"
    )

    people: int = Field(
        ...,
        ge=1,
        description="人数"
    )

    preferences: list[str] = Field(
        default_factory=list,
        description="旅行偏好"
    )


# AI旅行计划返回

class TravelGenerateResponse(BaseModel):

    status: str = Field(
        ...,
        description="success 或 conflict"
    )

    plan: dict | None = Field(
        default=None,
        description="旅行计划"
    )

    reason: str | None = Field(
        default=None,
        description="冲突原因"
    )

    suggestions: list[str] | None = Field(
        default=None,
        description="调整建议"
    )



# AI问答请求

class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        description="用户旅行问题"
    )



# AI问答返回

class ChatResponse(BaseModel):

    answer: str = Field(
        ...,
        description="AI回答内容"
    )