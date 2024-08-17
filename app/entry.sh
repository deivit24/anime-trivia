#!/bin/sh

if ["$POSTGRES_DRIVER" = "postgresql"]
then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_DRIVER $POSTGRES_PORT; do
        sleep 0.1
    done

    echo "Postgres Started"
fi

cd trivia
uvicorn app:app --reload --host 0.0.0.0 --port 8000

