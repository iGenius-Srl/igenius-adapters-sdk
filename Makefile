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