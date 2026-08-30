from pydantic import BaseModel, Field


class TransportInfo(BaseModel):
    duration: str = Field(..., description="预计耗时（分钟）")
    distance_km: float = Field(..., description="路线距离（公里）")
    cost: float | None = Field(default=None, description="预计费用")
    

class RouteResponse(BaseModel):
    origin: str = Field(..., description="起点名称")
    destination: str = Field(..., description="终点名称")

    straight_distance_km: float = Field(..., description="直线距离（公里）")

    driving: TransportInfo = Field(..., description="驾车路线")
    transit: TransportInfo = Field(..., description="公交/地铁路线")
    walking: TransportInfo = Field(..., description="步行路线")

    recommendation: str | None = None

    amap_url: str = Field(..., description="打开高德导航链接")

class RouteRequest(BaseModel):
    origin: str = Field(..., description="起点名称")
    destination: str = Field(..., description="终点名称")
    city: str = Field(..., description="所在城市")