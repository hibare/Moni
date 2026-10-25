# syntax=docker/dockerfile:1.7

FROM python:3.14.9-slim@sha256:35caba83af2fe6da9a5d922f9b0156f21d1246a48278c58a08bd253303ba42e8 AS base

# =============================================================================
# Frontend
# =============================================================================

FROM --platform=$BUILDPLATFORM node:26-slim@sha256:a1d9d671994fc2d26e297ac56b4b1522a8bc7fa71c43b14cd1b1fe6c5116f7dc AS frontend

ARG TARGETOS
ARG TARGETARCH

WORKDIR /frontend

ENV CI=true \
    NODE_OPTIONS=--openssl-legacy-provider

# Copy dependency manifests first for maximum cache reuse.
COPY frontend/package*.json ./

# Install dependencies in a way that keeps the dependency cache warm.
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY frontend/ ./

RUN npm run build

# =============================================================================
# Backend Dependencies
# =============================================================================

FROM base AS builder

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Build dependencies only.
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        libffi-dev \
        libpq-dev \
        libssl-dev \
        python3-dev \
        rustc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install UV
# hadolint ignore=DL3013
RUN pip install uv --no-cache-dir

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /opt

# Keep Python dependency resolution independently cacheable.
RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync \
    --locked \
    --no-dev \
    --no-install-project

# =============================================================================
# Runtime
# =============================================================================

FROM base

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

ENV USER=ghost
ENV APP_DIR=/home/${USER}/app

# Runtime dependencies only.
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        libpq5 \
    && update-ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/.venv /opt/.venv

ENV PATH="/opt/.venv/bin:$PATH"

RUN useradd -ms /bin/bash ${USER}

# hadolint ignore=DL3066
USER ${USER}

RUN mkdir -p ${APP_DIR}

WORKDIR ${APP_DIR}

COPY --chown=${USER}:${USER} backend .

# Copy assets
COPY --from=frontend --chown=${USER}:${USER} /frontend/dist/static ${APP_DIR}/moni/assets/static/

# Copy templates
COPY --from=frontend --chown=${USER}:${USER} /frontend/dist/*.html ${APP_DIR}/moni/assets/templates

# Copy favicon
COPY --from=frontend --chown=${USER}:${USER} /frontend/dist/favicon.png ${APP_DIR}/moni/assets/static/img/

RUN python manage.py collectstatic --no-input

EXPOSE 8000

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=5s \
    --retries=3 \
    CMD ["curl", "-f", "http://localhost:8000/__health/"]

CMD ["sh", "entrypoint.sh"]
