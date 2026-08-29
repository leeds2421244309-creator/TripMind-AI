# 调 Prompt Builder。

# 调 Qwen Client。

# 解析 JSON。

# 返回统一格式。

from app.clients.qwen_client import chat_with_qwen
from app.services.prompt_builder import build_travel_prompt


def generate_travel_plan(
    destination: str,
    days: int,
    budget: int,
    people: int,
    preferences: list[str]
):

    # 1. 生成 Prompt
    prompt = build_travel_prompt(
        destination=destination,
        days=days,
        budget=budget,
        people=people,
        preferences=preferences
    )


    # 2. 调用 Qwen
    result = chat_with_qwen(prompt)


    # 3. 返回 AI结果
    return result