# 模块级文档字符串：应用配置来自环境变量
"""Application configuration backed by environment variables."""

# 导入 Pydantic 字段工具
from pydantic import Field
# 导入 Pydantic Settings 基类与配置字典
from pydantic_settings import BaseSettings, SettingsConfigDict


# 定义应用设置类，继承 BaseSettings
class Settings(BaseSettings):
    # 类文档：带默认值的强类型设置
    """Strongly-typed settings with defaults for the RMS backend."""

    # 配置：读取 .env 文件，使用 UTF-8 编码
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # 应用元数据：FastAPI 标题
    app_name: str = "Report Management System"
    # 是否开启调试
    debug: bool = False

    # 主 SQLAlchemy 连接字符串
    database_url: str = Field(
        # 默认连接字符串分段拼接
        default=(
            "mssql+pyodbc://wangxu:6225112Wx..@localhost:1433/"
            "rms?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
        ),
        # 字段描述：SQL Server 连接字符串
        description="SQL Server connection string",
    )
    # FILETABLE 操作使用的 ODBC 连接字符串
    odbc_connection_string: str = Field(
        # 默认 ODBC 连接字符串分段拼接
        default=(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost,1433;"
            "DATABASE=rms;"
            "UID=wangxu;"
            "PWD=6225112Wx..;"
            "TrustServerCertificate=yes;"
        ),
        # 字段描述：FILETABLE 的 ODBC 连接
        description="ODBC connection string for FILETABLE operations",
    )
    # 产品完整报表附件的本地文件夹路径
    product_report_storage_dir: str = Field(
        # 默认文件路径
        default=r"D:\pdf",
        # 字段描述：附件根目录
        description="Root folder for product full report attachments",
    )


# 创建全局单例设置对象供应用使用
settings = Settings()
