"""
Risk Checker（规则版）

全部使用 Python 规则实现，不接 AI。
三类检查：
1. 时间冲突 time_conflict
2. 地点冲突 location_conflict
3. 预算冲突 budget_conflict
"""

from sqlalchemy.orm import Session

from app.models.budget_item import BudgetItem
from app.models.travel import Travel
from app.models.travel_booking import TravelBooking
from app.services.budget_service import calculate_budget_summary
from app.utils.location_utils import calculate_straight_distance


# ==========================
# 规则参数
# ==========================

# 市内交通估算速度（km/h），用于地点冲突的"是否赶得到"判断
CITY_AVG_SPEED_KMH = 30


# ==========================
# 1. 时间冲突
# ==========================
def check_time_conflict(bookings: list[TravelBooking]) -> list[dict]:
    """
    检查 Booking 时间重叠：
    酒店、餐厅、飞机、高铁、演唱会等所有带时间的订单。
    判断相邻订单（按开始时间排序）是否存在 end_time >= 下一个 start_time
    （含背靠背零缓冲的情况）。
    """
    risks = []

    # 只检查同时有 start_time 和 end_time 的订单
    timed_bookings = [
        b for b in bookings
        if b.start_time is not None and b.end_time is not None
    ]

    if len(timed_bookings) < 2:
        return risks

    # 按开始时间排序
    timed_bookings.sort(key=lambda b: b.start_time)

    # 检查相邻订单时间是否重叠
    for i in range(len(timed_bookings) - 1):
        current = timed_bookings[i]
        next_booking = timed_bookings[i + 1]

        if current.end_time >= next_booking.start_time:
            risks.append({
                "type": "time_conflict",
                "level": "high",
                "message": (
                    f"{current.name}（结束于 {current.end_time.strftime('%m-%d %H:%M')}）"
                    f" 与 {next_booking.name}"
                    f"（开始于 {next_booking.start_time.strftime('%m-%d %H:%M')}）"
                    f" 时间重叠"
                ),
                "suggestion": "请调整订单时间，避免冲突",
            })

    return risks


# ==========================
# 2. 地点冲突
# ==========================
def check_location_conflict(bookings: list[TravelBooking]) -> list[dict]:
    """
    利用 Booking 经纬度，调用已有距离计算（location_utils.calculate_straight_distance，
    map_service 内部亦用此函数）。
    若预计无法赶到下一个订单，返回 location_conflict。
    """
    risks = []

    # 只检查有经纬度且有时间的订单
    located_bookings = [
        b for b in bookings
        if b.latitude is not None
        and b.longitude is not None
        and b.start_time is not None
        and b.end_time is not None
    ]

    if len(located_bookings) < 2:
        return risks

    located_bookings.sort(key=lambda b: b.start_time)

    for i in range(len(located_bookings) - 1):
        current = located_bookings[i]
        next_booking = located_bookings[i + 1]

        # 时间重叠或背靠背交给 time_conflict 处理，这里跳过
        if current.end_time >= next_booking.start_time:
            continue

        # 直线距离（公里）—— 使用已有的 Haversine 距离计算
        distance_km = calculate_straight_distance(
            current.longitude,
            current.latitude,
            next_booking.longitude,
            next_booking.latitude,
        )

        # 估算交通时间（分钟）
        travel_minutes = (distance_km / CITY_AVG_SPEED_KMH) * 60

        # 可用时间窗口（分钟）
        time_gap_minutes = (
            next_booking.start_time - current.end_time
        ).total_seconds() / 60

        if travel_minutes > time_gap_minutes:
            risks.append({
                "type": "location_conflict",
                "level": "medium",
                "message": (
                    f"{current.name} 结束后到 {next_booking.name}："
                    f"直线距离 {distance_km:.1f}km，"
                    f"约需 {int(travel_minutes)} 分钟，"
                    f"可用时间仅 {int(time_gap_minutes)} 分钟"
                ),
                "suggestion": "建议调整行程顺序、缩短停留或预留更多交通时间",
            })

    return risks


# ==========================
# 3. 预算冲突
# ==========================
def check_budget_conflict(
    travel: Travel,
    budget_items: list[BudgetItem],
) -> list[dict]:
    """
    统计 BudgetItem 已支付 + 未支付，比较 Travel.total_budget。
    复用 budget_service.calculate_budget_summary。
    """
    risks = []

    summary = calculate_budget_summary(travel, budget_items)

    if summary["status"] == "over_budget":
        risks.append({
            "type": "budget_conflict",
            "level": "high",
            "message": (
                f"预算超支：总预算 {travel.total_budget}，"
                f"已规划 {summary['planned_cost']}"
            ),
            "suggestion": "建议删减非核心预算项或增加总预算",
        })

    elif summary["status"] == "warning":
        risks.append({
            "type": "budget_conflict",
            "level": "medium",
            "message": (
                f"预算使用率超过 80%："
                f"已规划 {summary['planned_cost']} / {travel.total_budget}"
            ),
            "suggestion": "谨慎增加新的预算项",
        })

    return risks


# ==========================
# 综合风险检查
# ==========================
def check_travel_risk(
    db: Session,
    travel_id: int,
) -> list[dict]:
    travel = db.query(Travel).filter(
        Travel.id == travel_id
    ).first()

    if travel is None:
        return []

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

    risks: list[dict] = []
    risks.extend(check_time_conflict(bookings))
    risks.extend(check_location_conflict(bookings))
    risks.extend(check_budget_conflict(travel, budget_items))

    return risks
