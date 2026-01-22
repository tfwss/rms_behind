# rms_behind

轻量级报告管理系统后端（FastAPI + SQL Server）。

## 目录结构
```
app/
  core/          # 配置与数据库连接
  models/        # SQLAlchemy 模型
  routers/       # API 路由
  schemas/       # Pydantic 模型
  services/      # 文件存储等服务
scripts/         # SQL Server 初始化脚本
```

## 主要功能
- 报告类型/字段可配置（建表、建字段）。
- 支持 5 种报告类型（可通过 API 配置，示例见下）。
- 支持多附件上传，附件保存到 SQL Server FILETABLE。

## 启动
```bash
uvicorn app.main:app --reload
```

## 报告类型示例
建议先创建 5 种报告类型：
- 设备验收报告
- 设备工艺报告
- 产品工艺报告
- 产品全功能报告
- 会议纪要

### 创建报告类型
```bash
curl -X POST http://localhost:8000/report-types \
  -H "Content-Type: application/json" \
  -d '{"name": "设备验收报告", "description": "设备验收"}'
```

### 创建报告字段
```bash
curl -X POST http://localhost:8000/report-types/1/fields \
  -H "Content-Type: application/json" \
  -d '{"name": "device_model", "label": "设备型号", "field_type": "text", "required": true}'
```

### 创建报告（表单 + 多附件）
```bash
curl -X POST http://localhost:8000/reports \
  -F "report_type_id=1" \
  -F "title=设备验收-2024" \
  -F 'values={"device_model":"ABC-01","owner":"张三"}' \
  -F "files=@/path/to/file1.pdf" \
  -F "files=@/path/to/file2.docx"
```

## SQL Server FILETABLE
请先启用 FILESTREAM，并执行 `scripts/sqlserver_init.sql` 创建 FILETABLE。

> 说明：示例使用 `report_files` 作为 FILETABLE，
> `app/services/storage_service.py` 中 `save_files` 会写入该表。
