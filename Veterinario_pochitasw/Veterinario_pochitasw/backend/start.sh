#!/bin/bash
# Script de inicio para Railway
set -e

echo "=== Starting deployment script ==="
echo "Creating staticfiles directory if it doesn't exist..."
mkdir -p staticfiles

echo "Waiting for database connection..."
sleep 3

echo "Running migrations..."
python manage.py migrate --noinput || {
    echo "WARNING: Migrations failed, but continuing..."
}

echo "Collecting static files..."
python manage.py collectstatic --noinput || {
    echo "WARNING: Collectstatic failed, but continuing..."
}

echo "Starting Gunicorn..."
PORT=${PORT:-8080}
exec gunicorn pochita_project.wsgi --log-file - --timeout 120 --workers 2 --bind 0.0.0.0:$PORT

