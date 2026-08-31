from app.models.budget_item import BudgetItem
from app.models.travel import Travel
from app.enums.payment_status import PaymentStatus


# ==========================
# 计算单个预算项金额
# ==========================
def calculate_item_cost(unit_cost: int, quantity: int) -> int:
    return unit_cost * quantity


# ==========================
# 判断预算状态
# ==========================
def get_budget_status(total_budget: int, planned_cost: int) -> str:
    if total_budget <= 0:
        return "normal"

    usage = planned_cost / total_budget

    if usage > 1:
        return "over_budget"

    if usage >= 0.8:
        return "warning"

    return "normal"


# ==========================
# 统计整趟旅行预算
# ==========================
def calculate_budget_summary(
    travel: Travel,
    budget_items: list[BudgetItem]
) -> dict:

    planned_cost = 0
    paid_cost = 0
    pending_cost = 0

    category_summary = {}

    for item in budget_items:

        # 已取消的不参与预算
        if item.payment_status == PaymentStatus.cancelled:
            continue

        item_cost = calculate_item_cost(
            item.unit_cost,
            item.quantity
        )

        planned_cost += item_cost

        if item.payment_status == PaymentStatus.paid:
            paid_cost += item_cost

        elif item.payment_status in [
            PaymentStatus.PENDING,
            PaymentStatus.UNDECIDED,
        ]:
            pending_cost += item_cost

        # 分类统计
        category_summary[item.category] = (
            category_summary.get(item.category, 0)
            + item_cost
        )

    remaining_budget = travel.total_budget - planned_cost

    usage = (
        round(planned_cost / travel.total_budget * 100, 1)
        if travel.total_budget
        else 0
    )

    status = get_budget_status(
        travel.total_budget,
        planned_cost
    )

    return {
        "total_budget": travel.total_budget,
        "planned_cost": planned_cost,
        "paid_cost": paid_cost,
        "pending_cost": pending_cost,
        "remaining_budget": remaining_budget,
        "budget_usage": usage,
        "status": status,
        "category_summary": category_summary,
    }


# ==========================
# 生成预算洞察
# ==========================
def generate_budget_insight(summary: dict) -> dict:

    category_summary = summary["category_summary"]
    planned_cost = summary["planned_cost"]

    category_percent = {}

    if planned_cost > 0:
        for category, cost in category_summary.items():
            category_percent[category] = round(
                cost / planned_cost * 100,
                1
            )

    largest_category = (
        max(category_summary, key=category_summary.get)
        if category_summary else "暂无"
    )

    insights = []

    # 预算状态提醒
    if summary["status"] == "over_budget":
        insights.append("⚠️ 当前预算已超支，建议调整酒店或门票预算。")

    elif summary["status"] == "warning":
        insights.append("💰 当前预算已使用80%以上，请谨慎增加新的预算项。")

    else:
        insights.append("✅ 当前预算充足，可以继续规划旅行。")

    # 酒店占比提醒
    if category_percent.get("住宿", 0) >= 40:
        insights.append("🏨 酒店支出占预算较高，可以尝试选择更优惠住宿。")

    # 餐饮提醒
    if category_percent.get("餐饮", 0) <= 10:
        insights.append("🍜 餐饮预算偏低，建议预留更多每日餐饮费用。")

    # 待支付提醒
    if summary["pending_cost"] >= summary["total_budget"] * 0.5:
        insights.append("🟡 待支付金额较多，请提前确认酒店、门票等订单。")

    return {
        "category_summary": category_summary,
        "category_percent": category_percent,
        "largest_category": largest_category,
        "remaining_budget": summary["remaining_budget"],
        "status": summary["status"],
        "insights": insights,
    }