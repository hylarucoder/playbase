title: 使用 Python 监控 Mac 一天的运行（下）
date: 2016-07-15 18:50:23
categories:
 - Python 黑魔法
tags:
 - 编程工具
 - 效率
 - 小玩具

---

## 前言

如果有不清楚本文介绍的是什么的？请移步
（使用 Python 监控 Mac 一天的运行 - 上）[http://www.jianshu.com/p/9ebb527e93a0]

任务回顾一下：

> 隔一段时间使用 Python 脚本，统计当前电脑的运行情况，CPU, 内存，硬盘，网络使用状况，然后在每天的下午六点通过 Email 把统计情况汇总，并且必须要有监控图，并通过 Email 发送给我的邮箱。

好了，这篇文章，我们讲解的是具体的 Python 脚本完成这些任务。因为代码可能稍微复杂一点点，老规矩，讲解思路和必要注意点，其他的请参阅代码。

## 目标确定与任务分解

目标就如同上面两段所写。

那么把任务分解一下：

 - 首先，你得知道如何获取计算机的运行信息。
 - 其次，你得知道如何把这些数据保存下来（不保存怎么分析）.
 - 接着，你得知道如何分析并制图。
 - 最后，你得知道如何发送邮件。

好了，本文的目录也就应运而生了。

 - 前言
 - 目标确定和任务分解
 - Python 获取计算机运行信息
 - RRDTool 保存计算机运行信息
   - 为什么是 RRDTool 而不是 sqlite
   -RRD 怎么保存信息
   -RRD 怎么保存计算机运行信息
 - RRDTool 制图功能
 - 汇总并发送 Email
 - 思考与不足
 - 代码

## Python 获取计算机运行信息

我们知道有很多 shell 命令可以获取当前时间点，或者当前时间段的计算机各种情况，但是呢，我们只需要某个时间点的计算机的运行情况，Python 中有一个比较好的神器叫做 psutil, 果断安装之。

```bash
pip3 install psutil
```

运行如下脚本，你就可以看出来你的电脑运行的当前状况了。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import rrdtool
import os
import sys
import time
from urllib.request import urlopen,URLError
import socket
import getpass
import psutil
import logging

now = str(time.strftime("%Y%m%d%H%M%S"))
today = str(time.strftime("%Y%m%d"))

logging.basicConfig(
    format="%(asctime)s - \
[%(process)d]%(filename)s:%(lineno)d - %(levelname)s: %(message)s",
    datefmt='%Y-%m-%d %H:%I:%S',
    filename=os.path.expanduser('~/OhMyCode/PyTools/logs/'+today+'.log'),
    level=logging.INFO
)

logger = logging.getLogger('monitor_my_mac')

if sys.version_info < (3,):
    raise RuntimeError("at least Python3.0 is required!!")
APP_DESC = """

                ---- A Terminal Tools For Monitoring Mac Daily

@author Micheal Gardner (twocucao@gmail.com)
                                last_update 2016-02-28
"""

def linux_distribution():
    try:
        return platform.linux_distribution()
    except:
        return "N/A"

def check_connectivity(reference):
    """检查是否连接到网络"""
    try:
        urlopen(reference, timeout=1)
        return True
    except URLError:
        return False

def secs2str(secs):
    """ 将秒转化为字符串 """
    if int(secs) < 0:
        return ""
    return str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(secs)))

def fetch_all_info():
    network_connectivity = check_connectivity("http://119.75.218.70")

    public_ip_addr = urlopen('http://ip.42.pl/raw').read().decode("utf-8")

    #=============>操作系统信息<==============#
    print("========>MACHINE<==========")
    print(getpass.getuser())
    print(platform.uname())
    # print(os.uname())

    print("""Python version: %s
    dist: %s
    linux_distribution: %s
    system: %s
    machine: %s
    platform: %s
    uname: %s
    version: %s
    mac_ver: %s
    """ % (
    sys.version.split('\n'),
    str(platform.dist()),
    linux_distribution(),
    platform.system(),
    platform.machine(),
    platform.platform(),
    platform.uname(),
    platform.version(),
    platform.mac_ver(),
    ))

    os_boot_time = psutil.boot_time()
    print("Boottime: " + str(os_boot_time) +"->"+secs2str(os_boot_time)  )

    print("========>CPU<==========")
    print(psutil.cpu_times())
    print(psutil.cpu_count())
    print(psutil.cpu_count(logical=False))
    print(psutil.cpu_times_percent())

    print("========>MEM<==========")
    print(psutil.virtual_memory())
    print(psutil.swap_memory())

    print("========>DISK<==========")
    print(psutil.disk_partitions())
    print(psutil.disk_usage("/"))
    print(psutil.disk_io_counters())
    print(psutil.disk_io_counters(perdisk=True))

    print("========>NET<==========")
    print(psutil.net_io_counters())
    print(psutil.net_io_counters(pernic=True))
    print(psutil.users())

    print("hostname:" + socket.gethostname())
    print("internal ip address: " + socket.gethostbyname(socket.gethostname()))
    print("connected to internet?: " + str(network_connectivity))
    print("public ip: " + public_ip_addr )

def main():
    print(APP_DESC)
    fetch_all_info()

if __name__ == "__main__":
    main()
```
好的，下面我就想把这些数据保存下来。

## RRDTool 保存计算机运行信息

对于 RRDTool, 引自 RRDTool 的官网

> RRDtool is the OpenSource industry standard, high performance data logging and graphing system for time series data. RRDtool can be easily integrated in shell scripts, perl, python, ruby, lua or tcl applications.

![stream-pop.png](http://upload-images.jianshu.io/upload_images/52890-b79e26953467d4a4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

> **注意：**    如果你看不懂下面关于 RRDTool 的相关内容，请立即反复参考下面的链接，大致留下 rrd 的印象。注意，**是反复，是反复，是反复**, 重要的事情听说要说三遍的。

http://oss.oetiker.ch/rrdtool/tut/rrdtutorial.en.html

wait,wait,don't tell me, 你怎么使用这个什么 RRDTool, 这又是什么东西？既然你一天只存储一点点的东西，为什么不使用 sqlite?

### 为什么是 RRDTool 而不是 sqlite

答案很简单，因为我们采用的是监控，采用 sqlite 不是说不可以，只是 sqlite 在监控领域不是很专业。那为什么不够专业呢？

> 因为在这个场景下，仅仅有存储数据的功能是不够的。

> 还需要根据监控的场景，进行各种绘图功能。

 - 如果使用 sqlite, 还要安装各种 python 绘图，运算库 (seaborn,numpy,pandas 等）进行统计绘图，那样就不够轻量级了。
 - 而 rrdtool 作为运维监控的常用工具，则成为首选数据库。

### RRD 怎么保存信息

既然，这是一种叫做数据库的东西，那么，最好的学习方式就是和在实战中练习并且和之前学过的同类型数据进行对比。

那好，我们要回想一下，在学习过的关系型数据库里面，我们是怎么进行数据的怎删改查的。

首先，对于关系型数据库，DBA 创建数据库并指派给某些权限用户，接着由 DB 用户创建表，表中需要各种数据的定义数据类型，最后插入数据，并且进行大量的 curd.

在 sqlite 这种依靠单个文件作为存储介质的关系型数据库，则是由 DB 用户创建表，表中需要各种数据的定义数据类型，最后依赖 SQL 语句插入数据，并且进行大量的 curd.（注：没有谈到事务不代表事务不重要）

rrdtool 也是这个道理。它也是依靠单文件作为存储介质的一种 rrd 数据库的实现。先看下面的实例：

这个实例来自于官网的 tutorial : http://oss.oetiker.ch/rrdtool/tut/rrdtutorial.en.html

仔细阅读官方教程，我们大致可以得出以下结论。

对于创建数据库：

```bash
rrdtool create test.rrd             \
        --start 920804400          \
        DS:speed:COUNTER:600:0:U   \
        RRA:AVERAGE:0.5:1:24       \
        RRA:AVERAGE:0.5:6:10
```

 - 创建一个数据库文件，文件名为 test,
 - 开始时间为 unix 时间戳 920804400 ,
 - 存储的行车速度（额，其实这里我觉得用行车路程表示比较好）
 - 用两个 rra 用来保存"当保存行车路程的时候，经过计算的值".
 - 一个 databese 是一个 rrd 文件，一个 rrd 文件中存储多个 rra（类似于关系型数据库中，一个数据库里面有多张表）, 但是这里的"表"是用来存储不同的时间间隔的数据，所有的数据来源由创建数据库的时候指定的，(rr 代表 round robin,a 代表 achive)
 - 第一个 RRA 存储的是平均值（也可以存储 MAX 和 MIN),CDP 中的 PDP 超过一半的时候，则 CDP 标记为 UNKNOWNA（这里咱默认 0.5 就好）, 每隔 1 X 300 秒的时候，存一次平均值，存 24 次。

对于更新数据：

```bash
 rrdtool update test.rrd 920804700:12345 920805000:12357 920805300:12363
 rrdtool update test.rrd 920805600:12363 920805900:12363 920806200:12373
 rrdtool update test.rrd 920806500:12383 920806800:12393 920807100:12399
 rrdtool update test.rrd 920807400:12405 920807700:12411 920808000:12415
 rrdtool update test.rrd 920808300:12420 920808600:12422 920808900:12423
```
你可能有疑惑：官网里面的 speed 指的不是速度么，怎么会用来代表路程.（回顾一下：路程 = 时间 X 速度）, 官网的教程插入数据的时候，使用的是某个时间点已经行驶的路程。说实话，我也觉得很疑惑。
请注意：它更新的数据都是累加的 (COUNTOR), 也就是说，

对于绘图：

```bash
rrdtool graph speed.png                                 \
    --start 920804400 --end 920808000               \
    DEF:myspeed=test.rrd:speed:AVERAGE              \
    LINE2:myspeed#FF0000
```

```bash
rrdtool graph speed2.png                           \
    --start 920804400 --end 920808000               \
    --vertical-label m/s                            \
    DEF:myspeed=test.rrd:speed:AVERAGE              \
    CDEF:realspeed=myspeed,1000,\*                  \
    LINE2:realspeed#FF0000

```

```bash
rrdtool graph speed3.png                             \
    --start 920804400 --end 920808000               \
    --vertical-label km/h                           \
    DEF:myspeed=test.rrd:speed:AVERAGE              \
    "CDEF:kmh=myspeed,3600,*"                       \
    CDEF:fast=kmh,100,GT,kmh,0,IF                   \
    CDEF:good=kmh,100,GT,0,kmh,IF                   \
    HRULE:100#0000FF:"Maximum allowed"              \
    AREA:good#00FF00:"Good speed"                   \
    AREA:fast#FF0000:"Too fast"
```

```bash
rrdtool graph speed4.png                           \
      --start 920804400 --end 920808000               \
      --vertical-label km/h                           \
      DEF:myspeed=test.rrd:speed:AVERAGE              \
      CDEF:nonans=myspeed,UN,0,myspeed,IF             \
      CDEF:kmh=nonans,3600,*                          \
      CDEF:fast=kmh,100,GT,100,0,IF                   \
      CDEF:over=kmh,100,GT,kmh,100,-,0,IF             \
      CDEF:good=kmh,100,GT,0,kmh,IF                   \
      HRULE:100#0000FF:"Maximum allowed"              \
      AREA:good#00FF00:"Good speed"                   \
      AREA:fast#550000:"Too fast"                     \
      STACK:over#FF0000:"Over speed"
```
![speed.png](http://upload-images.jianshu.io/upload_images/52890-e7979c928d1bf4ec.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![speed2.png](http://upload-images.jianshu.io/upload_images/52890-92c75ac53eedd2bc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![speed3.png](http://upload-images.jianshu.io/upload_images/52890-061e0e0c91521d9b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![speed4.png](http://upload-images.jianshu.io/upload_images/52890-59100ed39a3b8588.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### RRD 怎么保存计算机运行信息

在这里，仅仅使用带宽的统计作为演示案例（案例来自使用 Python 自动化运维这本书）.

#### 创建数据库

#### 更新数据库

#### RRDTool 制图

## 汇总并发送 Email
## 思考与不足
## 代码

代码地址为：

## 参考资料

https://github.com/yorkoliu/pyauto/blob/master/%E7%AC%AC%E4%B8%89%E7%AB%A0/rrdtool/graph.py

http://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python

---
ChangeLog:
 - **2017-03-14** 本文已经彻底烂尾了，哈哈哈
