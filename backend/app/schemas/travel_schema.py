from datetime import date
from pydantic import BaseModel, Field


# 创建旅行（前端第一次填写旅行信息）
class TravelCreateRequest(BaseModel):
    title: str = Field(..., description="旅行名称")

    origin: str = Field(..., description="出发地")

    destination: str = Field(..., description="目的地")

    goal: str = Field(..., description="旅行目标，例如演唱会、迪士尼、毕业旅行")

    start_date: date = Field(..., description="开始日期")

    end_date: date = Field(..., description="结束日期")

    people_count: int = Field(
        default=1,
        ge=1,
        description="出行人数"
    )

    # total_budget: int = Field(
    #     default=0,
    #     ge=0,
    #     description="总预算"
    # )

    # preferences: str | None = Field(
    #     default=None,
    #     description="旅行偏好（用户自由输入）"
    # )

    # # transport_preference: str | None = Field(
    # #     default=None,
    # #     description="交通偏好，例如公共交通、自驾、飞机"
    # # )

    # long_transport_preference: str | None = Field(
    #     default=None,
    #     description="大交通偏好：飞机、高铁、轮船、大巴、自驾、最便宜、最快"
    # )

    # local_transport_preference: str | None = Field(
    #     default=None,
    #     description="市内交通偏好：公共交通、步行优先、打车优先、自驾"
    # )

    # notes: str | None = Field(
    #     default=None,
    #     description="旅行备注"
    # )


# 返回旅行信息
class TravelResponse(BaseModel):
    id: int
    user_id: int

    title: str
    origin: str
    destination: str
    goal: str

    start_date: date
    end_date: date

    people_count: int
    total_budget: int

    # preferences: str | None = None

    # long_transport_preference: str | None = None
    # local_transport_preference: str | None = None

    # notes: str | None = None

    status: str

    class Config:
        from_attributes = True


# 旅行列表（个人中心使用）
class TravelListItem(BaseModel):
    id: int

    title: str

    destination: str

    goal: str

    start_date: date

    end_date: date

    status: str

    total_budget: int

    class Config:
        from_attributes = True


# ===== Budget 页面配置 =====

class BudgetSetupRequest(BaseModel):

    total_budget: int = Field(
        ...,
        ge=0,
        description="旅行总预算"
    )

    currency: str = Field(
        default="CNY",
        description="预算货币：CNY/HKD/KRW/JPY..."
    )

    budget_mode: bool = Field(
        default=True,
        description="是否开启预算管理"
    )