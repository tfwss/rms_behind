-- 说明：运行脚本前需启用 FILESTREAM 并创建数据库/文件组
-- Enable FILESTREAM and create database/filegroup before running this script.

-- 如果不存在 report_files 表则创建
IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'report_files')
-- 开始条件块
BEGIN
    -- 创建 FILETABLE 表
    CREATE TABLE report_files AS FILETABLE
    -- 指定 FILETABLE 配置
    WITH
    -- 配置参数块开始
    (
        -- FILETABLE 目录名称
        FILETABLE_DIRECTORY = 'report_files',
        -- 文件名排序规则
        FILETABLE_COLLATE_FILENAME = database_default
    -- 配置参数块结束
    );
-- 结束条件块
END;
-- 批处理分隔符
GO
