# 导入路由模块以便集中暴露
from app.routers import product_reports, report_types, reports

# 指定可导出的模块列表
__all__ = ["product_reports", "report_types", "reports"]
