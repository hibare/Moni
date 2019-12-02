# Crazy Wizard

Django + Celery + Beat app to monitor websites health.
Sends notifications via e-mail or slack on receiving status 5XX.

Easily add URLs to monitor using Django's built in admin panel.

Celery beat will schedule a task to run checks on all URLs in paraller in separate celery tasks.

## Requirements

1. Python3 (recommended version 3.8.0 but optional)
2. Docker

Install requirements by running following command from project root directory.

```shell
pip install -r src/requirements.txt
```

## Running

### Local (Dev)

Rename file `.env.example` to `.env` and populate all values. You can leave values for `DATABASE_URL` and `REDIS_URL` as it is.

Navigate to `docker` directory under project root.

Spin-up docker containers, postgres and redis, using following command.

```shell
docker-compose up -d
```

If you have installed project requirements in a virtual environment, activate the virtual environment.

Navigate to `src` directory and apply all database migrations using following command.

```shell
python3 manage.py migrate
```

Start the app using following command.

```shell
honcho start -f Procfile.real
```

URL and port number for the app will be printed on the console.

### Heroku

Create an app on heroku and provision `heroku-postgres` add-on.
For redis either use heroku redis add on or free redis instance provided by [Redis labs](https://redislabs.com/).

Link heroku app to your project on the dev system and push the code to heroku.

Heroku will use `Procfile` which will internally executes `Procfile.real`. This is a workaround to run all processes in a single dyno.
