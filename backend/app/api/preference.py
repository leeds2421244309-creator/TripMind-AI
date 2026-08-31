from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.preference_schema import (
    PreferenceResponse,
    PreferenceUpdateRequest,
)

from app.services.preference_service import (
    get_preference,
    update_preference,
)

router = APIRouter(
    prefix="/api/travel",
    tags=["Travel Preference"]
)


@router.patch(
    "/{travel_id}/preference",
    response_model=PreferenceResponse,
    summary="保存吃住行偏好"
)
def save_preference(
    travel_id: int,
    request: PreferenceUpdateRequest,
    db: Session = Depends(get_db)
):
    return update_preference(db, travel_id, request)


@router.get(
    "/{travel_id}/preference",
    response_model=PreferenceResponse,
    summary="获取吃住行偏好"
)
def read_preference(
    travel_id: int,
    db: Session = Depends(get_db)
):
    preference = get_preference(db, travel_id)

    if preference is None:
        raise HTTPException(
            status_code=404,
            detail="Preference not found"
        )

    return preference