from fastapi import APIRouter

from app.clients.amap_client import search_poi

from app.schemas.map_schema import POIResponse

router = APIRouter(
    prefix="/api/map",
    tags=["Map"]
)


@router.get(
    "/poi",
    response_model=POIResponse)
def poi_search(keyword:str):

    result = search_poi(keyword)

    return result