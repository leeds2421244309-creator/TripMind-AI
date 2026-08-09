from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserLogin,
    Token
)
from app.core.security import (
    get_password_hash,
    verify_password
    )

from app.core.jwt import (
    create_access_token,
    get_current_user
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Auth"]
)

# 注册
@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
        

    )


    db.add(new_user)

    db.commit()

    db.refresh(new_user)


    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }


# 登录
@router.post(
    "/login",
    response_model=Token
)
def login(
    user: OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
):

    # 查询用户

    db_user = db.query( # 相当于 SQL 语句：SELECT * FROM users
        User
    ).filter( # 类似于 SQL 中的 WHERE 子句。
        User.username == user.username
    ).first() # 只取符合条件的第一条记录


    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="用户名不存在"
        )


    # 验证密码

    if not verify_password(
        user.password,
        db_user.password_hash
    ):

        raise HTTPException(
            status_code=400,
            detail="密码错误"
        )


    # 生成JWT

    access_token = create_access_token(
        {
            "sub": str(db_user.id)
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# 获取当前登录用户信息
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }