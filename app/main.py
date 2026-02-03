# 模块级文档字符串：FastAPI 应用入口
"""FastAPI application entrypoint."""

# 导入 FastAPI 框架主类
from fastapi import FastAPI

# 导入应用配置对象
from app.core.config import settings
# 导入数据库 Base 与 engine 以便建表
from app.core.database import Base, engine
# 导入模型模块以确保模型被注册（避免未加载）
from app.models import product_report_models, report_models  # noqa: F401
# 导入路由模块
from app.routers import product_reports, report_types, reports


# 定义创建 FastAPI 应用的工厂函数
def create_app() -> FastAPI:
    # 函数文档：创建并配置 FastAPI 应用
    """Create and configure the FastAPI application."""
    # 创建 FastAPI 应用实例，并设置标题与调试模式
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    # 启动时确保数据库表已创建
    Base.metadata.create_all(bind=engine)

    # 注册 API 路由：报表类型
    app.include_router(report_types.router)
    # 注册 API 路由：报表
    app.include_router(reports.router)
    # 注册 API 路由：产品完整报表
    app.include_router(product_reports.router)

    # 返回构建好的应用实例
    return app


# ASGI 应用实例（给 uvicorn/gunicorn 使用）
app = create_app()
