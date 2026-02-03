# 模块级文档字符串：报表类型与字段的 API 路由
"""API routes for report types and fields."""

# 导入 FastAPI 路由与依赖工具
from fastapi import APIRouter, Depends, HTTPException
# 导入 SQLAlchemy 会话类型
from sqlalchemy.orm import Session

# 导入数据库会话依赖
from app.core.database import get_db
# 导入报表类型与字段模型
from app.models.report_models import ReportField, ReportType
# 导入请求与响应的 schema
from app.schemas.report_schemas import (
    # 创建字段请求体
    ReportFieldCreate,
    # 字段返回体
    ReportFieldRead,
    # 创建报表类型请求体
    ReportTypeCreate,
    # 报表类型返回体
    ReportTypeRead,
)

# 创建路由器并设置前缀与标签
router = APIRouter(prefix="/report-types", tags=["report-types"])


# 定义创建报表类型的 POST 接口
@router.post("", response_model=ReportTypeRead)
def create_report_type(payload: ReportTypeCreate, db: Session = Depends(get_db)):
    # 函数文档：创建新的报表类型
    """Create a new report type."""
    # 构建报表类型对象
    report_type = ReportType(name=payload.name, description=payload.description)
    # 添加到数据库会话
    db.add(report_type)
    # 提交事务
    db.commit()
    # 刷新对象以获取数据库状态
    db.refresh(report_type)
    # 返回创建结果
    return report_type


# 定义获取报表类型列表的 GET 接口
@router.get("", response_model=list[ReportTypeRead])
def list_report_types(db: Session = Depends(get_db)):
    # 函数文档：列出所有报表类型
    """List all report types."""
    # 查询并返回全部报表类型
    return db.query(ReportType).all()


# 定义在报表类型下创建字段的 POST 接口
@router.post("/{report_type_id}/fields", response_model=ReportFieldRead)
def create_report_field(
    # 路径参数：报表类型 ID
    report_type_id: int,
    # 请求体：字段信息
    payload: ReportFieldCreate,
    # 数据库会话依赖
    db: Session = Depends(get_db),
):
    # 函数文档：创建报表字段
    """Create a field under a report type."""
    # 查询报表类型是否存在
    report_type = db.query(ReportType).filter(ReportType.id == report_type_id).first()
    # 如果不存在则抛出 404
    if not report_type:
        raise HTTPException(status_code=404, detail="Report type not found")

    # 持久化新的字段定义
    field = ReportField(
        # 关联报表类型 ID
        report_type_id=report_type_id,
        # 字段名称
        name=payload.name,
        # 字段标签
        label=payload.label,
        # 字段类型
        field_type=payload.field_type,
        # 是否必填
        required=payload.required,
    )
    # 添加到数据库会话
    db.add(field)
    # 提交事务
    db.commit()
    # 刷新对象
    db.refresh(field)
    # 返回字段信息
    return field


# 定义获取报表字段列表的 GET 接口
@router.get("/{report_type_id}/fields", response_model=list[ReportFieldRead])
def list_report_fields(report_type_id: int, db: Session = Depends(get_db)):
    # 函数文档：列出某个报表类型的字段
    """List all fields for a given report type."""
    # 返回对应报表类型的字段列表
    return (
        # 查询报表字段
        db.query(ReportField)
        # 过滤报表类型 ID
        .filter(ReportField.report_type_id == report_type_id)
        # 返回全部结果
        .all()
    )
