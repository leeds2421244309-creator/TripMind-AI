from fastapi import (
    APIRouter,
    Depends
)

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.clients.qwen_client import chat_with_qwen

from app.models.user import User

from app.core.jwt import get_current_user


router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest,
    current_user: User = Depends(get_current_user)
):

    print(
        "当前用户:",
        current_user.username
    )


    prompt = f"""
你是 TripMind AI，
一个专业的旅行助手。

请使用中文回答用户问题。

用户问题：

{request.message}

要求：

1. 回答简洁准确。
2. 给出实际旅行建议。
3. 如果涉及旅行信息，考虑预算和交通。
"""

    answer = chat_with_qwen(prompt)

    return ChatResponse(
        answer=answer
    )