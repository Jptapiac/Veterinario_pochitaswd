#!/bin/bash
# Script de inicio para Railway
set -e

echo "Creating staticfiles directory if it doesn't exist..."
mkdir -p staticfiles

echo "Waiting for database connection..."
# Esperar un poco para que la red esté lista
sleep 2

echo "Running migrations..."
python manage.py migrate --noinput || {
    echo "WARNING: Migrations failed, but continuing..."
    echo "You may need to run migrations manually later"
}

echo "Collecting static files..."
python manage.py collectstatic --noinput || {
    echo "WARNING: Collectstatic failed, but continuing..."
}

echo "Starting Gunicorn..."
PORT=${PORT:-8080}
exec gunicorn pochita_project.wsgi --log-file - --timeout 120 --workers 2 --bind 0.0.0.0:$PORT

