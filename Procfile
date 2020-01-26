release: cd src; python3 manage.py migrate
web: env > .env; env PYTHONUNBUFFERED=true honcho start -f Procfile.real 2>&1
