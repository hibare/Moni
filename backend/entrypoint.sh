#!/bin/bash


check_env_vars() {
    # Check DATABASE environment variable
    if [ -z "${DATABASE_URL}" ] 
    then
        echo "DATABASE_URL not found"

        if [ ${QOVERY_DATABASE_PGDB_CONNECTION_URI} ] 
        then
            echo "Found QOVERY_DATABASE_PGDB_CONNECTION_URI, setting DATABASE_URL"
            export DATABASE_URL=$QOVERY_DATABASE_PGDB_CONNECTION_URI
        fi
    fi

}

moni_api(){
    gunicorn moni.wsgi -b 0.0.0.0:8000
}

check_env_vars
moni_api