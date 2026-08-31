from sqlalchemy.orm import Session

from app.models.travel import Travel
from app.schemas.travel_schema import TravelCreateRequest


def create_travel(
    db: Session,
    user_id: int,
    request: TravelCreateRequest,
):
    travel = Travel(
        user_id=user_id,
        title=request.title,
        origin=request.origin,
        destination=request.destination,
        goal=request.goal,
        start_date=request.start_date,
        end_date=request.end_date,
        people_count=request.people_count,
        # total_budget=request.total_budget,
        # preferences=request.preferences,
        # long_transport_preference=request.long_transport_preference,
        # local_transport_preference=request.local_transport_preference,
        # notes=request.notes,
        total_budget=0,
        currency="CNY",
        budget_mode=False,
    )

    db.add(travel)
    db.commit()
    db.refresh(travel)

    return travel

# 获取当前用户所有旅行
def get_user_travels(
    db: Session,
    user_id: int,
):
    travels = (
        db.query(Travel)
        .filter(Travel.user_id == user_id)
        .order_by(Travel.start_date.desc())
        .all()
    )

    return travels

# 获取单个旅行详情
def get_travel_detail(
    db: Session,
    user_id: int,
    travel_id: int,
):
    travel = (
        db.query(Travel)
        .filter(
            Travel.id == travel_id,
            Travel.user_id == user_id,
        )
        .first()
    )

    return travel