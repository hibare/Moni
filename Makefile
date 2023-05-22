SHELL=/bin/bash

UI := $(shell id -u)
GID := $(shell id -g)
MAKEFLAGS += -s
DOCKER_COMPOSE_PREFIX = HOST_UID=${UID} HOST_GID=${GID} docker-compose -f docker-compose.dev.yml

db-up:
	${DOCKER_COMPOSE_PREFIX} up -d postgres adminer gotify httpbin

db-down:
	${DOCKER_COMPOSE_PREFIX} rm -fsv postgres adminer gotify httpbin

api-up: db-up
	${DOCKER_COMPOSE_PREFIX} up api

api-down:
	${DOCKER_COMPOSE_PREFIX} rm -fsv api

api-py-shell:
	${DOCKER_COMPOSE_PREFIX} exec api python manage.py shell

api-shell:
	${DOCKER_COMPOSE_PREFIX} exec api bash

gen-openapi-schema:
	${DOCKER_COMPOSE_PREFIX} exec api python manage.py generateschema --file openapi-schema.yml
	docker cp api:/app/openapi-schema.yml openapi-schema.yml 