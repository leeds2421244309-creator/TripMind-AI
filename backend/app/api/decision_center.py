from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.decision_center_schema import DecisionCenterResponse
from app.services.decision_center_service import get_decision_center

router = APIRouter(
    prefix="/api/travel",
    tags=["Decision Center"],
)


# Decision Center 聚合接口
@router.get(
    "/{travel_id}/decision-center",
    response_model=DecisionCenterResponse,
)
def read_decision_center(
    travel_id: int,
    db: Session = Depends(get_db),
):
    """
    聚合旅行决策数据：
    travel + budget_summary + preference + bookings + wishlist
    """
    result = get_decision_center(db, travel_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="旅行不存在",
        )

    return result
