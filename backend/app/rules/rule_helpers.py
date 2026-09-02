"""
规则引擎公共工具

包含：
1. RuleContext — 所有规则共享的上下文
2. 地理检测函数 — 判断目的地类型（港澳/台湾/国际/国内）
3. 日期辅助 — 相对于出发日期的 deadline 计算
4. Todo 模板构造器 — 统一 dict 格式
"""

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Any

from app.models.budget_item import BudgetItem
from app.models.travel import Travel
from app.models.travel_booking import TravelBooking
from app.models.travel_preference import TravelPreference
from app.models.travel_wishlist import TravelWishlist


# ============================================================
# RuleContext — 规则上下文
# ============================================================

@dataclass
class RuleContext:
    """所有规则函数共享的旅行上下文"""

    travel: Travel
    bookings: list[TravelBooking] = field(default_factory=list)
    budget_items: list[BudgetItem] = field(default_factory=list)
    preference: TravelPreference | None = None
    wishlist: list[TravelWishlist] = field(default_factory=list)


# ============================================================
# Todo 模板格式
# ============================================================

def make_todo(
    title: str,
    description: str = "",
    deadline: datetime | None = None,
    day_number: int = 0,
    category: str = "general",
    priority: str = "medium",
) -> dict[str, Any]:
    """
    构造统一的 Todo 模板 dict。

    :param title:       标题
    :param description: 描述
    :param deadline:    提醒时间（None = 无具体截止时间）
    :param day_number:  第几天（0 = 出发前准备）
    :param category:    分类 document / visa / transport / hotel / budget / schedule / packing / safety / equipment
    :param priority:    优先级 high / medium / low
    """
    return {
        "title": title,
        "description": description,
        "deadline": deadline,
        "day_number": day_number,
        "category": category,
        "priority": priority,
    }


# ============================================================
# 地理关键词库
# ============================================================

HONG_KONG_MACAU_KEYWORDS = {
    "香港", "澳门", "港澳", "HK", "Macau", "macau",
    "Hong Kong", "hong kong",
}

TAIWAN_KEYWORDS = {
    "台湾", "台北", "高雄", "台南", "台中",
    "Taiwan", "taipei", "Taipei",
}

# 国际目的地关键词（不含港澳台，港澳台单独处理）
INTERNATIONAL_KEYWORDS = {
    # 亚洲
    "日本", "东京", "大阪", "京都", "北海道", "札幌", "冲绳", "奈良", "福冈",
    "韩国", "首尔", "釜山", "济州",
    "泰国", "曼谷", "清迈", "普吉", "芭提雅",
    "新加坡", "马来西亚", "吉隆坡", "槟城",
    "印尼", "巴厘岛", "雅加达",
    "越南", "河内", "胡志明", "岘港",
    "柬埔寨", "暹粒", "吴哥",
    "菲律宾", "马尼拉", "长滩",
    "老挝", "琅勃拉邦",
    "缅甸", "仰光",
    "印度", "新德里", "孟买",
    "尼泊尔", "加德满都",
    "斯里兰卡", "科伦坡",
    "马尔代夫", "Maldives",
    # 中东
    "迪拜", "阿联酋", "卡塔尔", "多哈", "土耳其", "伊斯坦布尔",
    # 欧洲
    "法国", "巴黎", "尼斯", " Lyon",
    "英国", "伦敦", "曼彻斯特", "爱丁堡",
    "意大利", "罗马", "米兰", "威尼斯", "佛罗伦萨", "那不勒斯",
    "西班牙", "巴塞罗那", "马德里", "塞维利亚",
    "德国", "柏林", "慕尼黑", "法兰克福", "汉堡",
    "瑞士", "苏黎世", "日内瓦", "因特拉肯",
    "荷兰", "阿姆斯特丹",
    "比利时", "布鲁塞尔",
    "奥地利", "维也纳", "萨尔茨堡",
    "希腊", "雅典", "圣托里尼", "米克诺斯",
    "葡萄牙", "里斯本", "波尔图",
    "爱尔兰", "都柏林",
    "瑞典", "斯德哥尔摩",
    "挪威", "奥斯陆",
    "芬兰", "赫尔辛基",
    "丹麦", "哥本哈根",
    "冰岛", "雷克雅未克",
    "波兰", "华沙",
    "捷克", "布拉格",
    "匈牙利", "布达佩斯",
    "克罗地亚", "萨格勒布", "杜布罗夫尼克",
    "塞尔维亚", "贝尔格莱德",
    "俄罗斯", "莫斯科", "圣彼得堡",
    # 美洲
    "美国", "纽约", "洛杉矶", "旧金山", "夏威夷", "关岛", "塞班",
    "加拿大", "多伦多", "温哥华", "蒙特利尔",
    "墨西哥", "坎昆",
    "巴西", "里约", "圣保罗",
    "阿根廷", "布宜诺斯艾利斯",
    "秘鲁", "利马",
    "古巴", "哈瓦那",
    # 大洋洲
    "澳大利亚", "悉尼", "墨尔本", "布里斯班", "黄金海岸",
    "新西兰", "奥克兰", "皇后镇",
    # 非洲
    "埃及", "开罗",
    "摩洛哥", "马拉喀什", "卡萨布兰卡",
    "肯尼亚", "南非", "开普敦",
}

# 需要提前办签证的国家（中国大陆护照）
VISA_REQUIRED_KEYWORDS = {
    "美国", "纽约", "洛杉矶", "旧金山", "夏威夷", "关岛", "塞班",
    "加拿大", "多伦多", "温哥华", "蒙特利尔",
    "澳大利亚", "悉尼", "墨尔本", "布里斯班", "黄金海岸",
    "新西兰", "奥克兰", "皇后镇",
    "俄罗斯", "莫斯科", "圣彼得堡",
    "印度", "新德里", "孟买",
    "巴西", "里约", "圣保罗",
    "阿根廷", "布宜诺斯艾利斯",
    "埃及", "开罗",
}

# 免签/落地签国家
VISA_FREE_KEYWORDS = {
    "日本", "东京", "大阪", "京都", "北海道", "札幌", "冲绳", "奈良", "福冈",
    "韩国", "首尔", "釜山", "济州",
    "泰国", "曼谷", "清迈", "普吉", "芭提雅",
    "新加坡", "马来西亚", "吉隆坡", "槟城",
    "印尼", "巴厘岛", "雅加达",
    "越南", "河内", "胡志明", "岘港",
    "柬埔寨", "暹粒", "吴哥",
    "菲律宾", "马尼拉", "长滩",
    "老挝", "琅勃拉邦",
    "缅甸", "仰光",
    "斯里兰卡", "科伦坡",
    "马尔代夫", "Maldives",
    "迪拜", "阿联酋", "卡塔尔", "多哈",
    "格鲁吉亚", "亚美尼亚",
    "塞尔维亚", "贝尔格莱德",
    "摩洛哥", "马拉喀什", "卡萨布兰卡",
    "古巴", "哈瓦那",
}

# 海岛关键词
ISLAND_KEYWORDS = {
    "海岛", "沙滩", "潜水", "浮潜",
    "巴厘岛", "普吉岛", "马尔代夫", "长滩岛", "塞班", "关岛", "冲绳",
    "济州岛", "兰卡威", "芽庄", "岘港", "薄荷岛",
    "夏威夷", "大溪地", "斐济", "塞舌尔", "毛里求斯",
    "圣托里尼", "巴厘", "沙巴",
}

# 主题乐园关键词
THEME_PARK_KEYWORDS = {
    "迪士尼", "disney", "Disney", "DISNEY",
    "环球", "universal", "Universal",
    "乐园", "乐高", "legoland",
}

# 演唱会/活动关键词
CONCERT_KEYWORDS = {
    "演唱会", "concert", "Concert", "CONCERT",
    "音乐节", "festival", "Festival",
    "live", "Live", "LIVE",
    "演出", "巡演",
}


# ============================================================
# 地理检测函数
# ============================================================

def _contains_any(text: str, keywords: set[str]) -> bool:
    """判断 text 中是否包含 keywords 中的任意一个"""
    return any(k in text for k in keywords)


def is_hong_kong_macau(travel: Travel) -> bool:
    return _contains_any(travel.destination, HONG_KONG_MACAU_KEYWORDS)


def is_taiwan(travel: Travel) -> bool:
    return _contains_any(travel.destination, TAIWAN_KEYWORDS)


def is_international(travel: Travel) -> bool:
    """判断是否国际旅行（含港澳台）"""
    if is_hong_kong_macau(travel) or is_taiwan(travel):
        return True
    return _contains_any(travel.destination, INTERNATIONAL_KEYWORDS)


def is_overseas(travel: Travel) -> bool:
    """判断是否海外旅行（不含港澳台，纯国际）"""
    if is_hong_kong_macau(travel) or is_taiwan(travel):
        return False
    return _contains_any(travel.destination, INTERNATIONAL_KEYWORDS)


def needs_visa(travel: Travel) -> bool:
    """是否需要办理签证"""
    return _contains_any(travel.destination, VISA_REQUIRED_KEYWORDS)


def is_visa_free(travel: Travel) -> bool:
    """是否免签/落地签"""
    return _contains_any(travel.destination, VISA_FREE_KEYWORDS)


def has_island_keywords(travel: Travel) -> bool:
    return _contains_any(travel.destination, ISLAND_KEYWORDS)


def has_theme_park_keywords(travel: Travel) -> bool:
    text = travel.destination + " " + travel.goal
    for item in travel.wishlist:
        text += " " + item.name
    return _contains_any(text, THEME_PARK_KEYWORDS)


def has_concert_keywords(travel: Travel) -> bool:
    text = travel.destination + " " + travel.goal
    for b in travel.bookings:
        text += " " + (b.name or "")
    return _contains_any(text, CONCERT_KEYWORDS)


# ============================================================
# 日期辅助
# ============================================================

def days_before_start(travel: Travel, days: int) -> datetime:
    """出发前 N 天的 09:00"""
    return datetime.combine(
        travel.start_date - timedelta(days=days),
        time(9, 0),
    )


def hours_before_start(travel: Travel, hours: int) -> datetime:
    """出发前 N 小时"""
    return datetime.combine(
        travel.start_date, time(9, 0)
    ) - timedelta(hours=hours)


def trip_days(travel: Travel) -> int:
    """旅行天数（含首尾）"""
    return (travel.end_date - travel.start_date).days + 1


def budget_per_day(travel: Travel) -> float:
    """日均预算"""
    days = trip_days(travel)
    if days <= 0:
        return 0.0
    return travel.total_budget / days


# ============================================================
# 地区日均消费参考（CNY）
# ============================================================

REGION_DAILY_BUDGET = {
    "southeast_asia": 300,   # 东南亚
    "east_asia": 500,         # 日韩
    "europe": 800,            # 欧洲
    "north_america": 800,     # 北美
    "oceania": 700,           # 澳新
    "middle_east": 600,       # 中东
    "domestic": 200,          # 国内
    "default": 300,
}

_SEA_KEYWORDS = {"泰国", "曼谷", "清迈", "普吉", "新加坡", "马来西亚",
                 "印尼", "巴厘岛", "越南", "柬埔寨", "菲律宾", "老挝", "缅甸"}
_EA_KEYWORDS = {"日本", "东京", "大阪", "韩国", "首尔", "釜山"}
_EU_KEYWORDS = {"法国", "英国", "意大利", "西班牙", "德国", "瑞士", "荷兰",
                "奥地利", "希腊", "葡萄牙", "爱尔兰", "瑞典", "挪威",
                "芬兰", "丹麦", "冰岛", "波兰", "捷克", "匈牙利", "克罗地亚"}
_NA_KEYWORDS = {"美国", "纽约", "洛杉矶", "加拿大", "多伦多", "温哥华"}
_OC_KEYWORDS = {"澳大利亚", "悉尼", "新西兰", "奥克兰"}
_ME_KEYWORDS = {"迪拜", "阿联酋", "卡塔尔", "土耳其", "埃及", "摩洛哥"}


def region_daily_budget(travel: Travel) -> int:
    """根据目的地返回日均消费参考（CNY）"""
    dest = travel.destination
    if _contains_any(dest, _SEA_KEYWORDS):
        return REGION_DAILY_BUDGET["southeast_asia"]
    if _contains_any(dest, _EA_KEYWORDS):
        return REGION_DAILY_BUDGET["east_asia"]
    if _contains_any(dest, _EU_KEYWORDS):
        return REGION_DAILY_BUDGET["europe"]
    if _contains_any(dest, _NA_KEYWORDS):
        return REGION_DAILY_BUDGET["north_america"]
    if _contains_any(dest, _OC_KEYWORDS):
        return REGION_DAILY_BUDGET["oceania"]
    if _contains_any(dest, _ME_KEYWORDS):
        return REGION_DAILY_BUDGET["middle_east"]
    if is_international(travel):
        return REGION_DAILY_BUDGET["default"]
    return REGION_DAILY_BUDGET["domestic"]
