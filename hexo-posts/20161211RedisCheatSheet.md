title: Redis Cheatsheet
date: 2016-12-11 18:41:47
categories:
 - 后台组件
tags:
 - Redis
 - Cheatsheet

---

## 0x00. 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 MongoDB 相关命令。

 - Redis Shell
 - Redis 配套工具
 - Redis-Py
 - Django 中使用 Redis 进行缓存
 - 踩坑记录

不定期更新。

<!-- more -->

## 0x01. Redis Shell

 - RedisClient
 - 通过网络或者 Dash 查看文档
 - Redis 官方自带工具

## 0x02. Redis 配套工具

## 0x03. Redis-Py

## 0x04. 踩坑记录

### 1. 无法磁盘持久化

用 scrapy 配合 scrapy-redis 抓取网页并且存储到 MongoDB 里面。

由于 scrapy-redis 重写了 scrapy 的几个核心模块，借助 redis 来实现多个 scrapy 节点从而实现分布式。

默认的 scrapy 设置会把 items 放在 redis 从而方便程序对 items 进行后续处理。这个设计很完美，只是美中不足的是，我常常需要抓取大量页面直接缓存到数据库中。这就导致了 redis 很快就满了。

于是很容易报出这么一个错误。

> (error) MISCONF Redis is configured to save RDB snapshots, but is currently not able to persist on disk. Commands that may modify the data set are disabled. Please check Redis logs for details about the error.

出错原因如同提示所言，无法磁盘持久化。

基本上问题可能就是：
1. 磁盘满了。
2. redis 本身在某个地方配置了磁盘缓存的大小。
3. 其他权限之类的问题。

最快的解决方式就是删除占用磁盘的部分。

```bash
# 进入 redis-cli 删除 items
config set stop-writes-on-bgsave-error no
del xxx_html:items
config set stop-writes-on-bgsave-error yes
# 到 bash 下面检查磁盘，我的机器瞬间释放了 3GB 的磁盘空间
df -hl
```
备注：del 一次即可，因为有程序正在运行，所以当 del 之后，原来阻塞的程序接着开始运行。 xxx_html:items 会不断出现新的值。

Scrapy 立马就开始工作了（无需重启）


