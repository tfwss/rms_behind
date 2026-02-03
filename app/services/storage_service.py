# 模块级文档字符串：SQL Server FILETABLE 附件存储服务
"""Services for storing report attachments in SQL Server FILETABLE."""

# 导入操作系统路径工具
import os
# 导入类型注解
from typing import Iterable, List

# 导入 ODBC 驱动
import pyodbc
# 导入 FastAPI 上传文件类型
from fastapi import UploadFile

# 导入配置
from app.core.config import settings


# FILETABLE 存储服务类
class FileTableStorage:
    # 类文档：封装 FILETABLE 持久化逻辑
    """Encapsulates FILETABLE persistence logic."""

    # 初始化方法
    def __init__(self, connection_string: str | None = None) -> None:
        # 构造函数文档：允许覆盖 ODBC 连接字符串
        """Initialize with an optional override for the ODBC connection string."""
        # 优先使用传入连接字符串，否则使用配置默认值
        self.connection_string = connection_string or settings.odbc_connection_string

    # 获取原始 ODBC 连接
    def _get_raw_connection(self) -> pyodbc.Connection:
        # 方法文档：开启自动提交的 ODBC 连接
        """Open a raw pyodbc connection with autocommit enabled."""
        # 返回新的 ODBC 连接
        return pyodbc.connect(self.connection_string, autocommit=True)

    # 保存附件到 FILETABLE
    def save_files(self, report_id: int, files: Iterable[UploadFile]) -> List[dict]:
        # 方法文档：保存文件到 SQL Server FILETABLE
        """
        Save files into SQL Server FILETABLE.

        You need to:
        1. Enable FILESTREAM on SQL Server.
        2. Create FILETABLE (see scripts/sqlserver_init.sql).
        3. Grant INSERT/UPDATE permissions.
        """
        # 如果没有附件则返回空列表
        if not files:
            return []

        # 准备保存结果列表
        saved: List[dict] = []
        # 打开 ODBC 连接并自动关闭
        with self._get_raw_connection() as connection:
            # 获取数据库游标
            cursor = connection.cursor()
            # 遍历上传的文件
            for upload in files:
                # 规范化文件名并读取内容
                filename = os.path.basename(upload.filename)
                # 读取文件二进制内容
                content = upload.file.read()

                # 向 FILETABLE 插入二进制并返回路径
                cursor.execute(
                    # SQL 语句：插入并输出路径
                    """
                    INSERT INTO report_files (name, file_stream)
                    OUTPUT INSERTED.path_locator
                    VALUES (?, ?)
                    """,
                    # 参数：文件名
                    filename,
                    # 参数：二进制内容
                    pyodbc.Binary(content),
                )
                # 读取插入后的结果行
                row = cursor.fetchone()
                # 获取存储路径
                storage_path = row[0]
                # 构建 ORM 需要的元数据
                saved.append(
                    {
                        # 保存文件名
                        "filename": filename,
                        # 保存存储路径
                        "storage_path": storage_path,
                        # 保存内容类型
                        "content_type": upload.content_type,
                        # 保存报表 ID
                        "report_id": report_id,
                    }
                )

        # 返回保存结果列表
        return saved
