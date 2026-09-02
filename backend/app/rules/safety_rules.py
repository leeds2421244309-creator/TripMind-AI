"""
安全规则

规则编号：
  31. 贵重物品 → 备份护照/重要资料
  32. 夜间活动 → 注意交通安全
"""

from app.rules.rule_helpers import (
    RuleContext,
    days_before_start,
    is_overseas,
    make_todo,
)


def check(ctx: RuleContext) -> list[dict]:
    travel = ctx.travel
    todos: list[dict] = []

    # ======== 31. 贵重物品备份 ========
    if is_overseas(travel):
        todos.append(make_todo(
            title="备份重要证件和资料",
            description=(
                "国际旅行前请备份：\n"
                "- 护照首页拍照（存手机 + 云端）\n"
                "- 签证页拍照\n"
                "- 机票/酒店确认单截图\n"
                "- 紧急联系方式（使馆、保险）\n"
                "- 银行卡分别存放"
            ),
            deadline=days_before_start(travel, 3),
            category="safety",
            priority="high",
        ))

    # ======== 32. 夜间活动 ========
    night_bookings = [
        b for b in ctx.bookings
        if b.start_time and b.start_time.hour >= 22
    ]

    if night_bookings:
        names = "、".join(b.name for b in night_bookings[:3])
        todos.append(make_todo(
            title="夜间活动注意安全",
            description=(
                f"以下活动在 22:00 后开始：{names}\n"
                "夜间出行请注意：\n"
                "- 确认返程交通方式\n"
                "- 避免单独行动\n"
                "- 保存当地紧急电话"
            ),
            category="safety",
            priority="low",
        ))

    return todos
