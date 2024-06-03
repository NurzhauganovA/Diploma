#!/bin/sh

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py runserver 0.0.0.0:8000

daphne -p 8001 diploma.asgi:application