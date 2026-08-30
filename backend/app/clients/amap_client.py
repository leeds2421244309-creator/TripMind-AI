"""
高德地图客户端

负责：
1. 请求高德API
2. POI搜索
3. 返回地图数据

业务逻辑不要写这里
"""

import requests

from app.core.config import settings


def search_poi(
    keyword: str,
    city:str|None=None):
    """
    POI关键词搜索

    参数:
        keyword:
            景点名称

    返回:
        景点基本信息
    """


    url = f"{settings.AMAP_BASE_URL}/v3/place/text"


    params = {
        "key": settings.AMAP_API_KEY,
        "keywords": keyword,
        "output": "json"
    }

    if city:
        params["city"] = city

    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    # 高德返回状态判断
    if data.get("status") != "1":
        return None


    pois = data.get("pois")


    if not pois:
        return None


    poi = pois[0]


    longitude, latitude = poi["location"].split(",")


    return {
        "name": poi["name"],
        "address": poi["address"],
        "location": poi["location"] ,
        "longitude": float(longitude),
        "latitude": float(latitude)
    }