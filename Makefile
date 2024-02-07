SHELL=/bin/bash

UI := $(shell id -u)
GID := $(shell id -g)
MAKEFLAGS += -s
DOCKER_COMPOSE_PREFIX = HOST_UID=${UID} HOST_GID=${GID} docker-compose -f docker-compose.dev.yml

.DEFAULT_GOAL := help

.PHONY: db-up
db-up: ## Spin up DB and other services
	${DOCKER_COMPOSE_PREFIX} up -d postgres adminer gotify httpbin

.PHONY: db-down
db-down: ## Spin down DB and other services
	${DOCKER_COMPOSE_PREFIX} rm -fsv postgres adminer gotify httpbin

.PHONY: moni-up
moni-up: ## Build and run moni
	$(MAKE) db-up
	${DOCKER_COMPOSE_PREFIX} up --build moni

.PHONY: moni-down
moni-down: ## Stop and remove moni
	$(MAKE) db-down
	${DOCKER_COMPOSE_PREFIX} rm -fsv moni

.PHONY: api-up
api-up: ## Spin up API
	$(MAKE) db-up
	${DOCKER_COMPOSE_PREFIX} up api

.PHONY: api-down
api-down: ## Spin down API
	${DOCKER_COMPOSE_PREFIX} rm -fsv api

.PHONY: api-py-shell
api-py-shell: ## Open python shell in API container
	${DOCKER_COMPOSE_PREFIX} exec api python manage.py shell

.PHONY: api-shell
api-shell: ## Open shell in API container
	${DOCKER_COMPOSE_PREFIX} exec api bash

.PHONY: build-api
build-api: ## Build API
	${DOCKER_COMPOSE_PREFIX} build --no-cache api 

.PHONY: build-ui
build-ui: ## Build UI
	${DOCKER_COMPOSE_PREFIX} build --no-cache ui

.PHONY: ui-up
ui-up: ## Spin up UI
	${DOCKER_COMPOSE_PREFIX} up ui

.PHONY: ui-down
ui-down: ## Spin down UI
	${DOCKER_COMPOSE_PREFIX} rm -fsv ui

.PHONY: app-up
app-up: ## Spin up UI and API
	$(MAKE) db-up
	${DOCKER_COMPOSE_PREFIX} up ui api

.PHONY: app-down
app-down: ## Spin down UI and API
	$(MAKE) db-down
	${DOCKER_COMPOSE_PREFIX} rm -fsv ui api

.PHONY: gen-openapi-schema
gen-openapi-schema: ## Generate openapi schema
	${DOCKER_COMPOSE_PREFIX} exec api python manage.py generateschema --file openapi-schema.yml
	docker cp api:/app/openapi-schema.yml openapi-schema.yml 

.PHONY: help
help: ## Disply this help
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BCYAN)%-35s$(NC)%s\n", $$1, $$2}'