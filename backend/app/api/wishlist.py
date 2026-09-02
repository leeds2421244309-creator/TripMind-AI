from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.wishlist_schema import (
    WishlistCreateRequest,
    WishlistListResponse,
    WishlistResponse,
    WishlistUpdateRequest,
)

from app.services.wishlist_service import (
    create_wishlist,
    delete_wishlist,
    get_wishlist,
    get_wishlist_list,
    update_wishlist,
)

router = APIRouter(
    prefix="/api",
    tags=["Travel Wishlist"],
)


# 创建心愿单
@router.post(
    "/travel/{travel_id}/wishlist",
    response_model=WishlistResponse,
)
def create_new_wishlist(
    travel_id: int,
    request: WishlistCreateRequest,
    db: Session = Depends(get_db),
):
    return create_wishlist(db, travel_id, request)


# 获取所有心愿单
@router.get(
    "/travel/{travel_id}/wishlist",
    response_model=WishlistListResponse,
)
def read_wishlist_list(
    travel_id: int,
    db: Session = Depends(get_db),
):
    wishlists = get_wishlist_list(db, travel_id)

    return {"wishlists": wishlists}


# 修改心愿单
@router.patch(
    "/wishlist/{wishlist_id}",
    response_model=WishlistResponse,
)
def edit_wishlist(
    wishlist_id: int,
    request: WishlistUpdateRequest,
    db: Session = Depends(get_db),
):
    wishlist = update_wishlist(db, wishlist_id, request)

    if wishlist is None:
        raise HTTPException(
            status_code=404,
            detail="Wishlist not found"
        )

    return wishlist


# 删除心愿单
@router.delete("/wishlist/{wishlist_id}")
def remove_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
):
    success = delete_wishlist(db, wishlist_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Wishlist not found"
        )

    return {"message": "Wishlist deleted successfully"}
