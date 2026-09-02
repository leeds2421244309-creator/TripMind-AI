"""
行李 + 设备规则

规则编号：
  20. 冬季旅行 → 保暖衣物
  21. 夏季旅行 → 防晒 + 补水
  25. 摄影旅行 → 相机设备
  29. 国际旅行 → 漫游/转换插头
  30. 摄影设备 → 充电、备用电池、存储卡
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

    month = travel.start_date.month

    # ======== 20. 冬季旅行 ========
    if month in (12, 1, 2):
        todos.append(make_todo(
            title="准备冬季保暖衣物",
            description=(
                "冬季出行建议准备：\n"
                "- 羽绒服/厚外套\n"
                "- 保暖内衣\n"
                "- 手套、围巾、帽子\n"
                "- 保暖鞋"
            ),
            deadline=days_before_start(travel, 7),
            category="packing",
            priority="medium",
        ))

    # ======== 21. 夏季旅行 ========
    if month in (6, 7, 8):
        todos.append(make_todo(
            title="准备夏季防晒用品",
            description=(
                "夏季出行建议准备：\n"
                "- 防晒霜（SPF50+）\n"
                "- 太阳镜、遮阳帽\n"
                "- 轻薄透气衣物\n"
                "- 便携水杯/补水用品"
            ),
            deadline=days_before_start(travel, 7),
            category="packing",
            priority="medium",
        ))

    # ======== 25/30. 摄影旅行 ========
    # 检查偏好或 wishlist 是否含摄影关键词
    photography_keywords = {"摄影", "拍照", "相机", "photo", "Photo"}
    has_photography = False

    # 检查 preference 中的 prompt 字段
    if ctx.preference:
        for field_name in (
            "hotel_prompt", "food_prompt",
            "transport_prompt", "local_transport_prompt",
        ):
            value = getattr(ctx.preference, field_name, None)
            if value and any(k in value for k in photography_keywords):
                has_photography = True
                break

    # 检查 wishlist name
    if not has_photography:
        for item in ctx.wishlist:
            if any(k in item.name for k in photography_keywords):
                has_photography = True
                break

    if has_photography:
        todos.append(make_todo(
            title="准备摄影设备",
            description=(
                "摄影旅行建议检查：\n"
                "- 相机、镜头清洁\n"
                "- 备用电池（至少 2 块）\n"
                "- 存储卡（备 1-2 张）\n"
                "- 充电器、移动电源\n"
                "- 三脚架（如需夜景）"
            ),
            deadline=days_before_start(travel, 3),
            category="equipment",
            priority="medium",
        ))

    # ======== 29. 国际旅行 - 设备 ========
    if is_overseas(travel):
        todos.append(make_todo(
            title="检查手机漫游/流量套餐",
            description=(
                "国际旅行建议：\n"
                "- 开通国际漫游或购买当地 SIM 卡\n"
                "- 下载离线地图\n"
                "- 确认手机支付在目的地可用"
            ),
            deadline=days_before_start(travel, 5),
            category="equipment",
            priority="medium",
        ))
        todos.append(make_todo(
            title="准备转换插头",
            description=(
                "不同国家插座类型不同，请根据目的地准备转换插头：\n"
                "- 欧洲：Type C/E/F（圆脚两孔）\n"
                "- 英联邦：Type G（方脚三孔）\n"
                "- 北美：Type A/B（扁脚）\n"
                "- 日韩：Type A（扁脚两孔）"
            ),
            deadline=days_before_start(travel, 5),
            category="equipment",
            priority="medium",
        ))

    return todos
