from pydantic import BaseModel, Field


# 单条风险
class RiskItem(BaseModel):

    type: str = Field(..., description="风险类型：time_conflict / location_conflict / budget_conflict")

    level: str = Field(..., description="风险等级：high / medium / low")

    message: str = Field(..., description="风险描述")

    suggestion: str = Field(..., description="处理建议")


# 风险检查响应
class RiskCheckResponse(BaseModel):
    risks: list[RiskItem]
