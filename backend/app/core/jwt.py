from datetime import datetime, timedelta, timezone

from jose import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User





# JWT密钥
SECRET_KEY = "tripmind-ai-secret-key"


# 加密算法
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

# Token有效时间
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )


    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id = payload.get("sub")


        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token无效"
            )


    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token解析失败"
        )


    user = db.query(
        User
    ).filter(
        User.id == int(user_id)
    ).first()


    if user is None:

        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )


    return user