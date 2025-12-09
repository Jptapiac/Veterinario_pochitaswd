#!/bin/bash
# Script de inicio para Railway
set -e

echo "Creating staticfiles directory if it doesn't exist..."
mkdir -p staticfiles

echo "Running migrations..."
python manage.py migrate --noinput || echo "Migrations failed, continuing..."

echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Collectstatic failed, continuing..."

echo "Starting Gunicorn..."
exec gunicorn pochita_project.wsgi --log-file - --timeout 120 --workers 2

