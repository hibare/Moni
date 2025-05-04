FROM python:3.13.3-slim AS base

# Build frontend assets

FROM node:23 AS frontend

ENV NODE_OPTIONS=--openssl-legacy-provider \
    BUILD_DIR=/frontend

WORKDIR ${BUILD_DIR}

COPY ./frontend/package*.json ${BUILD_DIR}/

RUN npm install

COPY ./frontend ${BUILD_DIR}

RUN npm run build

# Build backend deps

FROM base AS builder

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    rustc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache \
    --mount=type=bind,source=backend/uv.lock,target=uv.lock \
    --mount=type=bind,source=backend/pyproject.toml,target=pyproject.toml \
    uv sync \
    --locked \
    --no-dev \
    --no-install-project

# Build final image

FROM base

ENV USER=ghost

ENV APP_DIR=/home/${USER}/app

# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y libpq5 --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd -ms /bin/bash ${USER}

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

CMD ["sh", "entrypoint.sh"]
