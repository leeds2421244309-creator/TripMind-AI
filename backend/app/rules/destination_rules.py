"""
目的地 + 住宿规则

规则编号：
  10. 酒店入住 → 确认入住时间 + 保存地址
  11. 酒店距离主要景点远 → 提醒
  22. 海岛旅行 → 泳衣 + 防晒
  23. 演唱会旅行 → 确认时间 + 门票
  24. 迪士尼/环球影城 → 门票 + APP
"""

from app.enums.booking_type import BookingType
from app.rules.rule_helpers import (
    RuleContext,
    days_before_start,
    has_concert_keywords,
    has_island_keywords,
    has_theme_park_keywords,
    make_todo,
)
from app.utils.location_utils import calculate_straight_distance


def check(ctx: RuleContext) -> list[dict]:
    travel = ctx.travel
    todos: list[dict] = []

    # ======== 10. 酒店入住确认 ========
    hotel_bookings = [
        b for b in ctx.bookings
        if b.booking_type == BookingType.HOTEL
    ]

    for hotel in hotel_bookings:
        todos.append(make_todo(
            title=f"确认酒店入住信息 - {hotel.name}",
            description=(
                f"入住时间：{hotel.start_time.strftime('%m-%d %H:%M') if hotel.start_time else '未定'}\n"
                f"退房时间：{hotel.end_time.strftime('%m-%d %H:%M') if hotel.end_time else '未定'}\n"
                f"地址：{hotel.address or '未填写'}\n"
                "建议保存酒店地址到手机，并截图离线保存。"
            ),
            deadline=days_before_start(travel, 1),
            category="hotel",
            priority="medium",
        ))

    # ======== 11. 酒店距离主要景点远 ========
    if hotel_bookings and ctx.wishlist:
        hotel = hotel_bookings[0]  # 取第一个酒店
        if hotel.latitude and hotel.longitude:
            far_attractions = []
            for item in ctx.wishlist:
                if item.latitude and item.longitude:
                    distance = calculate_straight_distance(
                        hotel.longitude, hotel.latitude,
                        item.longitude, item.latitude,
                    )
                    if distance > 15:
                        far_attractions.append((item.name, distance))

            if far_attractions:
                names = "、".join(
                    f"{name}（{dist:.0f}km）"
                    for name, dist in far_attractions[:3]
                )
                todos.append(make_todo(
                    title="住宿位置距部分景点较远",
                    description=(
                        f"酒店 {hotel.name} 距以下景点较远：\n"
                        f"{names}\n"
                        "可能影响每日交通时间，"
                        "建议调整住宿或预留充足交通时间。"
                    ),
                    category="hotel",
                    priority="low",
                ))

    # ======== 22. 海岛旅行 ========
    if has_island_keywords(travel):
        todos.append(make_todo(
            title="准备海岛用品",
            description=(
                "海岛目的地建议准备：\n"
                "- 泳衣、浮潜面镜\n"
                "- 高倍防晒霜（SPF50+）\n"
                "- 防水手机袋\n"
                "- 凉鞋/拖鞋\n"
                "- 晒后修复用品"
            ),
            category="packing",
            priority="medium",
        ))

    # ======== 23. 演唱会/活动 ========
    if has_concert_keywords(travel):
        todos.append(make_todo(
            title="确认演唱会/活动门票",
            description=(
                "请确认门票已购买，电子票请截图保存。"
                "查看场馆入场规则和交通路线。"
            ),
            deadline=days_before_start(travel, 3),
            category="destination",
            priority="high",
        ))
        todos.append(make_todo(
            title="准备应援/活动物品",
            description="根据活动类型准备应援物、充电宝等。",
            category="packing",
            priority="low",
        ))

    # ======== 24. 迪士尼/环球影城 ========
    if has_theme_park_keywords(travel):
        todos.append(make_todo(
            title="提前购买乐园门票",
            description=(
                "迪士尼/环球影城建议提前在官方渠道购票，"
                "现场购票排队时间长且可能售罄。"
            ),
            deadline=days_before_start(travel, 7),
            category="destination",
            priority="high",
        ))
        todos.append(make_todo(
            title="下载乐园官方 APP",
            description=(
                "下载官方 APP 查看实时排队、预约快速通行证、"
                "地图导航和表演时间表。"
            ),
            deadline=days_before_start(travel, 3),
            category="destination",
            priority="medium",
        ))
        todos.append(make_todo(
            title="查看项目预约规则",
            description=(
                "部分热门项目需单独预约或抽签，"
                "请提前在 APP 上了解规则。"
            ),
            deadline=days_before_start(travel, 2),
            category="destination",
            priority="medium",
        ))

    return todos
