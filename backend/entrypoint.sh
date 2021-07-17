#!/bin/bash

moni_api(){
    echo "Running migrations..."
    python manage.py migrate
    
    echo "Starting..."
    gunicorn moni.wsgi -b 0.0.0.0:${PORT:-8000}
}

moni_api