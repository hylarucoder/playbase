title: MySQL Cheatsheet
date: 2016-09-12 18:41:47
categories:
 - 后台组件
tags:
 - Cheatsheet
 - MySQL
 - 关系型数据库

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 MySQL 相关命令。主要包含：

 - MySQL Shell, 其实就是 SQL 命令。
 - MySQL 配套工具
 - Python API

不定期更新。

<!-- more -->

## 0x01 安装，配置，基本 shell 命令

### 字符编码

> UTF-8 , Please

真的很讨厌那些用 GBK 的程序员啊！

```bash
# 注意，下面的设置 MySQL 是无法保存 emoji 的 /
[mysql]
default-character-set=utf8

[mysqld]
collation-server = utf8_general_ci
init-connect='SET NAMES utf8'
character-set-server = utf8
```

然后在 mysql console 执行：

```bash
show variables like "%character%";show variables like "%collation%";
```

如下即可

## 0x02 MySQL 配套工具

 - JetBrain 的 Datagrip 作为 编写大段 SQL 语句的 IDE
 - 通过网络或者 Dash 查看文档
 - 强烈推荐 mycli 作为正常情况下的 MySQL 命令的替代品。
 - MySQL 官方自带工具

只挑选几个重要的，常用的说一说。

```bash
# 启动 MYSQL

# 常规 mysql
mysql -u username -p password
## 命令的用户名和密码最好与命令合在一起
mysqlshow -uroot -psomepass some_db;
# 导入数据
mysql -u username -p password < filename
# 优雅的导入数据，可以查看进度条的 Hacks
pv -i 1 -p -t -e /Users/twocucao/Codes/update_new_date.sql | mysql -uadmin -p123456 -h 192.168.2.254 --port=3306 some_db
# 导出数据
mysqldump -u username -p password database [tables] > filename
mysqldump database table_bame --where="date_column BETWEEN '2012-07-01 00:00:00' and '2012-12-01 00:00:00'"

# ref : http://dev.mysql.com/doc/refman/5.7/en/mysqldump.html#option_mysqldump_where
```

## 0x03 MySQL 常用代码

```bash
SHOW DATABASES;
CREATE DATABASE database;
USE database;
SHOW TABLES;
DESCRIBE table;
SHOW COLUMN FROM table;
DROP DATEBASE;
```

## 0x04 常用代码片段

### 1. 数据清洗常用脚本

```sql
-- 少量去重
CREATE TABLE everyday_info_temp AS SELECT * FROM  everyday_info GROUP BY id,date,numbers;
-- 大量去重
CREATE TABLE everyday_info_temp AS SELECT * FROM  everyday_info GROUP BY id,date,numbers ORDER BY null;
```
http://stackoverflow.com/questions/16568228/how-to-transpose-mysql-table-rows-into-columns

```
  SELECT @max := MAX(ID)+ 1 FROM ABC;

  PREPARE stmt FROM 'ALTER TABLE ABC AUTO_INCREMENT = ?';
  EXECUTE stmt USING @max;

  DEALLOCATE PREPARE stmt;
```

mysql> delete from shophtml;
Query OK, 117141 rows affected (4 min 2.92 sec)
TRUNCATE shophtml;
### 2. 用户管理常用脚本

```bash
SELECT User FROM mysql.user;
```

### 3. 备份迁移常用脚本

```
#! /bin/bash

TIMESTAMP=$(date +"%F")
BACKUP_DIR="/mnt/$TIMESTAMP"
MYSQL_USER="root"
MYSQL=/usr/bin/mysql
MYSQL_PASSWORD="password"
MYSQLDUMP=/usr/bin/mysqldump
DATABASE="cyjoycity"

mkdir -p "$BACKUP_DIR/mysql"

for t in $($MYSQL -NBA -u $MYSQL_USER -p$MYSQL_PASSWORD -D $DATABASE -e 'show tables')
do
    echo "DUMPING TABLE: $DB.$t"
    $MYSQLDUMP --force --opt --user=$MYSQL_USER -p$MYSQL_PASSWORD $DATABASE $t | gzip > "$BACKUP_DIR/mysql/$t.sql.gz"
done

```

### 4. 性能优化常用脚本

SHOW FULL PROCESSLIST;

### 5. 其他脚本

```sql

# 6. 随机选择 10 组记录
-- 慢速
SELECT * FROM Table_Name ORDER BY RAND() LIMIT 0,10;

-- 快速
SELECT name
  FROM random AS r1 JOIN
       (SELECT CEIL(RAND() *
                     (SELECT MAX(id)
                        FROM random)) AS id)
        AS r2
 WHERE r1.id >= r2.id
 ORDER BY r1.id ASC
 LIMIT 1
```

```sql

# 1. 查询时间
select date_format(create_time, '%Y-%m-%d') as day from table_name
select from_unixtime(create_time, '%Y-%m-%d') as day from table_name

# 2. CASE WHEN 案例
## 2.1 返回同一列多个结果

## 2.2 行列值颠倒

# 3. 替换某字段内容
update table_name set content = REPLACE(content, 'aaa', 'bbb')  where (content like '%aaa%')

# 4. 获取表中某字段包含某字符串的数据
SELECT * FROM `表名` WHERE LOCATE('关键字', 字段名）

# 5. 字符串处理
SELECT SUBSTRING（字段名，1,4) FROM 表名

# 6. 求解数字的连续范围

select min(number) start_range,max(number) end_range
from
(
    select number,rn,number-rn diff from
    (
        select number,@number:=@number+1 rn from test_number,(select @number:=0) as number
    ) b
) c group by diff;

```

## 0x05 性能优化切入点

应用的切入点也比较简单和暴力：

1. 优化应用层面的查询。
2. 优化数据库的 SQL 查询。
3. 优化数据库的存储结构。
4. 优化单个数据库服务器的性能。
5. 遵循『机多运算大』的原则，上几台机器。
6. 更好的机器，即加内存条，上好的 CPU。

优化前三点，则需要理解取数据的客户端从发送 SQL 语句到接受数据之间都发生了什么？流程如下：

1. 开启连接
2. 发送查询给服务器
3. 分析查询
4. 执行查询
5. 传输数据
6. 关闭连接

### 优化应用层面的查询

在同样工作量的情况下不断的减少数据库的连接，将多个动作放在一起使用 TRANSACTION 可以显著提高速度。

1. 对于 OLTP 类型的数据库设计的数据库，一些耗时查询往往是可以在应用层面查询进行优化的，比如在手写代码应用级缓存，借助外部组件 (redis) 应用内缓存。
2. 对于一些有性能要求的场景，不要使用 select * from xxx 这种查询，服务器到客户端传输也是需要时间的，而是要选择需要的字段。
3. 如果有必要，不要在循环内部进行数据库查询，而是直接取出来放在内存中进行运算。学过的算法与数据结构用起来！!

### 优化数据库的 SQL 查询

如同前文所见，到了 SQL 命令这层切入点能够优化的地方只有步骤 4.

对于查找，效率取决于：

1. 取记录数量
2. 搜索到这些记录的时间。

对于插入，执行查询则插入记录和更新索引两个部分，也是插入的瓶颈所在：

1. 插入记录 速度取决于记录数量，记录大小
2. 更新索引 速度取决于索引数量。

对于更新，执行查询则有查找，更新记录和更新索引两个部分，也是更新的瓶颈所在：

1. 查找 需要参考查找
2. 更新记录 速度取决于记录数量，记录大小
3. 更新索引 速度取决于更新索引字段的数量。

对于删除，执行查询则有查找，删除记录和删除索引两个部分，也是删除的瓶颈所在：

1. 查找 需要参考查找
2. 删除记录 速度取决于记录数量，记录大小
3. 更新索引 速度取决于更新索引字段的数量。

#### 查询的优化

#### 索引的代价

> 在计算机这个神奇的世界里面，没有一个算法与数据结构的挑选是没有代价的。便于查询，则不便于插入更新。

有的人把索引比作字典。说字典的索引页面就好像是数据表中的索引。

这个比方很贴切，可以用在索引的比方上，也可以用在索引的代价上。

 - 一个没有索引的页面，即是一个只有页码，编号的字典。当我们查询一个新字的时候，只能从第一页翻到结尾，效率很低。
 - 一个有一个索引的页面，即是一个有页码，编号，拼音索引的字典。当我们查询一个新字的时候，先查询索引，然后从索引查页码，于是很快找到字。当我们**增加 / 删除 / 更新**一个字之后，还需要更新拼音索引。
 - 一个有多个索引的页面，即是一个有页码，编号，拼音索引和部首索引以及其他索引的字典。当我们**增加 / 删除 / 更新**一个字之后，还需要更新拼音索引，部首索引等等索引。

> **计算机世界就是这样，没有完美的算法，也没有完美的模型。**

### 数据存储结构

### 硬件优化

留空，这个可能比较接近运维或者 DBA 的工作

### 配置优化

留空，这个可能比较接近运维或者 DBA 的工作

## 0x06 常见问题

### 密码忘了怎么办？

```bash
/etc/init.d/mysql stop
mysqld_safe --skip-grant-tables &
# 在另一个终端 输入 mysql 进入终端
在另一端执行 SQL 命令
UPDATE mysql.user SET password=PASSWORD('nouveau') WHERE user='root';
## Kill mysqld_safe from the terminal, using Control + \
/etc/init.d/mysql start
```

## 0xEE 参考链接

关于 SQL 与数据库的有趣解释

1. [Inner Join 和 Outer Join](http://stackoverflow.com/questions/38549/what-is-the-difference-between-inner-join-and-outer-join)
2. [如何防止 SQL 注入](http://stackoverflow.com/questions/60174/how-can-i-prevent-sql-injection-in-php)
3. [索引是怎么工作的](http://stackoverflow.com/questions/1108/how-does-database-indexing-work)
4. [Mysql 常用 SQL 语句集锦（本文部分 SQL 语句取自此博文）](https://gold.xitu.io/post/584e7b298d6d81005456eb53)

http://stackoverflow.com/questions/194852/concatenate-many-rows-into-a-single-text-string
