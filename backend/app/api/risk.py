from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.travel import Travel
from app.schemas.risk_schema import RiskCheckResponse
from app.services.risk_service import check_travel_risk

router = APIRouter(
    prefix="/api",
    tags=["Risk Checker"],
)


# 旅行风险检查
@router.get(
    "/travel/{travel_id}/risk-check",
    response_model=RiskCheckResponse,
)
def get_travel_risks(
    travel_id: int,
    db: Session = Depends(get_db),
):
    travel = db.query(Travel).filter(
        Travel.id == travel_id
    ).first()

    if not travel:
        raise HTTPException(
            status_code=404,
            detail="旅行不存在",
        )

    risks = check_travel_risk(db, travel_id)

    return {"risks": risks}
