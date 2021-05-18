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
PG_DOCKER_RUN := docker exec -i -t mipha_postgres_1
DJANGO_DOCKER_RUN := docker exec -i -t mipha_django_1
DJANGO_DOCKER_PATH_RUN := docker exec -i -t mipha_django_1

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

sep--sep-a: ## ========== 开发时命令 ==============

docker-build: ## build and compose up
	docker compose build && docker-compose up

docker-build-no-cache: ## django / pg / es
	docker compose build --no-cache  && docker-compose up

before-up: ## some deamons
	docker compose up -d redis postgres mailhog elasticsearch rabbitmq celeryflower

start: ## runserver
	docker compose up django

beat: ## beat
	docker compose up celerybeat

worker: ## worker
	docker compose up celeryworker

flower: ## flower
	docker compose up celeryflower

up: ## build and up
	docker compose up

django-manager: ## Enter python manage.py
	$(DJANGO_DOCKER_RUN) python manage.py

django-import-articles: ## Enter python manage.py
	$(DJANGO_DOCKER_RUN) python manage.py import_hexo_source

django-console: ## Enter Django Console
	$(DJANGO_DOCKER_RUN) python manage.py shell

shell: ## Enter Shell
	$(DJANGO_DOCKER_RUN) /bin/bash

dbshell: ## Enter psql as postgres
	$(PG_DOCKER_RUN) su postgres -c "psql -U mipha"

sep--sep-b: ## ========== 测试与代码质量 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="

lint: ## check style with flake8
	$(DJANGO_DOCKER_RUN) flake8 mipha tests

test: ## run tests quickly with the default Python
	$(DJANGO_DOCKER_PATH_RUN) py.test --html=test_report.html --self-contained-html

coverage: ## check code coverage quickly with the default Python
	$(DJANGO_DOCKER_PATH_RUN) py.test tests/ --cov=mipha

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

build-mipha: ## > mipha
	docker build -t 'mipha:local' -f 'compose/django/Dockerfile' .

build-mipha-no-cache: ## > mipha
	docker build -t 'mipha:local' -f 'compose/django/Dockerfile' --no-cache .

build-elasticsearch: ## > elasticsearch
	docker build -t 'elasticsearch:local' -f 'compose/elasticsearch/Dockerfile-dev' .

build-elasticsearch-no-cache: ## > elasticsearch
	docker build -t 'elasticsearch:local' -f 'compose/elasticsearch/Dockerfile-dev' . --no-cache

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

