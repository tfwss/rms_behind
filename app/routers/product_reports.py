# 模块级文档字符串：产品报表提交的 API 路由
"""API routes for product report submissions."""

# 导入日期类型
from datetime import date
# 导入可选类型注解
from typing import Optional

# 导入 FastAPI 路由与表单/文件工具
from fastapi import APIRouter, Depends, File, Form, UploadFile
# 导入 SQLAlchemy 会话类型
from sqlalchemy.orm import Session

# 导入数据库会话依赖
from app.core.database import get_db
# 导入产品报表模型
from app.models.product_report_models import ProductFullReport
# 导入响应 schema
from app.schemas.product_report_schemas import ProductFullReportResponse
# 导入文件存储服务
from app.services.product_report_storage import save_product_report_file


# 创建路由器并设置前缀与标签
router = APIRouter(prefix="/product-reports", tags=["product-reports"])


# 定义提交产品完整报表的 POST 接口
@router.post("/full-report", response_model=ProductFullReportResponse)
def submit_full_report(
    # 可选 token
    token: Optional[str] = Form(default=None),
    # 操作码
    operationcode: int = Form(default=45),
    # 报表编号
    rp_number: str = Form(...),
    # 创建人
    creator: str = Form(...),
    # 产品名称
    product_name: str = Form(...),
    # 产品编码
    product_code: str = Form(...),
    # 创建时间
    creatorTime: date = Form(...),
    # 复核人
    verification_man: str = Form(...),
    # 项目负责人
    pro_leader: str = Form(...),
    # 配方负责人
    recipe_leader: str = Form(...),
    # 会议报告附件（可选）
    meetingReport: Optional[UploadFile] = File(default=None),
    # 数据库会话依赖
    db: Session = Depends(get_db),
):
    # 函数文档：保存产品完整报表及其附件
    """Persist a product full report and its optional attachment."""
    # 保存上传文件到文件系统
    file_path = save_product_report_file(product_code, meetingReport)
    # 创建报表 ORM 对象
    report = ProductFullReport(
        # token 字段
        token=token,
        # 操作码字段
        operationcode=operationcode,
        # 报表编号字段
        rp_number=rp_number,
        # 创建人字段
        creator=creator,
        # 产品名称字段
        product_name=product_name,
        # 产品编码字段
        product_code=product_code,
        # 创建时间字段
        creator_time=creatorTime,
        # 复核人字段
        verification_man=verification_man,
        # 项目负责人字段
        pro_leader=pro_leader,
        # 配方负责人字段
        recipe_leader=recipe_leader,
        # 附件路径字段
        file_name=file_path,
        # 删除标记
        is_delete=0,
    )

    # 尝试提交事务
    try:
        # 添加报表对象
        db.add(report)
        # 提交事务
        db.commit()
        # 返回成功响应
        return ProductFullReportResponse(operationcode=45, state="success")
    # 捕获异常并回滚
    except Exception:
        # 回滚事务
        db.rollback()
        # 返回失败响应
        return ProductFullReportResponse(operationcode=45, state="fail")
