title: Shell CheatSheet
date: 2015-04-18 08:34:47
categories:
 - 善用佳软
tags:
 - macOS
 - Ubuntu
 - Linux
 - Cheatsheet

---

## 0x00. 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 Shell 单行命令。

脚本主要适用于 BASH 环境，因为 Server 端的 Bash 主要还是 Bash 脚本居多。

不定期更新。

> 声明：Bash 命令适合那些十来行代码可以搞定的比较简单的逻辑，一般情况下用于处理一些服务的开启。至于部署，强烈推荐 Ansible. 目前在项目中使用 Ansible 从零开始无人值守部署一台机器。基本上完美到极致。

<!-- more -->

## 0x01. 快捷键操作

 - 「**c-c**」  : 中断当前命令。
 - 「**c-z**」  : 当前程序暂停，bg 切换后台运行，使用 fg 可以调回
 - 「**tab**」  : 补全
 - 「**tabx2**」  : 补全提示
 - 「**c-r**」  : 搜索命令行
 - 「**c-w**」  : 同 vim
 - 「**c-u**」  : 删除整行
 - 「**a-b/a-f**」  : 移动一个词
 - 「**c-a**」  : 移动至行首
 - 「**c-e**」  : 移动至行尾
 - 「**c-k**」  : 删除光标到行尾
 - 「**c-l**」  : 清屏
 - 「**c-x,c-e**」  : 用默认编辑器编辑当前命令（这样就可以把其他文本移动扔掉了。)

## 0x02. Linux 命令

如果你使用的是 MAC, 先安装下面的程序。

```bash
brew install findutils --with-default-names
brew install gnu-sed --with-default-names
brew install gnu-tar --with-default-names
brew install gnu-which --with-default-names
brew install gnutls --with-default-names
brew install grep --with-default-names
brew install coreutils
brew install binutils
brew install diffutils
brew install gzip
brew install watch
brew install tmux
brew install wget
brew install nmap
brew install gpg
brew install htop
```

> 经过上面一步，则基本上 find sed tar which 这些命令使用的 gnu 版本 (linux 版本）, 而非系统自带的 unix 版本了。

### 基本命令

```bash
man python

whatis python
which python
info python
where python
```

#### 文件与目录管理

```bash

# 创建和删除
mkdir
mkdir -p a/b/c
rm
rm -rf dir/file/regex
rm *log
# 等价
find ./ -name "*log" -exec rm {};
mv

## mv 可以用于移动文件，也可以进行重命名

cp

find ./ | wc -l
cp -r source_dir dest_dir
rsync --progress -a source_dir dest_dir
# 目录切换
cd
cd -
cd / cd ~
pwd
ls -lrt

find ./ -name "*.o" -exec rm {} \;

more
head
tail
tail -f filename
diff

chown
chmod
chown -R tuxapp source/
chmod a+x myscript

ln cc ccA
ln -s cc ccTo

cat -v record.log | grep AAA | grep -v BBB | wc -l

```

```bash
#!/bin/bash
lftp <<SCRIPT
set ftps:initial-prot ""
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate no
open ftp://192.168.2.254
user xxx xxx
lcd /Users/xxx/Codes/Workspace/
put /Users/xxx/Codes/Workspace/all_codes.zip
exit
SCRIPT
```

##### 查找文件之 find (gfind)

```bash
## Find

find . \( -name "*.txt" -o -name "*.pdf" \) -print
# 正则方式查找。txt 和。pdf
find . -regex  ".*\(\.txt|\.pdf\)$"
find . ! -name "*.txt" -print
find . -maxdepth 1 -type f
# 定制搜索
## 按照类型搜索
find . -type f -print  #只列出所有文件
find . -type d -print  #只列出所有目录
find . -type l -print  #只列出所有符号链接

## 按照时间搜索
find . -atime 7 -type f -print # 最近第 7 天被访问过的所有文件：
find . -atime -7 -type f -print # 最近 7 天内被访问过的所有文件：
find . -atime +7 type f -print # 查询 7 天前被访问过的所有文件：
# w,k,M,G
find . -type f -size +2k
find . -type f -perm 644 -print  # 找具有可执行权限的所有文件
find . -type f -user weber -print # 找用户 weber 所拥有的文件

# 后续动作
## 删除
find . -type f -name "*.swp" -delete
## 执行动作
find . -type f -name "*.swp" | xargs rm
find . -type f -user root -exec chown weber {} \;
## eg: copy 到另一个目录
find . -type f -mtime +10 -name "*.txt" -exec cp {} OLD \;
##  -exec ./commands.sh {} \;

# 2. 删除内部为空的文件夹
# 递归删除 a/b/c
find . -type d -empty -delete
#    使用.gitkeep 进行填充
find . -type d -empty -exec touch {}/.gitkeep \;
find . -type d -empty -not -path '*/\.*' -exec touch {}/.gitkeep \; # 不初始化.git/

# 3. 寻找 TOP 10
find . -type f -printf '%s %p\n'| sort -nr | head -10 | awk '{$1/=1024*1024;printf "%.2fMB - %s\n",$1,$2}'

# 4. 寻找文件夹 TOP 10

```

#### 文本处理

```bash

## Grep
grep match_pattern file

-o 只输出匹配的文本行
-v 只输出没有匹配的文本行
-c 统计文件中包含文本的次数

-n 打印匹配行号
-i 搜索时符合大小写
-l 之打印文件名

grep "class" . -R -n # 多级目录中对文本递归搜索
grep -e "class" -e "vitural" file # 匹配多个模式
grep "test" file* -lZ| xargs -0 rm # grep 输出以、0 作为结尾符的文件名：（-z）

-d 定义定界符
-n 输出为多行
-l {} 指定替换字符串
cat file.txt | xargs # 打印多行
cat file.txt | xargs -n 3 # 分割多行
cat file.txt | xargs -I {} ./command.sh -p {} -1
-0 指定、0 为输入定界符
find source_dir/ -type f -name "*.cpp" -print0 |xargs -0 wc -l

sort 排序
-n 按数字进行排序
-d 按字典序进行排序
-r 逆序排序
-k N 指定按照第 N 列排序

sort -nrk 1 data.txt
sort -bd data // 忽略像空格之类的前导空白字符

sort unsort.txt | uniq > sorted.txt # 消除重复行
sort unsort.txt | uniq -c # 统计各行在文件中出现的次数
sort unsort.txt | uniq -d # 找出重复行

# 用 tr 进行转换

# cut 按列切分文本
cut -f2,4 filename #截取文件的第 2 列和第 4 列
cut -f3 --complement filename #去文件除第 3 列的所有列
cut -f2 -d";" filename -d #指定定界符
cut -c1-5 file #打印第一到 5 个字符
cut -c-2 file  #打印前 2 个字符

# paste 按列拼接文本
paste file1 file2 -d ","

# wc 统计行和字符的工具
wc -l file # 统计行数
wc -w file # 统计单词数
wc -c file # 统计字符数

# sed 文本替换利器
sed 's/text/replace_text/' file  # 首处替换
sed 's/text/replace_text/g' file  # 全局替换
sed -i 's/text/repalce_text/g' file # 替换文件
sed '/^$/d' file  # 移除空白行

```

#### 查看磁盘空间

```bash
#查看磁盘空间
df -h
#查看目录大小
du -sh
du -sh `ls` | sort
#打包
tar -cvf
#解包
tar -xvf
#压缩
gzip
#解压缩 gunzip bzip
```

- tar 是将多个文件放在一起变成一个 tar 文件 (Tape Archiver)
- gzip 是讲一个文件变成一个压缩文件

> 则 foo.tar.gz 指的是 先把文件转为 tar 文件，然后 gzip 之

https://askubuntu.com/questions/122141/whats-the-difference-between-tar-gz-and-gz-or-tar-7z-and-7z

#### 进程管理工具

ps -fe| grep posgres

####  性能监控

内存瓶颈

```bash
htop
free # 从 /proc/meminfo 读取数据
```

IO 瓶颈

```bash
# ubuntu 下 可以 mac 下不可以
iostat -d -x -k 1 1
```

如果 %iowait 的值过高，表示硬盘存在 I/O 瓶颈。
如果 %util 接近 100%，说明产生的 I/O 请求太多，I/O 系统已经满负荷，该磁盘可能存在瓶颈。
如果 svctm 比较接近 await，说明 I/O 几乎没有等待时间；
如果 await 远大于 svctm，说明 I/O 队列太长，io 响应太慢，则需要进行必要优化。
如果 avgqu-sz 比较大，也表示有大量 io 在等待。

####  网络工具

```
netstat -a
```

####  用户管理工具

所有用户和用户组信息保存在：/etc/passwd , /etc/group

用户

```bash
useradd -m yaweb # 创建相关账号，和用户目录 /home/yaweb
passwd yaweb
userdel -r yaweb # 删除
```

用户组

```bash
usermod -g groupName username # 变更组
usermod -G groupName username # 添加到组
usermod -aG sudo yaweb # 添加 yaweb 到 sudo 组
```

用户权限

```bash
chown userMark(+|-)PermissionsMark
```
userMark 取值：
 - u：用户
 - g：组
 - o：其它用户
 - a：所有用户

PermissionsMark 取值：
 - r: 读
 - w：写
 - x：执行

```bash
chmod a+x main         对所有用户给文件 main 增加可执行权限
chmod g+w blogs        对组用户给文件 blogs 增加可写权限
chown -R weber server/
```

####  系统管理以及 IPC 资源管理

```
ps -ef | grep twocucao
ps -lu twocucao
# 完整显示
ps -ajx

top
htop

lsof -i:3306
lsof -u twocucao

kill -9 pidnum

# 将用户 colin115 下的所有进程名以 av_开头的进程终止：

ps -u colin115 |  awk '/av_/ {print "kill -9 " $1}' | sh
# 将用户 colin115 下所有进程名中包含 HOST 的进程终止：

ps -fe| grep colin115|grep HOST |awk '{print $2}' | xargs kill -9;
```

### 其他一些技巧

### 有趣的重命名

常用 mv 进行重命名，有的时候这个功能显得很不实用，比如，我要把当前的文件夹内的所有图片命名为 0001.png-9999.png, 这个 mv 时候就相当的鸡肋。

```bash
brew install renameutils mmv rename
```
如果对于大批的文件需要重命名，比如有接近 10000 个文件，大量乱码文件改为 0001.jpg - 9999.jpg

这种东西放在 IPython 里面写 Python 脚本也还 OK, 但是总想直接一行命令解决

### 常用组合技

```bash
# 查看 windows txt 文件中的查看二字的数量
cat * | iconv -f GBK | grep 查看 | wc -l
```

### Python 常用 Shell 命令

```bash

# 升级当前所有第三方包
pip install -i https://pypi.doubanio.com/simple -U pip
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U -i https://pypi.doubanio.com/simple

```
###

```
tig 字符模式下交互查看 git 项目
jq 可以用于 json 文件处理以及何世华显示
python -m json.tool
axel -n 20 http://centos.ustc.edu.cn/centos/7/isos/x86_64/CentOS-7-x86_64-Minimal-1511.iso
cloc 用于统计代码
```

## Tips && Hacks

### 网络篇
/etc/hostname /etc/hosts

### 磁盘篇

```bash
# 查看当前目录大小
du -sh
# 查看当前目录的下一级文件和子目录的磁盘容量
du -lh --max-depth=1
```
### 文本篇

sed -i 's/twocucao/micheal/g' xx.dump.sql
sed -n 634428,887831p insert_doc_ids_new.sql > uninserted_sql.sql

### 用户篇

```bash
# 添加 yaweb 为 sudo 用户
usermod -aG sudo yaweb
```

ps au | grep phantomjs | awk '{ print $2 }' | xargs kill -9

### 拷贝本地文件到远程服务器

rsync -vr --progress JudgementLibraryCrawler twocucao@192.168.2.151:/Users/twocucao/Codes/

### ssh
ssh -l root 192.168.2.253

### 扫描器
sudo nmap -v -sS -O 192.168.2.0/24

### FTP Client 自动化提交

```
#!/bin/bash

lftp <<SCRIPT
set ftps:initial-prot ""
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate no
open ftp://xxx.xxx.xxx.xxx:21
user ftpuser ftppass
lcd /Users/<username>/Ftps/Workspace/libs
put /Users/<username>/Ftps/Workspace/repos/xxx.jar
exit
SCRIPT
```

## 资料推荐

1. 一个关于 Linux 命令的各种奇技的网站 http://www.commandlinefu.com/commands/browse
2. Linux 工具快速教程 http://linuxtools-rst.readthedocs.org/zh_CN/latest/index.html
3. 一个 Awesome List, https://github.com/jaywcjlove/linux-command
4. 命令行的艺术  https://github.com/jlevy/the-art-of-command-line
5. man command 需要好好研读，特别是 man bash 至少要研读几遍
