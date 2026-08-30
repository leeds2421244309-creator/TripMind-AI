from math import radians, sin, cos, sqrt, atan2


def parse_location(location: str) -> tuple[float, float]:
    """
    将高德 location 字符串解析为 (lng, lat)

    输入：
        "114.057865,22.543096"

    输出：
        (114.057865, 22.543096)
    """

    lng, lat = location.split(",")

    return float(lng), float(lat)


EARTH_RADIUS_KM = 6371

def calculate_straight_distance(
    origin_lng: float,
    origin_lat: float,
    dest_lng: float,
    dest_lat: float,
) -> float:
    """
    使用 Haversine 算法计算两点直线距离（公里）
    """

    # 转为弧度
    origin_lat = radians(origin_lat)
    origin_lng = radians(origin_lng)
    dest_lat = radians(dest_lat)
    dest_lng = radians(dest_lng)

    d_lat = dest_lat - origin_lat
    d_lng = dest_lng - origin_lng

    a = (
        sin(d_lat / 2) ** 2
        + cos(origin_lat)
        * cos(dest_lat)
        * sin(d_lng / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = EARTH_RADIUS_KM * c

    return round(distance, 2)