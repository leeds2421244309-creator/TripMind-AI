from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.booking_schema import (
    BookingCreateRequest,
    BookingListResponse,
    BookingResponse,
    BookingUpdateRequest,
)

from app.services.booking_service import (
    create_booking,
    delete_booking,
    get_booking,
    get_booking_list,
    update_booking,
)

router = APIRouter(
    prefix="/api",
    tags=["Travel Booking"]
)


# 创建订单
@router.post(
    "/travel/{travel_id}/booking",
    response_model=BookingResponse,
)
def create_new_booking(
    travel_id: int,
    request: BookingCreateRequest,
    db: Session = Depends(get_db),
):
    return create_booking(db, travel_id, request)


# 获取所有订单
@router.get(
    "/travel/{travel_id}/booking",
    response_model=BookingListResponse,
)
def read_booking_list(
    travel_id: int,
    db: Session = Depends(get_db),
):
    bookings = get_booking_list(db, travel_id)

    return {"bookings": bookings}


# 修改订单
@router.patch(
    "/booking/{booking_id}",
    response_model=BookingResponse,
)
def edit_booking(
    booking_id: int,
    request: BookingUpdateRequest,
    db: Session = Depends(get_db),
):
    booking = update_booking(db, booking_id, request)

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


# 删除订单
@router.delete("/booking/{booking_id}")
def remove_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):
    success = delete_booking(db, booking_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return {"message": "Booking deleted successfully"}