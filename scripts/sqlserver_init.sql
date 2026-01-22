-- Enable FILESTREAM and create database/filegroup before running this script.

IF NOT EXISTS (SELECT 1 FROM sys.tables WHERE name = 'report_files')
BEGIN
    CREATE TABLE report_files AS FILETABLE
    WITH
    (
        FILETABLE_DIRECTORY = 'report_files',
        FILETABLE_COLLATE_FILENAME = database_default
    );
END;
GO
