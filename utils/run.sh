#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate
gunicorn papkort.wsgi --bind=0.0.0.0:80