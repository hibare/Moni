SHELL=/bin/bash

UI := $(shell id -u)
GID := $(shell id -g)
MAKEFLAGS += -s
DOCKER_COMPOSE_PREFIX = HOST_UID=${UID} HOST_GID=${GID} docker compose -f docker-compose.dev.yml

.DEFAULT_GOAL := help

.PHONY: db-up
db-up: ## Spin up DB and other services
	${DOCKER_COMPOSE_PREFIX} up -d postgres adminer  httpbin

.PHONY: moni-up
moni-up: ## Build and run moni
	$(MAKE) db-up
	${DOCKER_COMPOSE_PREFIX} up --build moni

.PHONY: build-dev
build-dev: ## Build Dev
	${DOCKER_COMPOSE_PREFIX} build --no-cache api
	${DOCKER_COMPOSE_PREFIX} build --no-cache ui

.PHONY: dev
dev: ## Spin up dev
	${DOCKER_COMPOSE_PREFIX} up ui api

.PHONY: api-py-shell
api-py-shell: ## Open python shell in API container
	${DOCKER_COMPOSE_PREFIX} exec api python manage.py shell

.PHONY: api-shell
api-shell: ## Open shell in API container
	${DOCKER_COMPOSE_PREFIX} exec api bash

.PHONY: clean
clean: ## Perform cleanup
	${DOCKER_COMPOSE_PREFIX} down --remove-orphans
	${DOCKER_COMPOSE_PREFIX} rm -f
	${DOCKER_COMPOSE_PREFIX} volume prune -f
	${DOCKER_COMPOSE_PREFIX} network prune -f

.PHONY: gen-openapi-schema
gen-openapi-schema: ## Generate openapi schema
	${DOCKER_COMPOSE_PREFIX} exec api python manage.py generateschema --file openapi-schema.yml
	docker cp api:/app/openapi-schema.yml openapi-schema.yml

.PHONY: help
help: ## Disply this help
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BCYAN)%-35s$(NC)%s\n", $$1, $$2}'
