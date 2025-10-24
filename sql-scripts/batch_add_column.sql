-- ==========================================
-- MySQL批量添加字段脚本
-- 功能：检查指定前缀的表是否缺少某个字段，生成批量添加字段的SQL语句
-- ==========================================

-- 设置变量：根据需要修改以下变量
SET @database_name = 'your_database';           -- 数据库名
SET @table_prefix = 'tbl_';                     -- 表前缀，如：tbl_、sys_、t_等
SET @column_name = 'updated_at';                -- 要添加的字段名
SET @column_type = 'DATETIME';                  -- 字段类型
SET @column_length = '';                        -- 字段长度（VARCHAR需要，如'100'，数值型和日期型留空''）
SET @column_default = 'CURRENT_TIMESTAMP';      -- 默认值（可选，如：'CURRENT_TIMESTAMP'、'0'、NULL等）
SET @column_nullable = 'NOT NULL';              -- 是否允许为空：'NOT NULL' 或 'NULL'
SET @column_comment = '更新时间';                -- 字段注释
SET @add_after_column = 'created_at';           -- 添加在哪个字段之后（可选，留空''则添加到最后）

-- ==========================================
-- 第一步：查询缺少该字段的表
-- ==========================================
SELECT
    CONCAT('-- 表 ', t.TABLE_NAME, ' 缺少字段 ', @column_name) AS '检查结果'
FROM
    information_schema.TABLES t
WHERE
    t.TABLE_SCHEMA = @database_name
    AND t.TABLE_NAME LIKE CONCAT(@table_prefix, '%')
    AND NOT EXISTS (
        SELECT 1
        FROM information_schema.COLUMNS c
        WHERE c.TABLE_SCHEMA = @database_name
          AND c.TABLE_NAME = t.TABLE_NAME
          AND c.COLUMN_NAME = @column_name
    )
ORDER BY
    t.TABLE_NAME;

-- ==========================================
-- 第二步：生成批量添加字段的ALTER TABLE语句
-- ==========================================
SELECT
    CONCAT(
        'ALTER TABLE `', t.TABLE_NAME, '` ADD COLUMN `', @column_name, '` ',
        @column_type,
        CASE
            WHEN @column_length != '' THEN CONCAT('(', @column_length, ')')
            ELSE ''
        END,
        ' ',
        @column_nullable,
        CASE
            WHEN @column_default IS NOT NULL AND @column_default != ''
            THEN CONCAT(' DEFAULT ', @column_default)
            ELSE ''
        END,
        CASE
            WHEN @column_comment IS NOT NULL AND @column_comment != ''
            THEN CONCAT(' COMMENT ''', @column_comment, '''')
            ELSE ''
        END,
        CASE
            WHEN @add_after_column IS NOT NULL AND @add_after_column != ''
            THEN CONCAT(' AFTER `', @add_after_column, '`')
            ELSE ''
        END,
        ';'
    ) AS 'ALTER_TABLE语句'
FROM
    information_schema.TABLES t
WHERE
    t.TABLE_SCHEMA = @database_name
    AND t.TABLE_NAME LIKE CONCAT(@table_prefix, '%')
    AND NOT EXISTS (
        SELECT 1
        FROM information_schema.COLUMNS c
        WHERE c.TABLE_SCHEMA = @database_name
          AND c.TABLE_NAME = t.TABLE_NAME
          AND c.COLUMN_NAME = @column_name
    )
ORDER BY
    t.TABLE_NAME;

-- ==========================================
-- 使用说明
-- ==========================================
-- 1. 修改上面的变量设置（@database_name、@table_prefix等）
-- 2. 执行第一步查询，查看哪些表缺少该字段
-- 3. 执行第二步查询，生成ALTER TABLE语句
-- 4. 复制生成的ALTER TABLE语句到新的查询窗口执行

-- ==========================================
-- 常用示例
-- ==========================================

-- 示例1：添加VARCHAR类型字段
/*
SET @database_name = 'mydb';
SET @table_prefix = 'user_';
SET @column_name = 'phone';
SET @column_type = 'VARCHAR';
SET @column_length = '20';
SET @column_default = NULL;
SET @column_nullable = 'NULL';
SET @column_comment = '手机号';
SET @add_after_column = 'email';
*/

-- 示例2：添加INT类型字段
/*
SET @database_name = 'mydb';
SET @table_prefix = 'order_';
SET @column_name = 'status';
SET @column_type = 'INT';
SET @column_length = '';
SET @column_default = '0';
SET @column_nullable = 'NOT NULL';
SET @column_comment = '订单状态';
SET @add_after_column = '';
*/

-- 示例3：添加DECIMAL类型字段
/*
SET @database_name = 'mydb';
SET @table_prefix = 'product_';
SET @column_name = 'price';
SET @column_type = 'DECIMAL';
SET @column_length = '10,2';
SET @column_default = '0.00';
SET @column_nullable = 'NOT NULL';
SET @column_comment = '价格';
SET @add_after_column = 'name';
*/

-- 示例4：添加DATETIME类型字段
/*
SET @database_name = 'mydb';
SET @table_prefix = 't_';
SET @column_name = 'created_at';
SET @column_type = 'DATETIME';
SET @column_length = '';
SET @column_default = 'CURRENT_TIMESTAMP';
SET @column_nullable = 'NOT NULL';
SET @column_comment = '创建时间';
SET @add_after_column = '';
*/

-- 示例5：添加TEXT类型字段
/*
SET @database_name = 'mydb';
SET @table_prefix = 'article_';
SET @column_name = 'content';
SET @column_type = 'TEXT';
SET @column_length = '';
SET @column_default = NULL;
SET @column_nullable = 'NULL';
SET @column_comment = '文章内容';
SET @add_after_column = 'title';
*/
