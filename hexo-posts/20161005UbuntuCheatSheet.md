title: Ubuntu16.04 Cheatsheet
date: 2017-10-20 18:41:47
categories:
 - 善用佳软
tags:
 - Ubuntu
 - Cheatsheet

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 Shell 单行命令。

不定期更新。

桌面版和 Server 版的操作系统版本均为 Ubuntu 16.04 , 数据库为 MySQL / PostgreSQL , Python 3.5.2 开发和运行环境。

由于部分 Mac 上面的配置与 Ubuntu 上配置几乎相同，特别是一些桌面端，跨平台，强烈建议使用。

每次来一个新同事就需要给他们的环境进行配置，配置其实挺麻烦的，虽然可以花一天的时间配置一遍，但总觉得如果多来几个同事的话我基本上就废掉了。
于是抛弃 bash 脚本，修改为 Ansible 脚本，将当前的配置任务彻底脚本化。

<!-- more -->

## 0x01 Ubuntu 桌面版开发基本配置

语言级别配置，请参考我的其他文章，如何优雅的使用 MAC

## 0x02 Ubuntu 服务器版本基本配置

第一步，更新源：

```bash
# deb cdrom:[Ubuntu 16.04 LTS _Xenial Xerus_ - Release amd64 (20160420.1)]/ xenial main restricted
deb-src http://archive.ubuntu.com/ubuntu xenial main restricted #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb http://mirrors.aliyun.com/ubuntu/ xenial multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse #Added by software-properties
deb http://archive.canonical.com/ubuntu xenial partner
deb-src http://archive.canonical.com/ubuntu xenial partner
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted multiverse universe #Added by software-properties
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-security multiverse
```

```bash
# 更换源
sudo apt-get update
sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev libcurl4-openssl-dev python-software-properties libffi-dev
sudo apt-get install zsh tree htop
sudo apt-get install build-essential acl ntp htop git libpq-dev libmysqlclient-dev libffi-dev libfreetype6-dev libjpeg8-dev liblcms2-dev libtiff5-dev libwebp-dev libxml2-dev libxslt1-dev tcl8.6-dev tk8.6-dev zlib1g-dev python-dev python-pip python-pycurl python-tk ipython supervisor python3.5 python3.5-dev python3-pip python3-lxml python3-tk ipython3
sudo apt-get install mysql-server mysql-client libmysqlclient-dev slurm

# GIT 配置
git config --global color.ui true
git config --global user.name "twocucao"
git config --global user.email "twocucao@gmail.com"
ssh-keygen -t rsa -b 4096 -C "twocucao@gmail.com"
```

### 2.1 设置无登录密钥

```bash
# 刚开始用了一个很蠢的方法
scp ~/.ssh/id_rsa.pub twocucao@192.168.2.156:.ssh/id_rsa.pub
ssh twocucao@192.168.2.156 "mkdir .ssh;chmod 0700 .ssh"

# 现在想想，可以直接 ssh-copy-id
ssh-copy-id twocucao@192.168.2.156
```

http://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login
```bash
# 服务器

sudo apt-get install openssh-server
sudo vi /etc/ssh/sshd_config # 找到 PermitRootLogin no 一行，改为 PermitRootLogin yes
sudo service ssh restart

sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev libcurl4-openssl-dev python-software-properties libffi-dev

sudo adduser deploy
sudo adduser deploy sudo
su deploy

# 开发机复制 ssh 公钥。
# 可以用下面的命令，汗，之前都是在服务器上面创建.ssh 文件夹，然后在本地 scp 拷贝过去，现在想想这个方法还是挺笨的。
# 就像这样
scp ~/.ssh/id_rsa.pub deploy@192.168.1.143:/webapps/xxxapp/.ssh/authorized_keys
# 其实这个命令就 OK 了。
ssh-copy-id deploy@IPADDRESS

# 服务器
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 561F9B9CAC40B2F7
sudo apt-get install -y apt-transport-https ca-certificates

sudo apt-get install -y nginx-extras
sudo service nginx start

```

## 0x02 Ubuntu 服务器版本基本配置

## 0x03 了解 Linux 服务器运行情况

```bash
# 运行时间
uptime

# 内存情况
free -h

# 网络类
## 实时流量监控
iftop
## 进程占用带宽
nethogs
## sudo nethogs eth0
iptraf

# 磁盘类
iotop
## 当 dstat 的 wai 字段值比较大时，可以使用 iotop 找出哪些进程出了问题

# 综合类 之 监控进程，进程管理
top
htop
glances # PS , 这个监控粒度更细

# 综合类 可以取代 vmstat , iostat , netstat , ifstat
dstat

# 综合类
# 约等于 strace + tcpdump + htop + iftop + lsof
sysdig
```

## 0x04 踩坑集合

前段时间公司新买了一台 Thinkpad Server 作为内网服务器。

于是在安装 Ubuntu16.04 的时候就遇到了一个令人哭笑不得的问题。

> **无法正常安装** 报 ubuntu 的 initramfs 错误。

于是，我下意识的去 Google 问题，在 Ubuntu 的一个论坛上面找到了对应的答案：

> 是 Superblock 的问题。

对应措施如下：

```bash
# 找到分区号
sudo fdisk -l|grep Linux|grep -Ev 'swap'
# 找到超级块
sudo dumpe2fs /dev/sda2 | grep superblock
# 修复超级块
sudo fsck -b 32768 /dev/sda2 -y
```

然后重启即可。

当然，问题并没有结束，还是在老地方发现 initramfs 错误。

就在我哭笑不得的准备最后一搏，实在不行就安装 CentOS 作为系统的时候，由于安装时候选择 language 的时候选择英文，结果居然安装成功了。

> 所以，解决问题的方式就是**不要使用简体中文进行安装**.

虽然这是一个很奇怪的问题，至今我也没有探索出来具体的原因。想到问题居然是因为安装的时候因为选择了中文安装。

> 这个问题还真的是.....

**最后知道真相的我眼泪掉下来**

### 3.1 磁盘问题

```
df -h 查看磁盘块占用的文件（block）
df -i 查看索引节点的占用（Inodes）
find / -size +100M |xargs ls -lh
# 删除 5 天前的文件
find /path/to/files* -mtime +5 -exec rm {} \;
du -h
rm xxx.log
echo "" > xxx.log
```

---
ChangeLog:
 - **2017-03-19** 重修文字，准备整理安装配置将结果转化为 Ansible PlayBook
 - **2017-10-20** 重修文字，准备整理安装配置将结果转化为 Ansible PlayBook
