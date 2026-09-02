"""
预算规则

规则编号：
  12. 超预算 → 调整住宿/交通预算
  13. 日均预算不足 → 提醒
"""

from app.rules.rule_helpers import (
    RuleContext,
    budget_per_day,
    make_todo,
    region_daily_budget,
    trip_days,
)
from app.services.budget_service import calculate_budget_summary


def check(ctx: RuleContext) -> list[dict]:
    travel = ctx.travel
    todos: list[dict] = []

    # ======== 12. 超预算 ========
    summary = calculate_budget_summary(travel, ctx.budget_items)

    if summary["status"] == "over_budget":
        todos.append(make_todo(
            title="预算超支提醒",
            description=(
                f"总预算 {travel.total_budget} 元，"
                f"已规划 {summary['planned_cost']} 元，"
                f"超支 {summary['planned_cost'] - travel.total_budget} 元。\n"
                "建议：删减非核心预算项，或增加总预算。"
            ),
            category="budget",
            priority="high",
        ))

    elif summary["status"] == "warning":
        todos.append(make_todo(
            title="预算使用率较高",
            description=(
                f"已规划 {summary['planned_cost']} / {travel.total_budget} 元"
                f"（{summary.get('usage', 0)}%）。\n"
                "谨慎增加新的预算项。"
            ),
            category="budget",
            priority="medium",
        ))

    # ======== 13. 日均预算不足 ========
    days = trip_days(travel)
    daily = budget_per_day(travel)
    ref = region_daily_budget(travel)

    if daily > 0 and daily < ref:
        todos.append(make_todo(
            title="日均预算可能不足",
            description=(
                f"旅行 {days} 天，总预算 {travel.total_budget} 元，"
                f"日均 {daily:.0f} 元。\n"
                f"目的地日均消费参考约 {ref} 元。\n"
                "建议增加预算或调整行程天数。"
            ),
            category="budget",
            priority="medium",
        ))

    return todos
