# playbase

![build](https://img.shields.io/travis/hylarucoder/playbase.svg)
![pyversions](https://img.shields.io/badge/python%20-3.11%2B-blue.svg)
![celery](https://img.shields.io/badge/celery-5.0.2-4BC51D.svg)
![pypi](https://img.shields.io/pypi/v/nine.svg)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-ff69b4.svg)](https://github.com/twocucao/YaDjangoWeb/issues)

## 技术栈

- 开发与部署环境为 Docker
- Python 3.11.8
- 前端 tailwind css + HTMX
- 后端 [Django 5.0](https://github.com/django/django) + RQ
- 后端组件
    - ElasticSearch 用于搜索和推荐
    - PostgreSQL 用于数据持久化
    - Redis 用于 Session / 和缓存
    - Nginx 用于反向代理

如果你也是追新的 Django 开发者，一起来提 PR;

## 特别感谢

- cookiecutter-django: https://github.com/pydanny/cookiecutter-django
- djangopackages: https://github.com/djangopackages/djangopackages
- 董伟明 关于 ElasticSearch 的几篇文章 http://www.dongwm.com/archives/%E7%9F%A5%E4%B9%8ELive%E5%85%A8%E6%96%87%E6%90%9C%E7%B4%A2%E4%B9%8B%E4%BD%BF%E7%94%A8Elasticsearch%E6%90%9C%E7%B4%A2/
- 各个组件的开发者们 ElasticSearch PostgreSQL Redis Nginx Docker

> Created by hylarucoder http://hylarucoder.xyz Since 2017.02

## license

MIT

