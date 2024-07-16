#!/bin/bash

python3 manage.py collectstatic --noinput
# i commit my migration files to git so i dont need to run it on server
# ./manage.py makemigrations app_name
python3 manage.py migrate auth --noinput
python3 manage.py migrate timetable 0001_initial
python3 manage.py migrate --noinput

# here it start nginx and the uwsgi
daphne SubtitutesProject.asgi:application -p 5858 -b 0.0.0.0