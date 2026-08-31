from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.budget_item import BudgetItem
from app.models.travel import Travel

from app.schemas.budget_schema import (
    BudgetItemCreateRequest,
    BudgetItemUpdateRequest,
    BudgetItemResponse,
    BudgetSummaryResponse,
)

from app.services.budget_service import (
    calculate_item_cost,
    calculate_budget_summary,
)

from app.schemas.budget_schema import BudgetInsightResponse

from app.services.budget_service import (
    generate_budget_insight,
)

router = APIRouter(
    prefix="/api/budget",
    tags=["Budget Engine"]
)

#新增预算
@router.post(
    "/{travel_id}",
    response_model=BudgetItemResponse
)
def create_budget_item(
    travel_id: int,
    request: BudgetItemCreateRequest,
    db: Session = Depends(get_db)
):
    travel = db.query(Travel).filter(
        Travel.id == travel_id
    ).first()

    if not travel:
        raise HTTPException(
            status_code=404,
            detail="旅行不存在"
        )

    estimated_cost = calculate_item_cost(
        request.unit_cost,
        request.quantity,
    )

    item = BudgetItem(
        travel_id=travel_id,
        budget_type=request.budget_type,
        category=request.category,
        title=request.title,
        unit_cost=request.unit_cost,
        quantity=request.quantity,
        estimated_cost=estimated_cost,
        payment_status=request.payment_status,
        notes=request.notes,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item

#查询预算
@router.get(
    "/{travel_id}",
    response_model=list[BudgetItemResponse]
)
def get_budget_items(
    travel_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(BudgetItem)
        .filter(BudgetItem.travel_id == travel_id)
        .all()
    )

#修改预算
@router.patch(
    "/item/{item_id}",
    response_model=BudgetItemResponse
)
def update_budget_item(
    item_id: int,
    request: BudgetItemUpdateRequest,
    db: Session = Depends(get_db)
):
    item = db.query(BudgetItem).filter(
        BudgetItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="预算项不存在"
        )

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    # 自动重新计算金额
    item.estimated_cost = calculate_item_cost(
        item.unit_cost,
        item.quantity,
    )

    db.commit()
    db.refresh(item)

    return item



#删除预算项
@router.delete("/item/{item_id}")
def delete_budget_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(BudgetItem).filter(
        BudgetItem.id == item_id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="预算项不存在"
        )

    db.delete(item)
    db.commit()

    return {
        "message":"删除成功"
    }


#预算卡
@router.get(
    "/summary/{travel_id}",
    response_model=BudgetSummaryResponse
)
def get_budget_summary(
    travel_id: int,
    db: Session = Depends(get_db)
):
    travel = db.query(Travel).filter(
        Travel.id == travel_id
    ).first()

    if not travel:
        raise HTTPException(
            status_code=404,
            detail="旅行不存在"
        )

    budget_items = (
        db.query(BudgetItem)
        .filter(BudgetItem.travel_id == travel_id)
        .all()
    )

    summary = calculate_budget_summary(
        travel,
        budget_items,
    )

    return summary


#预算提醒
@router.get(
    "/insight/{travel_id}",
    response_model=BudgetInsightResponse
)
def get_budget_insight(
    travel_id: int,
    db: Session = Depends(get_db)
):
    travel = db.query(Travel).filter(
        Travel.id == travel_id
    ).first()

    if not travel:
        raise HTTPException(
            status_code=404,
            detail="旅行不存在"
        )

    budget_items = (
        db.query(BudgetItem)
        .filter(BudgetItem.travel_id == travel_id)
        .all()
    )

    summary = calculate_budget_summary(
        travel,
        budget_items,
    )

    return generate_budget_insight(summary)