from sqlalchemy.orm import Session

from app.enums.payment_status import PaymentStatus
from app.models.travel_booking import TravelBooking
from app.schemas.booking_schema import (
    BookingCreateRequest,
    BookingUpdateRequest,
)


# 创建订单
def create_booking(
    db: Session,
    travel_id: int,
    request: BookingCreateRequest,
):
    booking = TravelBooking(
        travel_id=travel_id,

        booking_type=request.booking_type,

        name=request.name,
        address=request.address,
        phone=request.phone,

        start_time=request.start_time,
        end_time=request.end_time,

        price=request.price,

        payment_status=PaymentStatus.UNDECIDED,

        notes=request.notes,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


# 查询订单列表
def get_booking_list(
    db: Session,
    travel_id: int,
):
    return db.query(TravelBooking).filter(
        TravelBooking.travel_id == travel_id
    ).all()


# 查询单个订单
def get_booking(
    db: Session,
    booking_id: int,
):
    return db.query(TravelBooking).filter(
        TravelBooking.id == booking_id
    ).first()


# 更新订单
def update_booking(
    db: Session,
    booking_id: int,
    request: BookingUpdateRequest,
):
    booking = get_booking(db, booking_id)

    if booking is None:
        return None

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(booking, key, value)

    db.commit()
    db.refresh(booking)

    return booking


# 删除订单
def delete_booking(
    db: Session,
    booking_id: int,
):
    booking = get_booking(db, booking_id)

    if booking is None:
        return False

    db.delete(booking)
    db.commit()

    return True