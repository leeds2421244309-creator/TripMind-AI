from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.jwt import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.travel_schema import (
    TravelCreateRequest,
    TravelResponse,
    TravelListItem,
)
from app.services.travel_service import (
    create_travel,
    get_user_travels,
    get_travel_detail
)


router = APIRouter(
    prefix="/api/travel",
    tags=["Travel"],
)

@router.get(
    "/list",
    response_model=list[TravelListItem]
)
def get_travel_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_travels(
        db=db,
        user_id=current_user.id,
    )

@router.post(
    "/create",
    response_model=TravelResponse,
)
def create_new_travel(
    request: TravelCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_travel(
        db=db,
        user_id=current_user.id,
        request=request,
    )


@router.get(
    "/{travel_id}",
    response_model=TravelResponse,
)
def get_travel_info(
    travel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    travel = get_travel_detail(
        db=db,
        user_id=current_user.id,
        travel_id=travel_id,
    )

    if travel is None:
        raise HTTPException(
            status_code=404,
            detail="旅行不存在",
        )

    return travel