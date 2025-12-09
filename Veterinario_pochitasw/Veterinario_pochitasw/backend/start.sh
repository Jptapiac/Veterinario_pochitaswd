#!/bin/bash
# Script de inicio para Railway
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn pochita_project.wsgi --log-file -

