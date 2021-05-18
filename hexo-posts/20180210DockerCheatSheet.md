title: Docker CheatSheet
date: 2018-02-10 09:01:55
categories:
 - 我的开源项目
tags:
 - Docker
 - DevOps
 - Django

---

## 0x00 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 Docker 相关和命令。

 - Docker 相关概念
 - Docker 配套工具
 - Django PostgreSQL RabbitMQ Redis ElasticSearch Sentry 集群 Docker 化
 - Docker 踩坑记录

不定期更新。

<!-- more -->

## 0x01 Docker 相关概念

### 1.1 Docker 是什么？

在认知 Docker 这种相对而言比较新概念的时候，只要从以往的经验中拿出一个词语来概括新词汇即可。

于是，我们便可以这么理解：

> Docker 是一种比虚拟机轻量的用来存放职责比较单一的应用的容器。

也就是三点：
 - 比虚拟机轻量
 - 用来存放职责单一的应用
 - 容器

显然这是一种理解，而不是一种定义。

### 1.2 Docker 是用来做什么的？

新技术本质是什么？工具也。
每一个新的技术都是为了提升效率才被创造出来，那么，究竟 Docker 可以从哪些方面提升我们的效率呢？

我们知道开发一个有些规模的网站的话，需要严格遵守如下的开发流程：

 - 编码
 - 测试
 - 集成到系统中
 - 部署

但如果人员比较多，则会出现问题，有的人喜欢用 MacOS, 有的人喜欢用 Ubuntu, 开发测试环境怎么统一呢？如果开发人员明明使用的是某个版本的 PostgreSQL, 用了最新的功能，但是测试和运维用的就是老版本的功能怎么办？

部署环境也会有问题，比如，开发部突然想使用更高版本的软件，比如突然需要更多的 Django 应用来负担海量请求的怎么办？Hadoop 不够用怎么办？

当然，思路很简单，开发的时候使用虚拟机，拷贝给大家一起用，部署的时候多创建一些机器，然后上 Ansible 远程操控。即可。

并不是不行，但是 Docker 由于更加轻量，操作粒度更加细腻，我可以销毁镜像，上传镜像，定制镜像，很轻松调整镜像包并且安装挂载文件。

## 0x02 Docker 初始配置

```
docker-machine create --driver=virtualbox default
docker-machine ls
eval "$(docker-machine env default)"
```

## 0x03 Django 技术栈 Docker 化

为了理解这个过程，下面我将我 Docker 化 django 应用的流程按照一定步骤演示出来。我将我使用 Django 的部分经验搞出来，做成了一个 django-bpc ，即 django best practice。如果诸位有兴趣研究的话，拿来看看源码倒是倒是非常好。

```bash
# 演示环境为 MAC, 在此之前，务必安装好 docker for mac 以及 virualbox
# xxxxxx 为 阿里云分配的容器 registry
docker-machine create --engine-registry-mirror=https://xxxxxx.mirror.aliyuncs.com -d virtualbox default

```

```bash
├── AUTHORS.md
├── HISTORY.md
├── LICENSE
├── MANIFEST.in
├── Makefile
├── README.md
├── static
├── compose
│   ├── django
│   ├── elasticsearch
│   ├── nginx
│   ├── postgres
│   ├── rabbitmq
│   └── redis
├── config
│   ├── __init__.py
│   ├── settings
│   ├── urls.py
│   └── wsgi.py
├── dev.yml
├── docker-compose.yml
├── docs
│   ├── Makefile
│   ├── exts
│   ├── make.bat
│   ├── make_pdf.sh
│   └── source
├── cli.py
├── pytest.ini
├── requirements
│   ├── base.txt
│   ├── local.txt
│   ├── production.txt
│   └── test.txt
├── scripts
├── setup.cfg
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_basics.py
└── mipha
    ├── __init__.py
    ├── contrib
    ├── static
    ├── templates
    ├── yaaccounts
    ├── yaadmin
    ├── user
    ├── yablog
    ├── yacommon
    └── yataskapp
```

### 3.1 开发时

#### 1. 运行所需组件

在开发时候需要使用几个后台的组件

- PostgreSQL 用于做数据存储
- Redis 用于做缓存 和 Session 等等
- RedditMQ 用于消息队列
- ElasticSearch 用于做搜索与推荐

目录中的组件基本上都在这儿了。

```
├── compose
│   ├── django
│   ├── elasticsearch
│   ├── nginx
│   ├── postgres
│   ├── rabbitmq
│   └── redis
```

进行初步的封装和添加脚本，不直接采用官网的配置需要是因为添加一些的定制版本。

#### 2. Vue.JS 运行环境

Vue.JS 使用 Vue-Cli 搭建的脚手架还是挺方便的，这个就无需 Docker 化了，需要注意的是，建议配置一下开发时候请求的 API 地址。

我本人用于请求本地地址的 8080 端口，并且 8080 端口映射到 Docker 容器里面的 Django App

#### 3. Django App

配置 Django, 我使用的是 ubuntu 16.04 基础镜像，然后安装必备的依赖。

接着指定 workdir 为当前目录

需要注意的是，Django App 里面需要等待 PostgreSQL 初始化完毕才能进行正常的运行接下来需要运行的命令，比如 runserver 之类的命令。

entrypoint 的左右即是放在命令执行之前，这样的话，重写掉 entrypoint 文件，就可以实现上面的功能了

```python
# 本段代码来自 cookiecutter Django
function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_USER", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done
```

最后封装一些命令到，比如启动 Celery 之类的。

#### 4. Celery 运行环境

#### 5. 其他零散的重要配置

### 3.2 具体开发

我编写了一整套 makefile 的命令，我会先进入项目 YaDjangoBlog , 然后执行 make ; 执行 make 之后，显示了我编写的一些便于开发测试的命令如下：

```
sep--sep-a           ========== 开发时命令 ==============
django-build-up      build and compose up
force_djnago_build-up django / pg / es
django-before-up     e.g pg / es / redis
django-runserver     runserver
django-celerybeat    celerybeat
django-celeryworker  celeryworker
django-just-up       build and up
django-manager       Enter python manage.py
django-console       Enter Django Console
shell                Enter Shell
dbshell              Enter psql as yadjangoweb
sep--sep-b           ========== 测试与代码质量 ==============
lint                 check style with flake8
test                 run tests quickly with the default Python
coverage             check code coverage quickly with the default Python
sep--sep-c           ========== 文档生成相关 ==============
docs                 generate Sphinx HTML documentation, including API docs
servedocs            compile the docs watching for changes
sep--sep-d           ========== 程序发布相关 ==============
release              package and upload a release
dist                 builds source and wheel package
install              install the package to the active Python's site-packages
sep--sep-e           ========== Docker 镜像相关 ==============
build-postgres       > Postgres
force-build-postgres > Postgres
build-ubuntu         > base ubuntu
force_build-ubuntu   > base ubuntu
build-django         > base django
force_build-django   > base django
sep--sep-f           ========== 文件清理相关 ==============
clean                remove all build, test, coverage and Python artifacts
clean-build          remove build artifacts
clean-pyc            remove Python file artifacts
clean-test           remove test and coverage artifacts
```

#### 1. 构建镜像

执行 build 命令即可。

#### 2. 使用 Tmuxinator 批量运行命令

现在，我有这么一个需求，就是在 iterm 中开启如下的终端：

- 第 1 个终端，运行的命令是 Vue.JS 的启动命令 npm run dev。
- 第 2 个终端，有两个分屏，其一用于构建 iconfont 字体文件的命令，其二用于 Gulp 动态编译 SCSS 文件的命令。
- 第 3 个终端，运行的命令是 Django 的 runserver 的命令。
- 第 4 个终端，有两个分屏，一个是 Django 容器的 bash 环境，另一个是 PostgreSQL 的 命令行环境。
- 第 5 个终端，有两个分屏，一者运行 Celery Beat，另一者则是运行 Celery Worker.

> 当然，目前没有添加 redis 和 RabbitMQ 的命令行环境

#### 3. 使用 PyCharm 进行开发

### 3.3 部署时

Docker 部署需要解决的问题，是裸机部署的 Docker 化。

> TODO: 目前 Docker 部署的脚本还在编写中，这部分的文字可能后期会调整

#### 0. Django 生产环境和开发环境之间的区别

生产环境和开发环境除了一些文字配置上的不同，还有一些不同，比如：

1. 新增了 uwsgi / gunicorn 作为新的 web 容器
2. 新增了 Ngnix 作为反向代理
3. Celery Worker 数量的变化
4. Supervisor 进程守护

首先说第一点带来的区别，我们使用 Django 内置的 runserver 的时候，其实这个命令可以用于做生产环境的 Web 服务器。

比如，只需如此 python manage.py runserver 0.0.0.0:8888

可以用，但不推荐用。没什么负载量。这时候就需要 gunicorn 了。你可以理解 Gunicorn 是进阶的 runserver,

可以参考：https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/gunicorn/

同时，Gunicorn 可以进行颗粒度更细致的操作，但负载量不如 uwsgi, 毕竟前者 python 写的，后者是 C 写的。

一般 Gunicorn 也会配上 NGNIX,

简单来说，Nginx 至少可以解决下面的问题：

- 匹配域名
- 转发请求
    - 设置请求头
    - 转发本地的静态文件 (static / media）
    - 映射部分请求到 gunicorn , 然后 gunicorn 开启一个线程到 Django
    - 负载均衡

需要注意的是 gunicorn 这种关键性的进程，一定要用 Supervisor 进行守护，否则挂掉了就完蛋了，

#### 1. 裸机部署 Django 程序

#### 2. Docker 部署

## 0x04 Docker 踩坑记录

### 4.1 PostgreSQL 的初始化

当 Docker 化 PostgreSQL 的时候，必须要把一些初始化脚本放在 docker-entrypoint-initdb.d 中，才能初始化，笔者在进行测试的时候多次发现无法进行初始化，究其原因，经过查找，如果没有及时删除 Volume 的话，则无论怎么初始化，或者 Build, 每一次都会挂载原来的文件夹。

```bash
ADD init_django_db.sh /docker-entrypoint-initdb.d/init_django_db.sh
```

### 4.2 清空所有 Image

```bash
# Delete all containers
docker rm $(docker ps -a -q)
# Delete all images
docker rmi $(docker images -q)
# Force delete
docker rmi $(docker images -q) -f
# Delete Unused Volume
docker volume prune
```

# 0xEE 参考链接

- https://github.com/wsargent/docker-cheat-sheet

---
ChangeLog:
 - **2017-01-20** 初始化本文
