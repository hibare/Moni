FROM python:3.11.0rc2-slim as base

LABEL Github="hibare"

# Build frontend assets

FROM node as frontend

ENV NODE_OPTIONS=--openssl-legacy-provider

ENV BUILD_DIR=/frontend

WORKDIR ${BUILD_DIR}

COPY ./frontend/package*.json ${BUILD_DIR}/

RUN npm install

COPY ./frontend ${BUILD_DIR}

RUN npm run build

# Build backend deps

FROM base as builder

RUN apt-get update && apt-get install -y build-essential python3-dev libpq-dev libssl-dev libffi-dev rustc

COPY backend/requirements.txt .

RUN pip install -U pip setuptools wheel && pip install -r requirements.txt 

# Build final image

FROM base

ENV USER=ghost

ENV APP_DIR=/home/${USER}/app

RUN apt-get update && apt-get install -y libpq5 

COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY --from=builder /usr/local/lib/ /usr/local/lib/

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
COPY --from=frontend --chown=${USER}:${USER} /frontend/dist/favicon*.ico ${APP_DIR}/moni/assets/static/img/

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]