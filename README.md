# YaDjangoBlog

![build](https://img.shields.io/travis/twocucao/YaDjangoWeb.svg)
![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![celery](https://img.shields.io/badge/celery-5.0.2-4BC51D.svg)
![pypi](https://img.shields.io/pypi/v/nine.svg)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/twocucao/YaDjangoWeb/issues)

> Yet Another Django Blog 是的，这是另一个 Django Blog 应用

为什么不容错过?

- 这是笔者工作之余用于练手的项目
- 是引入新技术试验场所
- 也是 **全干**工程师 (Full Stuff Engineer) 的最新的 DevOps 思考成果

## 技术栈

- 开发与部署环境为 Docker
- Python 3.9.5
- 前端 Vue + Vite + axios
- 后端 [Django 3.0](https://github.com/django/django)
    + [DjangoRestFramework](https://github.com/tomchristie/django-rest-framework/) + Celery
- 自动化部署选用工具 Ansible 以及 Docker
- 后端组件
    - ElasticSearch 用于搜索和推荐
    - PostgreSQL 用于数据持久化
    - Redis 用于 Session / 和缓存
    - RabbitMQ 分布式队列 / 定时任务
    - Nginx 用于反向代理

如果你也是追新的 Django 开发者，一起来提 PR;

![pic alt](https://camo.githubusercontent.com/af66ed3ad2d9fd159b9f5fdc92ba0a1804cff642/68747470733a2f2f692e696d6775722e636f6d2f4766746846417a2e706e67)

## 特别感谢

- ansible django stack: https://github.com/jcalazan/ansible-django-stack
- cookiecutter-django: https://github.com/pydanny/cookiecutter-django
- djangopackages: https://github.com/djangopackages/djangopackages
- 董伟明 关于 ElasticSearch
  的几篇文章 http://www.dongwm.com/archives/%E7%9F%A5%E4%B9%8ELive%E5%85%A8%E6%96%87%E6%90%9C%E7%B4%A2%E4%B9%8B%E4%BD%BF%E7%94%A8Elasticsearch%E6%90%9C%E7%B4%A2/
- 各个组件的开发者们
    - ElasticSearch
    - PostgreSQL
    - Redis
    - RabbitMQ
    - Nginx
    - Docker

> Created by Micheal Gardner http://twocucao.xyz Since 2017.02

## 许可

MIT

