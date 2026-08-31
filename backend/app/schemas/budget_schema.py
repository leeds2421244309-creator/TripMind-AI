from pydantic import BaseModel, Field
from app.enums.payment_status import PaymentStatus

# 新增预算项
class BudgetItemCreateRequest(BaseModel):

    budget_type: str = Field(
        default="custom",
        description="default / custom"
    )

    category: str = Field(
        ...,
        description="餐饮、住宿、大交通、门票等"
    )

    title: str = Field(
        ...,
        description="预算项名称"
    )

    unit_cost: int = Field(
        default=0,
        ge=0,
        description="每天/每晚/单次预算"
    )

    quantity: int = Field(
        default=1,
        ge=1,
        description="天数、晚数、次数"
    )

    payment_status: PaymentStatus = Field(
        default=PaymentStatus.PENDING,
    )

    notes: str | None = None


# 修改预算项
class BudgetItemUpdateRequest(BaseModel):

    title: str | None = None

    unit_cost: int | None = Field(default=None, ge=0)

    quantity: int | None = Field(default=None, ge=1)

    payment_status: PaymentStatus | None = None

    notes: str | None = None


# 返回预算项
class BudgetItemResponse(BaseModel):

    id: int

    travel_id: int

    budget_type: str

    category: str

    title: str

    unit_cost: int

    quantity: int

    estimated_cost: int

    payment_status: PaymentStatus

    notes: str | None = None

    class Config:
        from_attributes = True


#计算总价
class BudgetSummaryResponse(BaseModel):

    total_budget: int

    planned_cost: int

    paid_cost: int

    pending_cost: int

    remaining_budget: int

    budget_usage: float

    status: str

class BudgetInsightResponse(BaseModel):

    category_summary: dict[str, int]

    category_percent: dict[str, float]

    largest_category: str

    remaining_budget: int

    status: str

    insights: list[str]