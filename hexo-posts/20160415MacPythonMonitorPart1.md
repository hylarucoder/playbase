title: 使用 Python 监控 Mac 一天的运行（上）
date: 2016-04-15 18:50:23
categories:
 - Python 黑魔法
tags:
 - 编程工具

---

## 前言

一不小心写成上下两篇了。真是有些过意不去。毕竟，写的太多就少了一部分读者（少了一部分赞额）.

之所以拆成上下两篇，主要是因为在研究的过程中越发感到在一篇中强行植入那么多的东西，自己的文章结构组织起来有些困难，对读者来说，也是不容易理解。那倒不如拆分成两部分。

## 任务分解

我的需求如此简单，统计 Mac 上面一天的运行情况，然后在每天的下午六点把统计的情况汇总通过 Email 发送给我。

<!-- more -->

用更加具体来说，就是，

> 隔一段时间使用 Python 脚本，统计当前电脑的运行情况，CPU, 内存，硬盘，网络使用状况，然后在每天的下午六点通过 Email 把统计情况汇总，并且必须要有监控图，并通过 Email 发送给我的邮箱。

初看这玩意是挺简单的，但是自己动手写了以后就知道，其实还是稍微有些费时间的。

比如：

 - linux 下面定时执行一个脚本只需要 crontab 或者 at 以下就好了.mac 上是是什么？怎么运行一个任务？
 - 统计的数据存哪儿？用什么存？
 - 表格绘图怎么画出来？
 - Email 怎么发送，如果要发送好看一点点的 Email 怎么办？

既然那么多，那就分成两篇，一篇用来介绍 Mac 上面的定时任务（简单，短文）, 另一篇用 Python 来监控 Mac 电脑，并持久化监控数据，绘图，汇总，发送 email.(稍微复杂一点，带图长文）

 - 上篇讲在 Mac 上如何让一个脚本定时运行。
 - 下篇讲如何写一个 Python 监控脚本。

## 本文结构

 - 前言
 - 本文结构
 - 为什么需要定时任务？
 - Mac 上面如何进行定时任务。
 - 疑问和解答
 - 扩展阅读

## 为什么需要定时任务？

所谓的定时任务，分为两种：

 1. 指定时间执行的程序
 2. 每隔一段时间执行的程序

执行的内容，通常情况下和要做什么事情有关，但是从内容上，分为两种：

 1. 任务之间的数据没有什么关联的
   - 比如，你想去抓一些数据（迅雷会员账号）但是懒得自己动手，于是就写了一个小脚本，放在每天早上的 8 点钟，去抓来账号。
 2. 任务之间的数据有关联的，甚至某种程度上可以绘制图像。
   - 比如，下一篇要说的使用 Python 监控自己的电脑情况，e.g: 流量。隔一段时间就查看一下自己的电脑运行情况，把情况存下来。甚至，在某个时间点，把结果汇总发给某个人。

## Mac 上面如何进行定时任务。

 - 首先，你要写一个任务。
 - 其次，让这个任务定时执行。

好，简单的写一个任务 get_time.sh.

```bash
#!/bin/bash
date >> /Users/twocucao/Downloads/dates.txt
```
接着加上可执行。
```
chmod a+x get_time.sh
```

那么，怎么让 Mac 通过 launchd 隔一段时间就执行脚本呢？

创建一个特殊的 xml 文件叫做 com.twocucao.apple.getdates.plist, 给你所要运行的命令建立一个进程。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.twocucao.apple.getdates</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/twocucao/OhMyCode/Bash/get_time.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>10</integer>
</dict>
</plist>
```

对于这个 com.twocucao.apple.getdates 随你命名的，保证唯一就好。通常情况下选择反转域名（和 Java 编程类似）, 其他的，依照你的脚本位置和间隔时间修改。

拷贝到 LaunchDaemons, 加载定时工作，然后检查是否加载成功

```bash
cp com.twocucao.apple.getdates.plist /Library/LaunchDaemons
launchctl load -w /Library/LaunchDaemons/com.twocucao.apple.getdates.plist
#列出定时任务，并且筛选一下。确认是否加载成功。
launchctl list | grep twocucao
```

由于这个脚本实在是太弱智了仅仅是为了演示，所以，记得把他给卸载，删除

```bash
launchctl unload -w /Library/LaunchDaemons/com.twocucao.apple.getdates.plist
rm /Library/LaunchDaemons/com.twocucao.apple.getdates.plist
```

## 疑问和解答

 - 问：为什么要把脚本的配置放在 /Library/LaunchAgents 呢？
 - 答：当然，你可以拷贝到其他的地方，
   - 如果你的需求是该用户登录时候执行的话，那么拷贝到：~/Library/LaunchAgents, 这叫做 User Agents.
   - 如果你的需求是该用户登录时候执行的话，那么拷贝到：/Library/LaunchAgents, 这叫做 Global Agents
   - 如果你的需求是让 Root 用户或者指定用户登录时候执行的话，那么拷贝到：/Library/LaunchDaemons , 这叫做 Global Daemons
   - 如果你的需求是用户登录执行，那么拷贝到：/System/Library/LaunchAgents ,System Agents
   - 如果你的需求是让 Root 用户或者指定用户登录时候执行的话，那么拷贝到：/System/Library/LaunchDaemons, 这叫做 System Daemons.

> user-agents 是级别最低，其他所需权限依次递增。

 - 问：怎么检查任务执行结果？
 - 答：tail -f /Users/twocucao/Downloads/dates.txt

 - 问：如何确定 launchd 存在这个任务
 - 答：launchctl list

 - 问：既然是隔一段时间就能执行脚本，那么，我可以先用简单的 shell 脚本，配置好相关执行信息，让他定时执行，接着修改 shell 脚本执行新的逻辑么？
 - 答：可以。

 - 问：bash 命令监控多么方便，为何下一篇要使用 Python 作为监控工具。
 - 答：shell 命令编写代码不直观，编写效率低.Python 有很好的第三方库可以使用。

## 扩展阅读（精选优质资料）

1. 一个关于 Linux 命令的各种奇技的网站 http://www.commandlinefu.com/commands/browse
2. Linux 工具快速教程 http://linuxtools-rst.readthedocs.org/zh_CN/latest/index.html
3. 关于 launchd 的参考链接，
  - http://launchd.info/ http://www.splinter.com.au/using-launchd-to-run-a-script-every-5-mins-on/
  - https://developer.apple.com/library/mac/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
 - http://linuxtools-rst.readthedocs.org/zh_CN/latest/index.html
4. 命令行的艺术  https://github.com/jlevy/the-art-of-command-line

---
ChangeLog:
 - **2016-12-05** 重新排版。
