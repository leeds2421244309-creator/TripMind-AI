from sqlalchemy.orm import Session

from app.models.budget_item import BudgetItem
from app.models.travel import Travel
from app.services.booking_service import get_booking_list
from app.services.budget_service import calculate_budget_summary
from app.services.preference_service import get_preference
from app.services.wishlist_service import get_wishlist_list


# 聚合 Decision Center 数据
def get_decision_center(
    db: Session,
    travel_id: int,
):
    travel = db.query(Travel).filter(
        Travel.id == travel_id
    ).first()

    if travel is None:
        return None

    # 复用已有 Service，不复制 SQL
    budget_items = (
        db.query(BudgetItem)
        .filter(BudgetItem.travel_id == travel_id)
        .all()
    )

    budget_summary = calculate_budget_summary(travel, budget_items)
    bookings = get_booking_list(db, travel_id)
    preference = get_preference(db, travel_id)
    wishlist = get_wishlist_list(db, travel_id)

    return {
        "travel": travel,
        "budget_summary": budget_summary,
        "preference": preference,
        "bookings": bookings,
        "wishlist": wishlist,
    }
