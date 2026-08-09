from passlib.context import CryptContext


pwd_context = CryptContext( #创建了一个密码工具
    schemes=["bcrypt"], #指定bcrypt算法
    deprecated="auto"
)


# 密码加密
def get_password_hash(password: str): #注册时调用

    return pwd_context.hash(password)


# 密码校验
def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )