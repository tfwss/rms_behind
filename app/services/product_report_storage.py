# 模块级文档字符串：产品报表附件的文件系统存储
"""Filesystem storage helpers for product report attachments."""

# 导入操作系统路径工具
import os
# 导入文件复制工具
import shutil
# 导入类型注解
from typing import Optional

# 导入 FastAPI 上传文件类型
from fastapi import UploadFile

# 导入配置
from app.core.config import settings


# 保存产品报表附件到本地
def save_product_report_file(
    # 产品编码
    product_code: str,
    # 会议报告文件（可选）
    meeting_report: Optional[UploadFile],
) -> Optional[str]:
    # 函数文档：持久化上传的会议报告
    """Persist an uploaded meeting report to the configured storage directory."""
    # 如果没有上传文件则返回 None
    if not meeting_report:
        return None

    # 规范化文件名并限定到产品编码目录
    safe_name = os.path.basename(meeting_report.filename)
    # 构建目标目录路径
    target_dir = os.path.join(settings.product_report_storage_dir, product_code)
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    # 构建目标文件路径
    target_path = os.path.join(target_dir, safe_name)

    # 将上传内容写入磁盘
    with open(target_path, "wb") as destination:
        # 复制文件流到目标文件
        shutil.copyfileobj(meeting_report.file, destination)

    # 返回保存后的路径
    return target_path
