#!/bin/bash


check_env_vars() {

    if [ -z "${DATABASE_URL}" ] 
    then
        echo "DATABASE_URL not found"

        # Qovery specific
        # Create a Postgres instance on Qovery with name PGDB
        # Qovery sets custom names for database URL
        # This routine will create new database URL env variable
        if [ ${QOVERY_DATABASE_PGDB_CONNECTION_URI} ] 
        then
            echo "Found QOVERY_DATABASE_PGDB_CONNECTION_URI, setting DATABASE_URL"
            export DATABASE_URL=$QOVERY_DATABASE_PGDB_CONNECTION_URI
        fi
    fi

}

moni_api(){
    echo "Running migrations..."
    python manage.py migrate
    
    echo "Starting..."
    gunicorn moni.wsgi -b 0.0.0.0:8000
}

check_env_vars
moni_api