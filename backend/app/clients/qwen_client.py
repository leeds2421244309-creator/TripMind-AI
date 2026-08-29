# 只负责通信
# 输入 Prompt。
# 请求 API。
# 返回 AI 内容。

from openai import OpenAI

from app.core.config import settings

from app.utils.json_parser import parse_json_response

import json

client = OpenAI(
    api_key=settings.QWEN_API_KEY,
    base_url=settings.QWEN_BASE_URL
)


def chat_with_qwen(prompt: str):

    response = client.chat.completions.create(
        model=settings.QWEN_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content
    #强制判定json
    return parse_json_response(content)

    # return response.choices[0].message.content
