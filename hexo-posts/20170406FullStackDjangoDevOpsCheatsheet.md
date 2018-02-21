title: Full Stack Django DevOps Cheatsheet
date: 2017-04-06 20:29:00
categories:
 - 后端开发
tags:
 - Django
 - VueJS
 - RestAPI
 - 全栈开发

---

## 前言

本文为 Cheatsheet 类型文章，用于记录我在日常编程中经常使用的 Django 全栈开发 的一些小经验和踩坑记录。本文没有安装和常识性配置的介绍，仅仅是一笔带过项目中遇到的一些点点滴滴的小问题。算是踩坑和心得笔记吧。

不仅仅是 Django, 还有 Django 涉及到的：
 - 组件：PostgreSQL,RabbitMQ,Redis,MongoDB,Ngnix
 - 技术：爬虫技术，数据库设计，GIS 记录，单页 / 多页 (VueJS+Webpack+DjangoRestFramework), 自动化部署
 - 轮子：Django 紧密关联的可以极大推进项目开发的轮子

<!-- more -->

于是，本文的内容就如下：

 - 前后端分离
 - 自动化部署
 - 数据库相关
 - 其他踩坑经历

<!-- more -->

## 0x01. 前后端分离

前后端分离是提高团队开发的一个重要的开发策略，前后端分离之后，后端和前端交流好 JSON 格式，并行开发，局域网中放置一台服务器，后端写好一个功能，推送代码，由 gitlab 触发 Runner 自动交付到局域网的服务器上。这样的话，前后端可以并行开发，从而摆脱每一次开发过程不可避免，前端编写模板，然后由后端套用模板，出了问题，前端修改模板，后端接着修改模板... 循环往复，不曾更改的问题，在这种职责分明的情况下也不会出现背锅侠的问题。

在往常的开发过程中，而如果 Ajax 比较多或者前端写的代码质量稍微低一些，那么倒霉的事情就发生了，后端和前端的沟通成本那是相当的高。推锅的事情也会发生。

而新的开发过程中，如果上级有界面上的需求，基本上只需要前端更新一下代码，推送，就可以立即看到效果。
同样的，后端也是如此。

> 这就是我选择前后端分离的初衷 -- 将主要的精力放在开发上面。而不是套用模板和编辑 Ajax 过程中带来的沟通问题。

在前后端配合上：

 - 后端选择 Django,Restful 框架选择了 DjangoRestFramework, DRF 的优点在于可以自动生成 API 界面，让前端对照着表单进行请求接口的测试。于是局域网的那一台可以配置为 Debug 模式，生产机器就可以关闭 DEBUG 模式。
 - 前端选择 VueJS, 选择这个小而精美的框架一方面是基于团队的开发水平考虑，如果使用太激进的框架 React, 可能遇到问题无法在短时间内解决。由于选用了 VueJS, 也就选用了 Vue 全家桶，通过 Webpack2 进行配置完成基本的打包任务，通过 config 读取环境变量进行生产环境和发布环境的 apiurl 的分离
 - 代码提交选择 Coding.NET 用于提交代码，在局域网中选择 Gitlab 用于提交代码，配上 Gitlab CI 进行持续集成，每次提交代码直接直接构建本地发布。前后端合作亲密无间。

前后端分离有什么缺点呢？

1. 必须强行升级 Https
2. 开发时候需要关掉 Django 的同源策略
3. IE8-- 不兼容

### 1.1. Django 和 他的小伙伴们

Django 适用于快速开发，对于创业公司来说，是不错的快速开发语言。

不仅仅是因为 Python 表达力比较强，更重要的是 Django 有很多高质量的包可以使用。

 - Django Debug Toolbar
 - DjangoRestFramework
 - Django Extensions

### 1.4. Django 的奇技淫巧

#### Django Model

 - [Save If Changed](http://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed)

## 0x02. 自动化部署

写程序 一般就是开发测试部署。

话虽然这么时候，但是在具体的实践过程中，还是有很多很多坑需要注意的。

比如，仅仅就开发环节来说，团队协作怎么搞？你说可以用 GIT 作为版本管理工具，代码托管。那我问你，这个 Web 开发过程中前端开发模板，后端套用模板怎么搞？你说，前后端分离，那前后端分离后 Http 请求被劫持怎么办，跨站攻击怎么搞......
甚至如果是一个人开发的话，直接拉一台服务器做做部署，定期更新到网站上就行了。但如果是团队协作呢？前端提交了代码，产品经理过来说，你更新一下服务器，后端提交了代码，前端过来说，你更新一下服务器，过程琐碎而耗时。大量的时间就浪费在了这种枯燥的事情上了。两个后端，一个前端的情况下，每天本地发布（交付）的次数就已经是相当惊人（大概是前后端每天提交 5 次左右），如果以后是 3 个后端，三个前端，那我作为主程，每天就写不了代码了，这种情况是断不能忍的。

这个时候，就需要想着把团队协作开发流程优化好：

在我刚开始进行开发的时候，使用 bash 配合 Ansible 在本地和上线的 Ubuntu 16.04 上面自动化能够自动化的大部分工作，程序员在本地开发的时候，只需要进行开发，然后推送代码到 repo, 剩下的诸如自动化测试集成到系统中，则全部自动化。

### 2.1. 使用场景

经过研究，我确定了理想中的使用场景：

> 前端与后端提交代码到代码托管上面的时候，直接集成，构建，Stage 到服务器。

> 到上线的时候，由我执行 Ansible 进行上线。

### 2.2. 实施方案

在这个流程中，我需要安装如下的软件：

 - Gitlab Gitlab-CI-Runner : 用于解决代码托管，项目的基本成长，以及持续化集成
 - PostgreSQL
 - MongoDB
 - Redis
 - RabbitMQ
 - Nginx
 - Python 以及 Python 扩展的依赖包
 - 其他

配置文件为 3 类：
 - test
 - stage
 - production

硬件设备 3 台：

1. 第一台为 Gitlab 部署的软件
2. 第二台为 Stage 环境 （本地局域网持续交付）的机器
3. 第三台为 Server （阿里云） 机器

> 注：最初使用 Ubuntu 机器，最终确定使用 Docker 镜像进行构建

### 2.3. 持续交付

当前端工程师 Push Master 分支到 Repo 上的时候，执行 Job 更新网站
当后端工程师 Push Master 分支到 Repo 上的时候，执行 Job 更新网站

Push Master 分支，这个自然无需多说，问题是怎么执行 Job 呢？

> **Gitlab CI Multi Runner**

在一台 stage 的机器上安装 gitlab ci multi runner , 并且在该机器上注册 runner 为 shell , 这意味着 runner 会以 gitlab-runner 用户的权限进行测试 , 你需要 uninstall
然后 install --user=root 一下，然后重启，即可在 gitlab-ci.yml 上。

修改文件
```bash

gitlab-runner register # 然后填入相关信息
vim /etc/gitlab-runner/config.toml # 接着进行修改
```

```bash
concurrent = 1
check_interval = 0

[[runners]]
  name = "yadjangoweb"
  url = "http://192.168.1.139/ci"
  token = "325asd65f4e7xa9faasda8da"
  executor = "shell"
  [runners.cache]
```

### 2.4. Dockerize Application

Docker 以其轻量级和类似于版本管理的软件方式吸引了我。于是，准备将所有的 Service 都 Docker 化。

拿 Django 程序来说，首先 Django 程序依赖三个组件 redis / postgresql / rabbitmq , 完成这些组件的安装之后才能进行下一步的操作。

## 0x03 数据库相关

### 1. 数据库设计

PostgreSQL Array 在爬虫方面可以用来标记一个 Record 的处理状态
PostgreSQL Range 用来判断范围也是一个比较高效的选择（用空间 gist 索引取代两个索引）

GeoDjango 和 PostGIS 非常配

### 2. 数据迁移

#### 1.1. 第一次数据迁移之 MySQL 转 PostgreSQL

第一次数据迁移的时候基于 PostgreSQL 社区里面有个大杀器，叫做 PostGIS, 通过 PostGIS, 可以很方便的拥有和国内一些地图公司匹敌的算法。抛开算法实现的效率问题，基本上可以满足日常的开发需求，当时数据量不算大，使用 mysqldump 下来也就 500M 左右，而且行数大约 700W 条，于是使用了一个很笨的方法，就是将数据库使用 Django 命令 dump 成 json, 接着修改配置重新导入新数据库。

这种方式的缺点就是效率低而且太吃内存了，当时 16G 的服务器满内存，满交换内存地搞了一个上午。

#### 1.2. 第二次数据迁移之重新 makemigrations

为什么要重新 makemigrations 呢，因为糟糕的事情发生了。

有个需求，需要重新定制用户登录认证系统。用户登录认证系统是最最应该在项目开始的时候编写的，这就是项目的基石，这个需求就恰似在房子盖到第三层的时候突然要把地基给加固。

Django 中如果使用了 auth 模块，则 auth.user 是最先被迁移到数据库中的，而如果你经过权衡继承 AbstractUser 并且 makemigrations 生成个迁移文件 0001_initial.py 后，在正常的情况下不容易将 migration 修改应用到数据库中。

> 如果我偏要勉强呢？

当然是可以勉强的，删掉数据库中已经记录下来的 auth.user migration 的相关记录即可。

那我为什么还是需要重新编写 migration 呢？

1. 因为之前对数据库的结构调整比较频繁，多达 138 次，而在 138 次调整数据结构之后，再去撤销第一次数据表的迁移操作的时候，则无异于厨子做菜要把牛排做 8 分熟，但是厨子做到 7 分熟的时候，突然顾客说，我要 5 分熟的牛排。那只能重新来了。
2. 顺手精简掉 138 个文件。

如何做呢？

1. 数据的迁移在没有表与表之间的关联的时候是很好办的，CSV, 标准 SQL 文件。
2. 有表关联的情况下则需要权衡数据量来进行迁移，假如数据量在 10 来个 G 的时候，读到内存中，按照数据表的依赖关系，自下而上逐层迁移即可。
3. 数据量大的时候，则需要去约束，去索引，然后转 CSV/SQL, 迁移到数据表中。如果表依赖不复杂的话，直接 psql 命令重定向数据也可以。

但是呢，由于使用了 Django, 在数据量不大的时候，完全可以使用 Django 的 ORM 来做迁移。

我在 Google 了一下，发现下面一个脚本，于是设置数据库为新数据库 default 和 depressed

```python
def batch_migrate(model):
    # remove data from destination db before copying
    # to avoid primary key conflicts or mismatches
    if model.objects.using('default').exists():
        model.objects.using('default').all().delete()

    # get data form the source database
    items = model.objects.using('depressed').order_by("pk").all()
    count = len(items)
    # process in chunks, to handle models with lots of data
    for i in range(0, count, 10000):
        chunk_items = items[i:i + 10000]
        print("已经迁移数据", i)
        model.objects.using('default').bulk_create(chunk_items)

    # many-to-many fields are NOT handled by bulk create; check for
    # them and use the existing implicit through models to copy them
    for m2mfield in model._meta.many_to_many:
        m2m_model = getattr(model, m2mfield.name).through
        batch_migrate(m2m_model)
```

按照表与表之间的依赖关系，逐个迁移到数据库中搞定。

### 1.3 sequence 问题

在写 Django 的时候发现的时候无论如何都无法保存新的 item.

原来的代码为：

```python
item = Item.objects.get_or_create()
item.foo = 1
item.save()
```
报错信息是 Integrety, 报 duplicated 错误（下面的代码当然是打了马赛克了）

```python
django.db.utils.IntegrityError: duplicate key value violates unique constraint "foo_item_pkey"
DETAIL:  Key (id)=(111111) already exists.
```

那么，问题来了：

> ~~挖掘技术哪家强？~~

啊，不是

> How To Solve This?

经过猜测，而 get 到已有的 item 设置并且保存的话，并不会出现这个问题。问题主要出在 create 上面。

于是编写代码验证一下是不是猜想正确

```python
try:
    item = Item.objects.get()
except Exception:
    item = Item.objects.create()

# do something

item.save()
```

duplicate 的问题肯定是多次存同样的不能重复的字段。

**但尼玛，我之前做测试的时候考虑过这个逻辑呀？**换而言之，这种问题不应该出现，如果出现了问题，八成是 ORM 用的不对。

印象中这种问题 Google 一下 Integrety Duplicate Django PostgreSQL 一般就能出来了。

最后找到解决方案：http://centoshowtos.org/web-services/django-and-postgres-duplicate-key/

在终端进入 psql 查询 sequence 最新值

```sql
select start_value, last_value, max_value from dt_crawler_item_item_id_seq;

 start_value | last_value |      max_value
-------------|------------|---------------------
           1 |    111110 | 9223372036854775807
```

而我们查看一下 item\_id 的最大值

```
select max(item_id) from app_model_item;

   max
---------
 111111
```

重置 sequence last_value 值到最新即可。

```
alter sequence app_model_item_item_id_seq restart with 111111;
```

> 当数据库每次插入一条非指定主键的记录，则获取 last_value(111110), 加 1 得到当前的主键接着插入。但这个过程无异于数据库中已经有了一个 pk 为 111111 的记录，再插入一条。于是报错。

回顾这个问题，该问题是由于 PostGres 的 sequence 造成 pkey 相等，换而言之，postgres 应该在有一个 pk 值为 111111 的时候，插入一个无主键的记录，PostgreSQL 获取 sequence+1(111110 + 1) 得到它认为当前的主键值，接着再一次插入了主键为 111111 的这个值。

这个过程相当于依次插入两个条 ID 相同的记录。
```sql
INSERT INTO table(id, column2, …) VALUES (111111, value2, …);
INSERT INTO table(id, column2, …) VALUES (111111, value2, …);
```

> sequence 避免了每一次 max 查找带来的性能损失，一方面带来了方便，也带来了隐藏的坑。

如果以后这个问题比较多的话，参考下面的源码对文本进行修改。

https://github.com/ASKBOT/django-postgresql-fix-sequences/blob/master/postgresql_sequence_utils/utils.py

## 0x04 WebServer

目前使用的 WebServer 是用 Nginx 做反向代理，将请求通过 unix socket 转发到 gunicorn，gunicorn 作为 django 实际上的 webserver。

### unix socket 和 gunicorn 的 REMOTE_ADDR 问题

Django Admin 模块在访问 某个页面的时候特别特别慢，而在我的机器上一切正常，我怀疑的是数据库的问题，于是，那么首先要知道数据库的查询语句，于是想借用 django debug toolbar 来 profiling, 于是问题来了，我在局域网模拟真机环境，结果无论如何都无法呈现 Django Debug Toolbar,

问题八成出现在 Django 配置环境 或者 Nginx 上面（当然，最后发现是 Gunicorn 的锅）. 在

经过一段时间的排查，认为是 Nginx 的问题，在相关配置添加下面设置 Header,

```python
proxy_set_header X-Forwarded-For $remote_addr;
```

结果依旧无法获取 request.Meta["REMOTE-ADDR"]

经过搜索发现不止我一个人的问题：https://github.com/benoitc/gunicorn/issues/797

最后发现是 Http 请求从 nginx 这儿经过 unix socket 转发到 gunicorn.sock 下默认是没有赋值 REMOTE-ADDR 的，

那么，这个在 HTTP Header 层次的东西，没有在 gunicorn 层次解决，那就只能在 django 层次解决。

给 Django 添加中间件如下，放在 djangodebugtools 的前面。
```python
class XForwardedForMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.META.get("HTTP_X_FORWARDED_FOR", False):
            request.META["HTTP_X_PROXY_REMOTE_ADDR"] = request.META["REMOTE_ADDR"]
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(",", 1)
            request.META["REMOTE_ADDR"] = parts[0]
```

解决。

### Nginx Gzip 压缩

当 json 数据量比较大的时候，则必须要考虑开启压缩。一般情况下，虽然这个可以在 Django 层次完成，但是这么做还不如在 nginx 层次完成。

```python
    gzip on;
    gzip_disable "msie6";
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/x-javascript text/xml application/xml application/xml+rss text/javascript;
```

开启之后，我这边的 一个 220k 的数据缩减到 54k

## 0x04. 其他踩坑相关

### 4.1 奇怪的文件问题

在某一天遇到了一个问题 往常的时候，当文件上传到 Django 中的时候，都可以正常的解析，但是这两天居然不能用了。

```python
# 问题代码出现在
df = pd.read_excel(file_obj)
# 报这个问题 google 几乎没有什么解决方案
Invalid file path or buffer object type
<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
```

更加糟糕的问题出现了，我本人的开发环境和服务器的开发环境基本一致，但，但，但为什么不能用呢？

分别回滚代码，Nginx 设置，在线上打 Log, 最终确定了是 Pandas 从 0.19 升级到了 0.20 之后出现的一个小问题。最终还原线上 python 安装环境，搞定。


