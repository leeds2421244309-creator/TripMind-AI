from app.db.database import engine
from app.db.base import Base


# 导入所有 Model（一定要导入，否则不会创建）
from app.models.user import User
from app.models.travel import Travel
from app.models.budget_item import BudgetItem


def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建完成！")

if __name__ == "__main__":
    init_db()