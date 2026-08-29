from fastapi import APIRouter, Depends

from app.models.user import User

from app.core.jwt import get_current_user

from app.schemas.ai_schema import (
    TravelGenerateRequest,
    TravelGenerateResponse,
)
from app.services.ai_service import generate_travel_plan

router = APIRouter(prefix="/api/ai", tags=["AI"])#所有接口自动带 /api/ai
# 这一整个文件都是 AI 模块的路由。
# 以后 /chat、/optimize-route 都会放这里。

@router.post("/generate", response_model=TravelGenerateResponse)#返回内容格式校验

def generate_plan(
    request: TravelGenerateRequest,
    current_user:User=Depends(get_current_user)   #depends的作用是依赖注入，自动获取当前用户
):
    print(
        "当前用户:",
        current_user.username
    )

    result = generate_travel_plan(
        destination=request.destination,
        days=request.days,
        budget=request.budget,
        people=request.people,
        preferences=request.preferences,
    )

    return TravelGenerateResponse(result=result)