#!/bin/sh

# Migrate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsu

# Start gunicorn server at port 8000
# To watch for code changes, pass the --reload flag to the command
# workers determined by (2 x $num_cores) + 1 -- docker tasks currently has 1024 cpu (1 core) -- (2 x 1) + 1 = 3
gunicorn timecard.wsgi:application -w 3 -b 0.0.0.0:8000
