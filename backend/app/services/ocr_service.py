from app.schemas.ocr_schema import OCRBookingResponse


def parse_booking_image() -> OCRBookingResponse:
    """
    临时模拟 OCR 返回。
    Day16 先跑通接口，下一步替换成 AI Vision。
    """

    return OCRBookingResponse(
        booking_type="hotel",
        name="Holiday Inn Golden Mile Hong Kong",
        address="50 Nathan Road, Tsim Sha Tsui",
        phone="+85223151000",
        price=880,
        ocr_text="""
Holiday Inn Golden Mile Hong Kong
Check-in: 2026-09-01 15:00
Check-out: 2026-09-03 12:00
Breakfast Included
Breakfast Time: 07:00-10:30
""",
        ai_summary="""
{
    "breakfast": true,
    "breakfast_time": "07:00-10:30",
    "luggage_storage": true
}
"""
    )