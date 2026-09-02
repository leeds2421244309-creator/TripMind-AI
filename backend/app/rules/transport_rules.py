"""
交通规则

规则编号：
  6. 飞机 → 确认航班信息 + 线上值机
  7. 国内飞机 → 提前 2 小时到机场
  8. 国际航班 → 提前 3 小时到机场
  9. 火车 → 购票 + 确认车站
"""

from datetime import timedelta

from app.enums.booking_type import BookingType
from app.rules.rule_helpers import (
    RuleContext,
    days_before_start,
    hours_before_start,
    is_overseas,
    make_todo,
)


def check(ctx: RuleContext) -> list[dict]:
    travel = ctx.travel
    todos: list[dict] = []

    has_flight = False
    has_intl_flight = False
    has_train = False

    for booking in ctx.bookings:
        # ======== 6/7/8. 飞机 ========
        if booking.booking_type == BookingType.FLIGHT:
            has_flight = True

            # 确认航班信息（出发前 24 小时）
            todos.append(make_todo(
                title=f"确认航班信息 - {booking.name}",
                description=(
                    f"航班号：{booking.name}\n"
                    f"出发时间：{booking.start_time.strftime('%m-%d %H:%M') if booking.start_time else '未定'}\n"
                    "请确认航班未变更，查看起飞航站楼。"
                ),
                deadline=hours_before_start(travel, 24),
                category="transport",
                priority="high",
            ))

            # 办理线上值机（出发前 24 小时）
            todos.append(make_todo(
                title=f"办理线上值机 - {booking.name}",
                description=(
                    "大多数航空公司支持起飞前 24 小时线上值机。"
                    "建议提前选座，尤其长途航班。"
                ),
                deadline=hours_before_start(travel, 24),
                category="transport",
                priority="medium",
            ))

            # 提前到达机场
            intl = is_overseas(travel)
            if intl:
                has_intl_flight = True
                lead = 3
                desc = (
                    "国际航班建议起飞前 3 小时到达机场，"
                    "预留值机、托运、海关、安检时间。"
                )
            else:
                lead = 2
                desc = (
                    "国内航班建议起飞前 2 小时到达机场，"
                    "预留值机、托运、安检时间。"
                )

            if booking.start_time:
                todos.append(make_todo(
                    title=f"提前{lead}小时到达机场 - {booking.name}",
                    description=desc,
                    deadline=booking.start_time - timedelta(hours=lead),
                    category="transport",
                    priority="high",
                ))

        # ======== 9. 火车 ========
        elif booking.booking_type == BookingType.TRAIN:
            has_train = True

            todos.append(make_todo(
                title=f"确认乘车站 - {booking.name}",
                description=(
                    f"出发时间：{booking.start_time.strftime('%m-%d %H:%M') if booking.start_time else '未定'}\n"
                    "请确认出发车站名称（注意同城可能有多个站），"
                    "提前查看交通到站路线。"
                ),
                deadline=days_before_start(travel, 1),
                category="transport",
                priority="medium",
            ))

            if booking.start_time:
                todos.append(make_todo(
                    title=f"提前30分钟到站 - {booking.name}",
                    description="建议发车前 30 分钟到达车站，预留安检和检票时间。",
                    deadline=booking.start_time - timedelta(minutes=30),
                    category="transport",
                    priority="medium",
                ))

        # ======== 大巴/轮渡 ========
        elif booking.booking_type in (BookingType.BUS, BookingType.FERRY):
            if booking.start_time:
                todos.append(make_todo(
                    title=f"提前到达乘车点 - {booking.name}",
                    description="建议提前 20 分钟到达乘车点/码头。",
                    deadline=booking.start_time - timedelta(minutes=20),
                    category="transport",
                    priority="low",
                ))

    # 如果有航班但没在 bookings 里（可能是用户手动添加），仍然提醒
    if not has_flight and is_overseas(travel):
        todos.append(make_todo(
            title="提前预订机票",
            description=(
                "国际旅行建议提前 1-2 个月预订机票，"
                "通常价格更优惠。"
            ),
            deadline=days_before_start(travel, 60),
            category="transport",
            priority="high",
        ))

    return todos
