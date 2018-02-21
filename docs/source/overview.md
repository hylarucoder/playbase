# YaDjangoBlog

> Yet Another Django Blog

> 是的，这是另一个 Django Blog 应用

> Created by Micheal Gardner http://twocucao.xyz Since 2017.02

![build](https://img.shields.io/travis/twocucao/YaDjangoWeb.svg)
![react](https://img.shields.io/badge/style-flat-green.svg?react=15.6)
![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![celery](https://img.shields.io/badge/celery-4.0.2-4BC51D.svg)
![pypi](https://img.shields.io/pypi/v/nine.svg)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/twocucao/YaDjangoWeb/issues)

工作之余用于练手的项目， 也是我给公司引入新技术之前用来测试新技术的一个试验场所。 也是我作为**全干**工程师 (Full Stuff Engineer) 的最新的 DevOps 思考成果。

## 技术栈

 - 开发与部署环境为 Docker
 - Python 3.5.2
 - 前端 Vue + Webpack + ES2015 + axios
 - 后端 [Django 2.0](https://github.com/django/django) + [DjangoRestFramework](https://github.com/tomchristie/django-rest-framework/) + Celery
 - ~~自动化部署选用工具 Ansible~~ 已经改用 Docker 啦
 - 后端组件
   - ElasticSearch 用于搜索和推荐
   - PostgreSQL 用于数据持久化
   - Redis 用于 Session / 分布式队列 / 定时任务
   - Nginx 用于反向代理

如果你也是追新的 Django 开发者，一起来提 PR;

![pic alt](https://camo.githubusercontent.com/af66ed3ad2d9fd159b9f5fdc92ba0a1804cff642/68747470733a2f2f692e696d6775722e636f6d2f4766746846417a2e706e67)

## 特别感谢

- ansible django stack: https://github.com/jcalazan/ansible-django-stack
- djangopackages: https://github.com/djangopackages/djangopackages
- cookiecutter-django: https://github.com/pydanny/cookiecutter-django

## 许可

MIT


