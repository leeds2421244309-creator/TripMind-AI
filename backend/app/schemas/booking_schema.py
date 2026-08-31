from datetime import datetime

from pydantic import BaseModel, Field

from app.enums.booking_type import BookingType
from app.enums.payment_status import PaymentStatus


# ===== 创建订单 =====
class BookingCreateRequest(BaseModel):
    booking_type: BookingType = Field(..., description="订单类型")

    name: str = Field(..., description="酒店名称、餐厅名称、航班号等")

    address: str | None = Field(
        default=None,
        description="地址（可为空）"
    )

    phone: str | None = Field(
        default=None,
        description="联系电话（酒店可填写）"
    )

    start_time: datetime | None = Field(
        default=None,
        description="入住/预约/出发时间"
    )

    end_time: datetime | None = Field(
        default=None,
        description="退房/结束/到达时间"
    )

    price: int | None = Field(
        default=None,
        ge=0,
        description="订单金额"
    )

    notes: str | None = Field(
        default=None,
        description="备注"
    )


# ===== 更新支付状态 =====
class BookingStatusUpdateRequest(BaseModel):
    payment_status: PaymentStatus


# ===== 返回订单 =====
class BookingResponse(BaseModel):
    id: int
    travel_id: int

    booking_type: BookingType

    name: str
    address: str | None
    phone: str | None

    start_time: datetime | None
    end_time: datetime | None

    price: int | None

    payment_status: PaymentStatus

    image_url: str | None

    notes: str | None

    created_at: datetime

    class Config:
        from_attributes = True


# ================= 更新订单 =================
class BookingUpdateRequest(BaseModel):

    name: str | None = None
    address: str | None = None
    phone: str | None = None

    start_time: datetime | None = None
    end_time: datetime | None = None

    price: int | None = Field(default=None, ge=0)

    payment_status: PaymentStatus | None = None

    notes: str | None = None


# ================= 订单列表 =================
class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]