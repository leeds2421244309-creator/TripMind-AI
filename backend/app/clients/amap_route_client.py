import requests

from app.core.config import settings

BASE_URL = "https://restapi.amap.com/v3/direction"


def request_route(api: str, origin: str, destination: str, extra_params=None):
    """
    请求高德路线接口
    """

    params = {
        "key": settings.AMAP_API_KEY,
        "origin": origin,
        "destination": destination,
        "output": "json",
    }

    if extra_params:
        params.update(extra_params)

    response = requests.get(f"{BASE_URL}/{api}", params=params)
    data = response.json()

    if data.get("status") != "1":
        raise Exception(data.get("info"))

    return data


def get_driving_route(origin: str, destination: str):
    return request_route("driving", origin, destination)

def get_walking_route(origin: str, destination: str):
    return request_route("walking", origin, destination)

def get_transit_route(origin: str, destination: str, city: str):
    return request_route(
        "transit/integrated",
        origin,
        destination,
        {
            "city": city,
            "cityd": city,
            "strategy": 0
        }
    )