# 模块级文档字符串：数据库引擎、会话工厂与依赖工具
"""Database engine, session factory, and dependency helpers."""

# 导入 SQLAlchemy 引擎创建函数
from sqlalchemy import create_engine
# 导入声明式基类与会话工厂
from sqlalchemy.orm import declarative_base, sessionmaker

# 导入配置设置
from app.core.config import settings


# 创建 SQLAlchemy 引擎
engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
# 创建请求级数据库会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 ORM 模型的声明式基类
Base = declarative_base()


# 提供数据库会话的依赖函数
def get_db():
    # 函数文档：生成会话并在使用后关闭
    """Yield a database session and ensure it is closed after use."""
    # 创建会话实例
    db = SessionLocal()
    # 尝试把会话交给调用者
    try:
        # 以生成器形式返回会话
        yield db
    # 最终确保会话关闭
    finally:
        # 关闭数据库会话
        db.close()
