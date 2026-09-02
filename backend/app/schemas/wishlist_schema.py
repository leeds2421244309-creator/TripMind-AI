from datetime import datetime

from pydantic import BaseModel, Field


# ===== 创建心愿单 =====
class WishlistCreateRequest(BaseModel):

    name: str = Field(..., description="地点名称")

    address: str | None = Field(
        default=None,
        description="地址（可为空）"
    )

    latitude: float | None = Field(
        default=None,
        description="纬度"
    )

    longitude: float | None = Field(
        default=None,
        description="经度"
    )

    category: str = Field(
        ...,
        description="分类：景点、餐厅、购物等"
    )

    notes: str | None = Field(
        default=None,
        description="备注"
    )

    is_must_visit: bool = Field(
        default=False,
        description="是否必去"
    )


# ===== 更新心愿单 =====
class WishlistUpdateRequest(BaseModel):

    name: str | None = None

    address: str | None = None

    latitude: float | None = None

    longitude: float | None = None

    category: str | None = None

    notes: str | None = None

    is_must_visit: bool | None = None


# ===== 返回心愿单 =====
class WishlistResponse(BaseModel):

    id: int
    travel_id: int

    name: str
    address: str | None

    latitude: float | None
    longitude: float | None

    category: str
    notes: str | None

    is_must_visit: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ===== 心愿单列表 =====
class WishlistListResponse(BaseModel):
    wishlists: list[WishlistResponse]
