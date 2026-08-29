from pydantic import BaseModel, Field


class POIResponse(BaseModel):
    """
    TripMind统一地点数据结构
    """

    name: str = Field(
        ...,
        description="地点名称"
    )

    address: str = Field(
        ...,
        description="地点地址"
    )

    longitude: float = Field(
        ...,
        description="经度"
    )

    latitude: float = Field(
        ...,
        description="纬度"
    )