from datetime import datetime, date

from pydantic import BaseModel

# 公共字段
class TravelPlanBase(BaseModel):

    title: str

    destination: str

    start_date: date

    days: int

    budget: float

    people_count: int

    interests: str | None = None

    transportation: str | None = None


# 创建旅行计划
class TravelPlanCreate(TravelPlanBase):
    pass

# 更新旅行计划
class TravelPlanUpdate(BaseModel):

    title: str

    destination: str

    start_date: date

    days: int

    budget: float

    people_count: int

    interests: str | None = None

    transportation: str | None = None



# 返回旅行计划
class TravelPlanResponse(TravelPlanBase):

    id: int

    user_id: int

    created_at: datetime
    updated_at: datetime


    class Config:
        from_attributes = True
        # 作用：
        # 允许：
        # SQLAlchemy对象
        # ↓
        # Pydantic对象
        # 转换。

        # 没有它：
        # SQLAlchemy：
        # TravelPlan(
        # id=1
        # title="东京"
        # )

        # Pydantic：

        # 不认识。