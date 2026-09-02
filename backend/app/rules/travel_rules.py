"""
TripMind 旅行规则引擎 — 总入口

Rule Engine 聚合所有规则模块，对外提供统一接口：

    generate_rule_todos(ctx) → list[dict]

规则模块：
  - visa_rules       证件/签证
  - transport_rules  交通
  - destination_rules 目的地+住宿
  - budget_rules     预算
  - schedule_rules   时间规划
  - packing_rules    行李+设备
  - safety_rules     安全

后续接入 AI Agent 时：
  - 规则负责：确保不漏重要事项
  - AI   负责：个性化表达和调整优先级
"""

from sqlalchemy.orm import Session

from app.models.budget_item import BudgetItem
from app.models.travel import Travel
from app.models.travel_booking import TravelBooking
from app.models.travel_preference import TravelPreference
from app.models.travel_wishlist import TravelWishlist
from app.rules.rule_helpers import RuleContext
from app.rules import (
    budget_rules,
    destination_rules,
    packing_rules,
    safety_rules,
    schedule_rules,
    transport_rules,
    visa_rules,
)

# 规则模块按优先级排序（证件 > 交通 > 住宿 > 预算 > 行程 > 行李 > 安全）
_RULE_MODULES = [
    visa_rules,
    transport_rules,
    destination_rules,
    budget_rules,
    schedule_rules,
    packing_rules,
    safety_rules,
]


def build_context(
    db: Session,
    travel_id: int,
) -> RuleContext | None:
    """
    从数据库加载旅行上下文。

    :return: RuleContext 或 None（旅行不存在时）
    """
    travel = db.query(Travel).filter(
        Travel.id == travel_id,
    ).first()

    if travel is None:
        return None

    bookings = (
        db.query(TravelBooking)
        .filter(TravelBooking.travel_id == travel_id)
        .all()
    )

    budget_items = (
        db.query(BudgetItem)
        .filter(BudgetItem.travel_id == travel_id)
        .all()
    )

    preference = (
        db.query(TravelPreference)
        .filter(TravelPreference.travel_id == travel_id)
        .first()
    )

    wishlist = (
        db.query(TravelWishlist)
        .filter(TravelWishlist.travel_id == travel_id)
        .all()
    )

    return RuleContext(
        travel=travel,
        bookings=bookings,
        budget_items=budget_items,
        preference=preference,
        wishlist=wishlist,
    )


def generate_rule_todos(ctx: RuleContext) -> list[dict]:
    """
    运行所有规则模块，聚合返回 Todo 模板列表。

    每个模块返回 list[dict]，格式见 rule_helpers.make_todo()。
    """
    all_todos: list[dict] = []

    for module in _RULE_MODULES:
        try:
            todos = module.check(ctx)
            all_todos.extend(todos)
        except Exception:
            # 单个规则模块出错不影响其它模块
            pass

    return all_todos
