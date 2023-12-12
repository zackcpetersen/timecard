#!/bin/sh

# run migrations and start local server
python manage.py migrate
python manage.py createsu
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000

exec "$@"
