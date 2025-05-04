SHELL=/bin/bash

UI := $(shell id -u)
GID := $(shell id -g)
MAKEFLAGS += -s
DOCKER_COMPOSE_PREFIX = HOST_UID=${UID} HOST_GID=${GID} docker compose -f docker-compose.dev.yml

.DEFAULT_GOAL := help

.PHONY: init
init: ## Initialize the project
	$(MAKE) install-pre-commit
	cd frontend && npm install && cd -
	cd backend && uv sync &&  cd -

.PHONY: install-pre-commit
install-pre-commit: ## Install pre-commit
	pre-commit install

.PHONY: db-up
db-up: ## Spin up DB and other services
	${DOCKER_COMPOSE_PREFIX} up -d postgres adminer  httpbin

.PHONY: dev
dev: ## Spin up dev (frontend & backend parallel using xargs)
	$(MAKE) db-up
	@echo "Starting frontend and backend in parallel using xargs..."
	# Use printf to feed commands line by line to xargs
	# -P 2 runs up to 2 processes in parallel
	# -I {} substitutes the command line
	# sh -c 'eval "$$1"' executes the command string in a shell
	# xargs should handle signal propagation (Ctrl+C) to children
	printf '%s\n' \
		"cd frontend && npm run dev" \
		"cd backend && uv run python manage.py runserver 0.0.0.0:5000" | \
	xargs -P 2 -I {} sh -c 'eval "$$1"' - {}
	@echo ">>> Development servers stopped."

.PHONY: api-py-shell
api-py-shell: ## Open python shell in API container
	uv run python manage.py shell

.PHONY: migrate
migrate: ## Run migrations
	cd backend && uv run python manage.py migrate

.PHONY: clean
clean: ## Perform cleanup
	cd frontend && rm -rf node_modules && cd -
	cd backend && rm -rf .venv && cd -
	@echo ">>> Cleaned up frontend and backend directories."

.PHONY: gen-openapi-schema
gen-openapi-schema: ## Generate openapi schema
	uv run python manage.py generateschema --file openapi-schema.yml

.PHONY: help
help: ## Disply this help
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(BCYAN)%-35s$(NC)%s\n", $$1, $$2}'
