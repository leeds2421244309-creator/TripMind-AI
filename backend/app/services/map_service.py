from app.clients.amap_route_client import (
    get_driving_route,
    get_transit_route,
    get_walking_route,
)

from app.schemas.transport_schema import (
    RouteResponse,
    TransportInfo,
)

from app.utils.location_utils import (
    parse_location,
    calculate_straight_distance,
)

def build_amap_navigation_url(
    origin: str,
    destination: str,
) -> str:
    """
    生成高德导航链接
    """

    return (
        "https://uri.amap.com/navigation?"
        f"from={origin}"
        f"&to={destination}"
        "&mode=car"
    )

#驾车转换
def parse_driving(data) -> TransportInfo:

    path = data["route"]["paths"][0]
    minutes = round(int(path["duration"]) / 60)

    return TransportInfo(
        duration=format_duration(minutes),
        distance_km=round(int(path["distance"]) / 1000, 2),
        cost=round(float(path.get("tolls", 0)), 2),
    )

def parse_walking(data) -> TransportInfo:

    path = data["route"]["paths"][0]
    minutes = round(int(path["duration"]) / 60)

    return TransportInfo(
        duration=format_duration(minutes),
        distance_km=round(int(path["distance"]) / 1000, 2),
        cost=0,
    )

def parse_transit(data) -> TransportInfo:

    route = data["route"]["transits"][0]
    minutes = round(int(route["duration"]) / 60)

    return TransportInfo(
        duration=format_duration(minutes),
        distance_km=round(int(route["distance"]) / 1000, 2),
        cost=round(float(route.get("cost", 0)), 2),
    )


def get_route_summary(
    origin_name: str,
    origin_location: str,
    destination_name: str,
    destination_location: str,
    city: str,
) -> RouteResponse:

    driving_data = get_driving_route(
        origin_location,
        destination_location,
    )

    transit_data = get_transit_route(
        origin_location,
        destination_location,
        city,
    )

    walking_data = get_walking_route(
        origin_location,
        destination_location,
    )
    recommendation = get_transport_recommendation(
        parse_driving(driving_data),
        parse_transit(transit_data),
        parse_walking(walking_data),
    )

    origin_lng, origin_lat = parse_location(origin_location)
    dest_lng, dest_lat = parse_location(destination_location)

    straight_distance = calculate_straight_distance(
        origin_lng,
        origin_lat,
        dest_lng,
        dest_lat,
    )

    return RouteResponse(
        origin=origin_name,
        destination=destination_name,

        straight_distance_km=straight_distance,

        driving=parse_driving(driving_data),
        transit=parse_transit(transit_data),
        walking=parse_walking(walking_data),

        recommendation=recommendation,

        amap_url=build_amap_navigation_url(
            origin_location,
            destination_location,
        ),
        
        
    )


#时间单位转换
def format_duration(minutes: int) -> str:
    """
    将分钟格式化为用户可读时间

    例如：
    45  -> "45min"
    60  -> "1h"
    75  -> "1h15min"
    125 -> "2h5min"
    """

    if minutes < 60:
        return f"{minutes}min"

    hours = minutes // 60
    remain_minutes = minutes % 60

    if remain_minutes == 0:
        return f"{hours}h"

    return f"{hours}h{remain_minutes}min"

#推荐路线
def get_transport_recommendation(
    driving: TransportInfo,
    transit: TransportInfo,
    walking: TransportInfo,
) -> str:
    """
    返回推荐交通方式
    """

    # 2km以内优先步行
    if walking.distance_km <= 2:
        return "🚶 推荐步行，距离较近，无需乘车。"

    # 公交费用低于10元时优先公交（大学生优先省钱）
    if transit.cost is not None and transit.cost <= 10:
        return f"🚇 推荐公交/地铁，全程约{transit.duration}，仅需¥{transit.cost}。"

    # 否则推荐最快方式
    return f"🚗 推荐驾车，全程约{driving.duration}。"