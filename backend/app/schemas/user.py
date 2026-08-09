from pydantic import BaseModel


class UserCreate(BaseModel):

    username: str

    email: str

    password: str


# 登录请求
class UserLogin(BaseModel):

    username: str

    password: str


# Token返回
class Token(BaseModel):

    access_token: str

    token_type: str