from sqlalchemy.orm import Session

from app.models.travel_preference import TravelPreference
from app.schemas.preference_schema import PreferenceUpdateRequest


def update_preference(
    db: Session,
    travel_id: int,
    request: PreferenceUpdateRequest
):
    preference = db.query(TravelPreference).filter(
        TravelPreference.travel_id == travel_id
    ).first()

    # 第一次填写
    if preference is None:
        preference = TravelPreference(
            travel_id=travel_id
        )
        db.add(preference)

    # 更新字段
    preference.hotel_budget_per_night = request.hotel_budget_per_night
    preference.hotel_prompt = request.hotel_prompt

    preference.food_budget_per_meal = request.food_budget_per_meal
    preference.food_prompt = request.food_prompt

    preference.transport_prompt = request.transport_prompt
    preference.local_transport_prompt = request.local_transport_prompt

    db.commit()
    db.refresh(preference)

    return preference


def get_preference(
    db: Session,
    travel_id: int
):
    return db.query(TravelPreference).filter(
        TravelPreference.travel_id == travel_id
    ).first()