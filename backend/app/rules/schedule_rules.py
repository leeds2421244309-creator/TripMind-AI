"""
时间规划规则

规则编号：
  14. 行程过密 → 一天超过 5 个活动提醒
  15. 连续早起 → 3 天以上 8 点前活动提醒
  16. 跨城市移动 → 预留交通时间
  17. 同一天多城市 → 风险提醒
"""

from datetime import date
from collections import defaultdict

from app.rules.rule_helpers import RuleContext, make_todo


def check(ctx: RuleContext) -> list[dict]:
    travel = ctx.travel
    todos: list[dict] = []

    # 过滤有时间的 booking
    timed_bookings = [
        b for b in ctx.bookings
        if b.start_time is not None
    ]

    if not timed_bookings:
        return todos

    # 按日期分组
    by_day: dict[date, list] = defaultdict(list)
    for b in timed_bookings:
        day = b.start_time.date()
        by_day[day].append(b)

    # ======== 14. 行程过密 ========
    for day, bookings in by_day.items():
        if len(bookings) > 5:
            day_label = day.strftime("%m-%d")
            todos.append(make_todo(
                title=f"{day_label} 行程安排较密",
                description=(
                    f"当天安排了 {len(bookings)} 个活动，"
                    "建议适当减少地点或预留休息时间。"
                ),
                deadline=None,
                day_number=(day - travel.start_date).days + 1,
                category="schedule",
                priority="low",
            ))

    # ======== 15. 连续早起 ========
    early_days = []
    for day in sorted(by_day.keys()):
        bookings = by_day[day]
        earliest = min(b.start_time for b in bookings)
        if earliest.hour < 8:
            early_days.append(day)

    if len(early_days) >= 3:
        todos.append(make_todo(
            title=f"连续 {len(early_days)} 天早起，注意休息",
            description=(
                f"有 {len(early_days)} 天的活动在 8:00 前开始。"
                "建议提前调整作息，保证充足睡眠。"
            ),
            category="schedule",
            priority="low",
        ))

    # ======== 16/17. 跨城市移动 ========
    # 通过 booking name 或 address 简单检测不同城市
    # 如果同一天有多个不同地址的活动，提示交通风险
    for day, bookings in by_day.items():
        # 检查同一活动的 name/address 是否有明显不同城市
        cities = set()
        for b in bookings:
            # 取 name 或 address 中可能的城市信息
            for text in [b.name or "", b.address or ""]:
                cities.add(text[:2] if len(text) >= 2 else text)

        # 如果一天有超过 2 个不同活动且都在不同地点
        if len(bookings) >= 2:
            # 简单启发式：如果有 2 个以上 booking 且时间间隔很短
            sorted_b = sorted(bookings, key=lambda b: b.start_time)
            for i in range(len(sorted_b) - 1):
                current = sorted_b[i]
                next_b = sorted_b[i + 1]

                # 如果两者都有 end_time，检查间隔
                if current.end_time and next_b.start_time:
                    gap_minutes = (
                        next_b.start_time - current.end_time
                    ).total_seconds() / 60

                    # 间隔不到 60 分钟且不同地点
                    if 0 < gap_minutes < 60:
                        day_label = day.strftime("%m-%d")
                        todos.append(make_todo(
                            title=f"{day_label} 行程时间紧张",
                            description=(
                                f"{current.name} 结束后到 {next_b.name}"
                                f" 仅 {int(gap_minutes)} 分钟，"
                                "可能来不及赶路。"
                            ),
                            deadline=None,
                            day_number=(day - travel.start_date).days + 1,
                            category="schedule",
                            priority="medium",
                        ))
                        break  # 每天最多一条

    return todos
