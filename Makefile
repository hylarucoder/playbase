.PHONY:  help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-30s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clear:
	@rm -rf build dist

build-wheel: ## build
	rm -rf build dist
	poetry build -f wheel

flake8: ## lint
	poetry run flake8 playbase

mypy: ## mypy
	poetry run mypy playbase

publish: ## publish package to pypi
	poetry publish --build

test: ## test
	docker-compose run --rm playbase-toolbox-test bash -c "python -m pytest tests"

test.verbose: ## test.verbose
	docker-compose run --rm playbase-toolbox-test bash -c "python -m pytest tests -v --pdb --pdbcls=IPython.terminal.debugger:Pdb"

format: ## publish package to pypi
	ruff format .

collectstatic:
	docker-compese run --rm playbase-toolbox bash -c "djcli collectstatic"

shell_plus:
	docker-compose run --rm playbase-toolbox bash -c "djcli shell_plus"

db.makemigrations:
	docker-compose run --rm playbase-toolbox bash -c "djcli makemigrations"

db.migrate:
	docker-compose run --rm playbase-toolbox bash -c "djcli migrate"

docker-build: ## build and compose up
	docker-compose build && docker-compose up

docker-build-no-cache: ## build --no-cache
	docker-compose build --no-cache  && docker-compose up

start: ## runserver
	docker-compose run --rm --service-ports playbase-web

beat: ## beat
	docker compose up celerybeat

worker: ## worker
	docker compose up celeryworker

flower: ## flower
	docker compose up celeryflower

up: ## build and up
	docker compose up

import-articles: ## Enter python manage.py
	$(DJANGO_DOCKER_RUN) python manage.py import_hexo_source

sep--sep-b: ## ========== 测试与代码质量 ==============
	echo "## ========== 本行只是优雅的分割线  ==============="


coverage: ## check code coverage quickly with the default Python
	$(DJANGO_DOCKER_PATH_RUN) pytest tests/ --cov=playbase

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

build-playbase: ## > playbase
	docker build -t 'playbase:local' -f 'compose/app/Dockerfile' .

build-playbase-no-cache: ## > playbase
	docker build -t 'playbase:local' -f 'compose/app/Dockerfile' --no-cache .

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

