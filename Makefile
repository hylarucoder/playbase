.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"
PG_DOCKER_RUN := docker exec -i -t yadjangoblog_postgres_1
DJANGO_DOCKER_RUN := docker exec -i -t yadjangoblog_django_1
DJANGO_DOCKER_PATH_RUN := docker exec -i -t yadjangoblog_django_1

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

sep--sep-a: ## ========== 开发时命令 ==============

django-build-up: ## build and compose up
	docker-compose -f dev.yml build && docker-compose -f dev.yml up

force_djnago_build-up: ## django / pg / es
	docker-compose -f dev.yml build --no-cache  && docker-compose -f dev.yml up

django-before-up: ## some deamons
	docker-compose -f dev.yml up -d redis postgres mailhog elasticsearch rabbitmq celeryflower

django-runserver: ## runserver
	docker-compose -f dev.yml up django

django-celerybeat: ## celerybeat
	docker-compose -f dev.yml up celerybeat

django-celeryworker: ## celeryworker
	docker-compose -f dev.yml up celeryworker

django-celeryflower: ## celeryflower
	docker-compose -f dev.yml up celeryflower

django-just-up: ## build and up
	docker-compose -f dev.yml up

django-manager: ## Enter python manage.py
	$(DJANGO_DOCKER_RUN) python manage.py

django-import-articles: ## Enter python manage.py
	$(DJANGO_DOCKER_RUN) python manage.py import_hexo_source

django-console: ## Enter Django Console
	$(DJANGO_DOCKER_RUN) python manage.py shell

shell: ## Enter Shell
	$(DJANGO_DOCKER_RUN) /bin/bash

dbshell: ## Enter psql as postgres
	$(PG_DOCKER_RUN) su postgres -c "psql -U yadjangoblog"

sep--sep-b: ## ========== 测试与代码质量 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

lint: ## check style with flake8
	$(DJANGO_DOCKER_RUN) flake8 yadjangoblog tests

test: ## run tests quickly with the default Python
	$(DJANGO_DOCKER_PATH_RUN) py.test --html=test_report.html --self-contained-html

coverage: ## check code coverage quickly with the default Python
	$(DJANGO_DOCKER_PATH_RUN) py.test tests/ --cov=yadjangoblog

sep--sep-c: ## ========== 文档生成相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/source/yadjangoblog.rst
	rm -f docs/source/yadjangoblog/*
	rm -f docs/source/modules.rst
	find ./yadjangoblog/  -maxdepth 1 -not -name "*template" -not -name "*static" -not -name "*__pycache__*" -not -name 'yadjangoblog' -exec sphinx-apidoc -o docs/source/yadjangoblog"{}" \;
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

sep--sep-d: ## ========== 程序发布相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

release: clean ## package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install

sep--sep-e: ## ========== Docker 镜像相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

build-postgres: ## > Postgres
	docker build -t 'db-postgres:0.1' -f 'compose/postgres/Dockerfile-dev' .

force-build-postgres: ## > Postgres
	docker build -t 'db-postgres:0.1' -f 'compose/postgres/Dockerfile-dev' --no-cache .

build-ubuntu: ## > base ubuntu
	docker build -t 'base-ubuntu:0.1' -f 'compose/django/Dockerfile-dev-base' .

force-build-ubuntu: ## > base ubuntu
	docker build -t 'base-ubuntu:0.1' -f 'compose/django/Dockerfile-dev-base' --no-cache .

build-django: ## > base django
	docker build -t 'base-django:0.1' -f 'compose/django/Dockerfile-dev' .

force-build-django: ## > base django
	docker build -t 'base-django:0.1' -f 'compose/django/Dockerfile-dev' --no-cache .

build-elasticsearch: ## > base elasticsearch
	docker build -t 'base-elasticsearch:0.1' -f 'compose/elasticsearch/Dockerfile-dev' .

force-build-elasticsearch: ## > base elasticsearch
	docker build -t 'base-elasticsearch:0.1' -f 'compose/elasticsearch/Dockerfile-dev' . --no-cache

build-all: build-postgres build-ubuntu build-django build-elasticsearch ## > build 所需所有镜像

sep--sep-f: ## ========== 文件清理相关 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

