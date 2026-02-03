# 模块级文档字符串：报表创建与查询的 API 路由
"""API routes for creating and retrieving reports."""

# 导入 JSON 处理模块
import json
# 导入类型注解
from typing import List, Optional

# 导入 FastAPI 路由与表单/文件工具
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
# 导入 SQLAlchemy 会话类型
from sqlalchemy.orm import Session

# 导入数据库会话依赖
from app.core.database import get_db
# 导入报表相关模型
from app.models.report_models import Report, ReportAttachment, ReportField, ReportFieldValue
# 导入响应 schema
from app.schemas.report_schemas import ReportRead
# 导入 FILETABLE 存储服务
from app.services.storage_service import FileTableStorage

# 创建路由器并设置前缀与标签
router = APIRouter(prefix="/reports", tags=["reports"])


# 定义创建报表的 POST 接口
@router.post("", response_model=ReportRead)
def create_report(
    # 报表类型 ID（表单字段）
    report_type_id: int = Form(...),
    # 报表标题（表单字段）
    title: str = Form(...),
    # 字段值 JSON（表单字段）
    values: str = Form("{}"),
    # 附件文件列表（可选）
    files: Optional[List[UploadFile]] = File(default=None),
    # 数据库会话依赖
    db: Session = Depends(get_db),
):
    # 函数文档：创建报表并可附带附件
    """Create a report with field values and optional attachments."""
    # 尝试解析字段值 JSON
    try:
        values_data = json.loads(values)
    # 处理 JSON 解析错误
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON for values") from exc

    # 先创建报表行以获得 ID
    report = Report(report_type_id=report_type_id, title=title)
    # 添加到数据库会话
    db.add(report)
    # 立即写入以生成主键
    db.flush()

    # 构建字段名称到字段定义的映射
    field_map = {
        # 键为字段名称，值为字段对象
        field.name: field
        # 遍历查询到的字段列表
        for field in db.query(ReportField)
        # 过滤报表类型 ID
        .filter(ReportField.report_type_id == report_type_id)
        # 取出全部结果
        .all()
    }

    # 遍历提交的字段值并保存
    for field_name, value in values_data.items():
        # 获取字段定义
        field = field_map.get(field_name)
        # 如果字段不存在则跳过
        if not field:
            continue
        # 添加字段值记录
        db.add(
            ReportFieldValue(
                # 关联报表 ID
                report_id=report.id,
                # 关联字段 ID
                field_id=field.id,
                # 字段值转字符串
                value=str(value) if value is not None else None,
            )
        )

    # 保存附件到 FILETABLE 并持久化元数据
    storage = FileTableStorage()
    # 保存文件并返回元数据列表
    attachments = storage.save_files(report.id, files or [])
    # 遍历附件元数据并保存到数据库
    for attachment in attachments:
        db.add(
            ReportAttachment(
                # 关联报表 ID
                report_id=report.id,
                # 保存文件名
                filename=attachment["filename"],
                # 保存存储路径
                storage_path=attachment["storage_path"],
                # 保存内容类型
                content_type=attachment["content_type"],
            )
        )

    # 提交事务并返回响应
    db.commit()
    # 刷新报表对象
    db.refresh(report)
    # 转换为响应 schema
    return _report_to_read(report)


# 定义获取单个报表的 GET 接口
@router.get("/{report_id}", response_model=ReportRead)
def get_report(report_id: int, db: Session = Depends(get_db)):
    # 函数文档：按 ID 获取报表
    """Fetch a single report by ID."""
    # 查询报表
    report = db.query(Report).filter(Report.id == report_id).first()
    # 如果不存在则抛出 404
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    # 返回转换后的响应
    return _report_to_read(report)


# 定义获取报表列表的 GET 接口
@router.get("", response_model=list[ReportRead])
def list_reports(db: Session = Depends(get_db)):
    # 函数文档：列出所有报表
    """List all reports."""
    # 返回所有报表的响应列表
    return [_report_to_read(report) for report in db.query(Report).all()]


# 将 ORM 报表对象转换为响应 schema
def _report_to_read(report: Report) -> ReportRead:
    # 函数文档：ORM 对象转 ReportRead
    """Convert a Report ORM object into a ReportRead schema."""
    # 构建字段名到值的映射
    values = {value.field.name: value.value for value in report.values}
    # 返回 ReportRead 实例
    return ReportRead(
        # 报表 ID
        id=report.id,
        # 报表类型 ID
        report_type_id=report.report_type_id,
        # 报表标题
        title=report.title,
        # 创建时间
        created_at=report.created_at,
        # 字段值
        values=values,
        # 附件列表
        attachments=report.attachments,
    )
