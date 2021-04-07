SHELL = bash

DOCS_BUCKET_NAME=crystal-web-connectors-docs
DOCS_BUCKET_PREFIX=sdk
DOCS_VERSION?=latest

.PHONY: docs-build
docs-build:
	poetry run mkdocs build

.PHONY: docs-serve
docs-serve:
	poetry run mkdocs serve

.PHONY: docs-deploy
docs-deploy:
	gsutil rsync -r ./site/ "gs://${DOCS_BUCKET_NAME}/${DOCS_BUCKET_PREFIX}/${DOCS_VERSION}/"

.PHONY: test
test: ## run all tests
	poetry run pytest tests --cov-report term-missing --cov=src

###########
# Release #
###########
CHANGELOG ?= CHANGELOG.md
SERVICE_VERSION = `cat pyproject.toml | grep "^version =" | cut -f 3 -d ' ' | cut -d '"' -f 2`

.PHONY: bump
bump:
	poetry version $(INCREMENT)

.PHONY: changelog
changelog:
	git-chglog -o $(CHANGELOG) -next-tag v$(SERVICE_VERSION)

.PHONY: release
release: test
	$(MAKE) bump INCREMENT=$(INCREMENT)
	$(MAKE) changelog
	git add . && git commit -m "Bump to v$(SERVICE_VERSION)" && git tag -a "v$(SERVICE_VERSION)" -m $(SERVICE_VERSION)

.PHONY: major
major: ## release a new major
	$(MAKE) release INCREMENT='major'

.PHONY: minor
minor: ## release a new minor
	$(MAKE) release INCREMENT='minor'

.PHONY: patch
patch: ## release a new patch
	$(MAKE) release INCREMENT='patch'

###########
# Linting #
###########

MAX_COMPLEXITY ?= 10
LINE_LENGTH ?= 120
FLAKE8_EXCLUDE_DIRS ?= .venv

.PHONY: lint
lint: ## lint code [toolchain style]
	poetry run flake8 --exclude=${FLAKE8_EXCLUDE_DIRS} --extend-ignore=E203 --max-complexity=$(MAX_COMPLEXITY) --max-line-length=$(LINE_LENGTH) .
	# E203 issue: https://github.com/PyCQA/pycodestyle/issues/373
	## format check [toolchain style]
	poetry run isort --line-width=$(LINE_LENGTH) --multi-line=3 --trailing-comma --atomic --skip-gitignore --check-only --diff --stdout .
	poetry run black --check --diff --line-length=$(LINE_LENGTH) .

.PHONY: format
format: ## format code [toolchain style]
	poetry run isort --line-width=$(LINE_LENGTH) --multi-line=3 --trailing-comma --atomic --skip-gitignore .
	poetry run black --line-length=$(LINE_LENGTH) .
	