from datetime import datetime

from pydantic import BaseModel, Field


# ===== 保存吃住行偏好 =====
class PreferenceUpdateRequest(BaseModel):

    # 🏨 酒店
    hotel_budget_per_night: int | None = Field(
        default=None,
        ge=0,
        description="酒店预算（每晚）"
    )

    hotel_prompt: str | None = Field(
        default=None,
        description="酒店需求描述"
    )

    # 🍜 美食
    food_budget_per_meal: int | None = Field(
        default=None,
        ge=0,
        description="每餐预算"
    )

    food_prompt: str | None = Field(
        default=None,
        description="饮食偏好描述"
    )

    # ✈️ 城市间交通
    transport_prompt: str | None = Field(
        default=None,
        description="大交通需求描述"
    )

    # 🚇 市内交通
    local_transport_prompt: str | None = Field(
        default=None,
        description="市内交通需求描述"
    )


# ===== 返回偏好 =====
class PreferenceResponse(BaseModel):

    id: int
    travel_id: int

    hotel_budget_per_night: int | None
    hotel_prompt: str | None

    food_budget_per_meal: int | None
    food_prompt: str | None

    transport_prompt: str | None
    local_transport_prompt: str | None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True