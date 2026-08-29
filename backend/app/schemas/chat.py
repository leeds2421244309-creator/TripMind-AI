from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        ...,#表示必填
        description="用户问题"
    )


class ChatResponse(BaseModel):
    answer: str = Field(
        ...,
        description="AI回答"
    )