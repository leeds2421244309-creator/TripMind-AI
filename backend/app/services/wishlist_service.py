from sqlalchemy.orm import Session

from app.models.travel_wishlist import TravelWishlist
from app.schemas.wishlist_schema import (
    WishlistCreateRequest,
    WishlistUpdateRequest,
)


# 创建心愿单
def create_wishlist(
    db: Session,
    travel_id: int,
    request: WishlistCreateRequest,
):
    wishlist = TravelWishlist(
        travel_id=travel_id,

        name=request.name,
        address=request.address,

        latitude=request.latitude,
        longitude=request.longitude,

        category=request.category,
        notes=request.notes,
        is_must_visit=request.is_must_visit,
    )

    db.add(wishlist)
    db.commit()
    db.refresh(wishlist)

    return wishlist


# 查询心愿单列表
def get_wishlist_list(
    db: Session,
    travel_id: int,
):
    return db.query(TravelWishlist).filter(
        TravelWishlist.travel_id == travel_id
    ).all()


# 查询单个心愿单
def get_wishlist(
    db: Session,
    wishlist_id: int,
):
    return db.query(TravelWishlist).filter(
        TravelWishlist.id == wishlist_id
    ).first()


# 更新心愿单
def update_wishlist(
    db: Session,
    wishlist_id: int,
    request: WishlistUpdateRequest,
):
    wishlist = get_wishlist(db, wishlist_id)

    if wishlist is None:
        return None

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(wishlist, key, value)

    db.commit()
    db.refresh(wishlist)

    return wishlist


# 删除心愿单
def delete_wishlist(
    db: Session,
    wishlist_id: int,
):
    wishlist = get_wishlist(db, wishlist_id)

    if wishlist is None:
        return False

    db.delete(wishlist)
    db.commit()

    return True
