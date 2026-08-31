from fastapi import APIRouter, File, UploadFile

from app.schemas.ocr_schema import OCRBookingResponse
from app.services.ocr_service import parse_booking_image

router = APIRouter(
    prefix="/api/ocr",
    tags=["OCR"]
)


@router.post(
    "/booking",
    response_model=OCRBookingResponse,
    summary="识别酒店/餐厅/交通订单截图"
)
async def booking_ocr(file: UploadFile = File(...)):
    """
    上传订单截图，返回 AI 识别信息。
    """

    # 后面这里会读取图片内容发送给 AI。
    return parse_booking_image()