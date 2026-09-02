from pydantic import BaseModel

from app.schemas.booking_schema import BookingResponse
from app.schemas.budget_schema import BudgetSummaryResponse
from app.schemas.preference_schema import PreferenceResponse
from app.schemas.travel_schema import TravelResponse
from app.schemas.wishlist_schema import WishlistResponse


# Decision Center 聚合响应
class DecisionCenterResponse(BaseModel):

    travel: TravelResponse

    budget_summary: BudgetSummaryResponse

    preference: PreferenceResponse | None

    bookings: list[BookingResponse]

    wishlist: list[WishlistResponse]
