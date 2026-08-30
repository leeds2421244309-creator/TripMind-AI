from fastapi import APIRouter

from app.clients.amap_client import search_poi

from app.services.map_service import get_route_summary

from app.schemas.transport_schema import RouteResponse
from app.schemas.transport_schema import RouteRequest
from app.schemas.map_schema import POIResponse

router = APIRouter(
    prefix="/api/map",
    tags=["Map"]
)



@router.post(
    "/route",
    response_model=RouteResponse
)
def get_route(
    request: RouteRequest
):
    """
    查询两个地点之间路线信息
    """

    origin_poi = search_poi(request.origin)
    destination_poi = search_poi(request.destination)
    # ##
    # print(origin_poi)
    # print(destination_poi)
    # ##
    return get_route_summary(
        origin_name=origin_poi["name"],
        origin_location=origin_poi["location"],
        destination_name=destination_poi["name"],
        destination_location=destination_poi["location"],
        city=request.city,
    )