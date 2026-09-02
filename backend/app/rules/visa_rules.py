"""
证件 / 签证规则

规则编号：
  1. 港澳地区 → 港澳通行证 + 签注
  2. 台湾地区 → 大陆居民往来台湾通行证
  3. 国际旅行 → 检查护照有效期
  4. 需签证国家 → 签证材料准备
  5. 免签国家 → 确认免签停留期限
"""

from app.rules.rule_helpers import (
    RuleContext,
    days_before_start,
    is_hong_kong_macau,
    is_international,
    is_overseas,
    is_taiwan,
    is_visa_free,
    make_todo,
    needs_visa,
)


def check(ctx: RuleContext) -> list[dict]:
    travel = ctx.travel
    todos: list[dict] = []

    # ======== 1. 港澳通行证 ========
    if is_hong_kong_macau(travel):
        todos.append(make_todo(
            title="确认港澳通行证有效期",
            description=(
                "前往港澳需持有效港澳通行证及有效签注。"
                "请检查通行证是否在有效期内，签注是否有效。"
            ),
            deadline=days_before_start(travel, 30),
            category="document",
            priority="high",
        ))
        todos.append(make_todo(
            title="办理港澳通行证签注",
            description=(
                "如无有效签注，请前往出入境管理部门办理。"
                "个人游签注（G签）通常 5-10 个工作日出签。"
            ),
            deadline=days_before_start(travel, 20),
            category="document",
            priority="high",
        ))

    # ======== 2. 台湾通行证 ========
    if is_taiwan(travel):
        todos.append(make_todo(
            title="确认大陆居民往来台湾通行证",
            description=(
                "前往台湾需持有效的大陆居民往来台湾通行证"
                "及有效签注（个人游 G 签或团队游 L 签）。"
            ),
            deadline=days_before_start(travel, 30),
            category="document",
            priority="high",
        ))
        todos.append(make_todo(
            title="确认入台相关材料",
            description=(
                "根据行程确认是否需要入台证。"
                "自由行需提前申请入台证，约 3-5 个工作日。"
            ),
            deadline=days_before_start(travel, 25),
            category="document",
            priority="high",
        ))

    # ======== 3. 国际旅行 - 护照 ========
    if is_overseas(travel):
        todos.append(make_todo(
            title="检查护照有效期",
            description=(
                "大多数国家要求护照有效期在回国日期后"
                "至少 6 个月以上。请检查护照到期日。"
                "如不足 6 个月，建议尽快更换。"
            ),
            deadline=days_before_start(travel, 60),
            category="document",
            priority="high",
        ))

    # ======== 4. 需签证国家 ========
    if needs_visa(travel):
        todos.append(make_todo(
            title="查询签证要求",
            description=(
                f"目的地 {travel.destination} 需要提前办理签证。"
                "请查阅大使馆/领事馆官网，确认所需材料"
                "和办理周期。"
            ),
            deadline=days_before_start(travel, 90),
            category="visa",
            priority="high",
        ))
        todos.append(make_todo(
            title="准备签证材料",
            description=(
                "准备：护照原件、照片、在职证明、银行流水、"
                "行程单、住宿预订确认等（具体以使馆要求为准）。"
            ),
            deadline=days_before_start(travel, 75),
            category="visa",
            priority="high",
        ))
        todos.append(make_todo(
            title="提交签证申请",
            description=(
                "将材料提交至签证中心或使馆。"
                "建议预留充足时间，避免临近出发仍未出签。"
            ),
            deadline=days_before_start(travel, 60),
            category="visa",
            priority="high",
        ))

    # ======== 5. 免签国家 ========
    if is_visa_free(travel) and not needs_visa(travel):
        todos.append(make_todo(
            title="确认免签停留期限",
            description=(
                f"目的地 {travel.destination} 对中国护照免签或落地签。"
                "请确认免签停留天数，确保行程不超期。"
                "需准备：返程机票、酒店预订、 sufficient funds。"
            ),
            deadline=days_before_start(travel, 15),
            category="visa",
            priority="medium",
        ))

    return todos
