web: cd src; gunicorn monitor.wsgi -b 0.0.0.0:$PORT
celery: cd src; celery worker --app=monitor -l info