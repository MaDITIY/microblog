#!/bin/sh
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :8080 --access-logfile - --error-logfile - microblog:app
