title: MongoDB Cheatsheet
date: 2016-12-09 18:41:47
categories:
 - 后台组件
tags:
 - MongoDB
 - NoSQL
 - Cheatsheet

---

## 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 MongoDB 相关命令。

 - Mongo Shell
 - Mongo 配套工具
 - Python API

不定期更新。

<!-- more -->

## 安装

```bash
# MacOS 安装
brew install mongodb
brew services start mongodb
# Ubuntu Server 16.04
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
apt-get update -y
apt-get install -y mongodb-org
service mongod start
```
## 配置

### IP 地址

## MongoDB 配套工具

 - RoboMongo
 - 通过网络或者 Dash 查看文档
 - Mongo 官方自带工具

## MongoDB Shell

## 基本查询

db.users.find({"name": /.*m.*/})
db.users.find({'name': {'$regex': 'sometext'}})

https://docs.mongodb.com/manual/

### 增删改查

use myNewDatabase
db.myCollection.insert( { x: 1 } );

### 聚合操作

## PyMongo

```bash
# 建索引的时候，会阻塞当前的操作，甚至是查询操作
# 据说转为 background 方式不会阻塞但是，没有实践过
"msg" : "Index Build Index Build: 167413/751748 22%",
"progress" : {
	"done" : 167413,
	"total" : 751748
},
```
