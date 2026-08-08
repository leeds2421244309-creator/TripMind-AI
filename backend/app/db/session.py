# 以后 API：

# def get_plans(db):

# 需要数据库连接。

# 每次请求：

# 用户请求
#  |
# 创建Session
#  |
# 查询MySQL
#  |
# 返回
#  |
# 关闭Session

# 类似：

# 打开数据库连接
# 使用
# 关闭

from sqlalchemy.orm import sessionmaker

from app.db.database import engine

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
