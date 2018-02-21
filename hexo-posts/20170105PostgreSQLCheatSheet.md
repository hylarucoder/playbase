title: PostgreSQL CheatSheet
date: 2017-01-05 20:48:31
categories:
 - 后台组件
tags:
 - PostgreSQL
 - CheatSheet
 - 数据分析

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 PostgreSQL 相关和命令。

PostGIS 相关的资料参考文章 [Geo Processing With Python](/2016/10/05/UbuntuCheatsheet/)

 - 安装与基本配置
 - PostgreSQL 配套工具
 - PostgreSQL SQL 常用代码片段
 - Python Driver : psycopg2 , 与两个 ORM ( Django ORM / SQLAlchemy )

不定期更新。

<!-- more -->

## 0x01 安装，配置，基本 shell 命令

### 安装

### 配置

### 基本 Shell 命令

```
# 开启关闭
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log stop
pg_ctl -D /usr/local/var/postgres start
pg_ctl -D /usr/local/var/postgres stop -s -m fast
```

### 数据的导入导出
```bash
pg_dump -C -Fp -f dump.sql -U twocucao QCS -h 192.168.2.175
pg_dump -C -Fp -f 20160602-150144-dump.sql -U twocucao QCS --column-inserts --data-only --table=users_table -h 192.168.2.175
# 插入数据
psql -U twocucao -d QCS -a -f insert_doc_ids.sql -h 192.168.2.175
pg_restore --verbose --clean --no-acl --no-owner -h localhost example.dump
```

## 0x02 PostgreSQL 配套工具

 - JetBrain 的 Datagrip 作为 编写大段 SQL 语句的 IDE
 - 通过网络或者 Dash 查看文档
 - PostgreSQL 官方自带工具

## 0x03 PostgreSQL SQL 常用代码

### 3.1 PostgreSQL 相关

```sql
-- 强行中断连接到此数据库的 session
SELECT
    pg_terminate_backend(pid)
FROM
    pg_stat_activity
WHERE
    -- don't kill my own connection!
    pid <> pg_backend_pid()
    -- don't kill the connections to other databases
    AND datname = 'demoweb' ;
```
### 3.2 DCL ( Data Control Languge )

```
-- 创建只读用户
\c demoweb
CREATE ROLE ro_user WITH LOGIN ENCRYPTED PASSWORD 'xxx123456';
GRANT CONNECT ON DATABASE demoweb TO ro_user;
-- This assumes you're actually connected to mydb..
GRANT USAGE ON SCHEMA public TO ro_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ro_user;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO ro_user;

-- 撤销数据库连接 ()
REVOKE CONNECT ON DATABASE demoweb FROM PUBLIC, demoweb;
```

### 3.3 DDL ( Data Definition Language )

CREATE
ALTER
DROP
TRUNCATE
COMMENT
RENAME

### 3.4 DML ( Data Manipulation Languge )

SELECT
INSERT
UPDATE
DELETE
MERGE
CALL
EXPLAIN PLAN
LOCK TABLE

### 3.5 TCL ( Transaction Control Languge )

## 0x04. 常用代码片段

### 4.1. Tips And Hacks

#### Recursive Query

```bash
WITH cte_name(
    CTE_query_definition -- non-recursive term
    UNION [ALL]
    CTE_query_definition -- recursive term
) SELECT * FROM cte_name;
```

### 4.2. 大数据量运算技巧

### 4.3 备份还原技巧

```
# 需要备份的机器
DB_NAME='xxxdb'
DUMP_DB_FILE='latest_dump.sql.gz'
sudo -u postgres pg_dump $DB_NAME | gzip -9 > $DUMP_DB_FILE
TARGET_HOSTNAME='xxx.org'
TARGET_PATH='/webapps/'
scp $DUMP_DB_FILE root@$TARGET_HOSTNAME:/webapps/

# 需要还原的机器
DB_NAME='xxxdb'
DUMP_DB_FILE='latest_dump.sql.gz'
sudo -u postgres dropdb $DB_NAME
sudo -u postgres createdb $DB_NAME
gunzip < $DUMP_DB_FILE | sudo -u postgres psql $DB_NAME
```

## 0x05. 并发优化技巧

> 优化技巧请参考我关于 MySQL 的一片文章。

### 5.1 ACID

- Atomicity     : 行不行，给个准话
- Consistency   : 完成时候，数据保持一致（多版本并发控制）
- Isolation     : 事务与事务之间是隔离的。即一事务无法查看另一个事务正在修改的数据（默认，如果不默认这玩意，则隔离程度是可以设置的）
- Durablity     : 就是存下来了。

#### 多版本并发控制模型

- Each query sees only transactions completed before it started
- On query start, PostgreSQL records:
  - the transaction counter
  - all transaction id’s that are in-process
- In a multi-statement transaction, a transaction’s own previous queries are also visible
- The above assumes the default read committed isolation level

使用 MVCC 多版本并发控制比锁定模型的主要优点是在 MVCC 里， 对检索（读）数据的锁要求与写数据的锁要求不冲突， 所以读不会阻塞写，而写也从不阻塞读。
在数据库里也有表和行级别的锁定机制， 用于给那些无法轻松接受 MVCC 行为的应用。 不过，恰当地使用 MVCC 总会提供比锁更好地性能。

### 5.2 DDL 事务

DDL 可以多条放在一起，然后直接 DDL, 据说可以在 sharding 时候用....

### 5.3 事务使用

```sql
begin;
-- insert_somethings;
savepoint my_savepoint01;
-- wrong ops
rollback to my_savepoint01;
commit;
```

### 5.4 事务隔离级别

- READ UNCOMMITED
- READ COMMITED
- REPEATABLE READ
- SEARLIZABLE

- 脏读          :  和程序的并发一致 默认是不可能的。
- 不可重复读    :  一个事物重新读取前面读过的数，但是发现被改过了。能读原来则是可重复读。读新的，则是不可重复读。
- 幻读          :  （举一个为赋新词强说愁的例子）比如，先 count 一下，然后依照 count 值遍历 cursor, 结果发现数量发生变化。

读已提交，是默认。在这里，脏读（不会）、不可重复读（可能）、幻读（可能）。

### 5.5 锁机制

- 表级锁模式
- 行级锁模式

### 5.6 死锁

死锁的典型案例就是：

1. 当你找你爸要钱的时候，你爸说，要是你妈给你钱，我就给你钱。
2. 当你找你妈要钱的时候，你妈说，要是你爸给你钱，我就给你钱。

死锁的四个必要条件：

- 互斥条件
- 请求和保持条件
- 不剥夺条件
- 环路等待条件

避免死锁的方式，一般是按照顺序来。

当然，数据库可以自动检测出死锁，但是由于捕获死锁需要一定的代价。可能会导致应用程序过久地持有排他锁。

> 慎用排他锁。

## 0x06. Python Driver : psycopg2 , 与两个 ORM ( Django ORM / SQLAlchemy )

## 0x07. 踩坑集

- 序列问题
