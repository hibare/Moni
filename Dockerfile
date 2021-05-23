FROM python:slim as base

LABEL Github="hibare"

FROM base as base-builder

RUN apt-get update && apt-get install -y build-essential python3-dev

RUN pip install -U pip setuptools

FROM base-builder as builder

COPY backend/requirements.txt .

RUN mkdir -p /install

RUN pip install -r requirements.txt --prefix=/install --no-warn-script-location

FROM base

ENV USER=ghost

ENV APP_DIR=/home/${USER}/app

COPY --from=builder /install /usr/local

RUN useradd -ms /bin/bash ${USER}

USER ${USER}

RUN mkdir -p ${APP_DIR}

WORKDIR ${APP_DIR}

COPY --chown=ghost:ghost backend .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["sh", "entrypoint.sh"]