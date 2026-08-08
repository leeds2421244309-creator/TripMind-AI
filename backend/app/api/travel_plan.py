from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.travel_plan import TravelPlan

from typing import List

from app.schemas.travel_plan import (
    TravelPlanResponse,
    TravelPlanCreate,
    TravelPlanUpdate
)

router = APIRouter(
    prefix="/api/v1/travel-plans",
    tags=["Travel Plans"]
)


@router.get(
    "/",
    response_model=List[TravelPlanResponse]
)

def get_travel_plans(
    db: Session = Depends(get_db)

# Depends(get_db)
# 请求来了
# ↓
# 调用 get_db()
# ↓
# 拿数据库连接
# ↓
# 执行接口
# ↓
# 关闭连接

):

    plans = db.query(
        TravelPlan  # 等价于SELECT *FROM travel_plans;
    ).all()



    return plans

@router.get(
    "/{plan_id}",
    response_model=TravelPlanResponse
)
def get_travel_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):

    plan = db.query(
        TravelPlan
    ).filter(
        TravelPlan.id == plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="旅行计划不存在"
        )

    return plan


@router.post(
    "/",
    response_model=TravelPlanResponse
)
def create_travel_plan(
    plan: TravelPlanCreate,
    db: Session = Depends(get_db)
):

    new_plan = TravelPlan(

    user_id=1,

    title=plan.title,

    destination=plan.destination,

    start_date=plan.start_date,

    days=plan.days,

    budget=plan.budget,

    people_count=plan.people_count,

    interests=plan.interests,

    transportation=plan.transportation

)

    db.add(new_plan)

    db.commit()

    db.refresh(new_plan)


    return new_plan

@router.put(
    "/{plan_id}",
    response_model=TravelPlanResponse
)
def update_travel_plan(
    plan_id: int,
    plan: TravelPlanUpdate,
    db: Session = Depends(get_db)
):

    db_plan = db.query(
        TravelPlan
    ).filter(
        TravelPlan.id == plan_id
    ).first()


    if not db_plan:
        raise HTTPException(
            status_code=404,
            detail="旅行计划不存在"
        )


    db_plan.title = plan.title
    db_plan.destination = plan.destination
    db_plan.start_date = plan.start_date
    db_plan.days = plan.days
    db_plan.budget = plan.budget
    db_plan.people_count = plan.people_count
    db_plan.interests = plan.interests
    db_plan.transportation = plan.transportation


    db.commit()

    db.refresh(db_plan)


    return db_plan

@router.delete(
    "/{plan_id}"
)
def delete_travel_plan(
    plan_id: int,
    db: Session = Depends(get_db)
):

    plan = db.query(
        TravelPlan
    ).filter(
        TravelPlan.id == plan_id
    ).first()


    if not plan:
        raise HTTPException(
            status_code=404,
            detail="旅行计划不存在"
        )


    db.delete(plan)

    db.commit()


    return {
        "message": "删除成功"
    }