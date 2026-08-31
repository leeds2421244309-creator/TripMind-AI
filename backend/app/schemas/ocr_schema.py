from datetime import datetime

from pydantic import BaseModel


class OCRBookingResponse(BaseModel):
    booking_type: str

    # AI识别出的基础信息
    name: str | None = None
    address: str | None = None
    phone: str | None = None

    start_time: datetime | None = None
    end_time: datetime | None = None

    price: int | None = None

    # OCR原始文字
    ocr_text: str

    # AI提取出的更多细节(JSON字符串)
    ai_summary: str | None = None