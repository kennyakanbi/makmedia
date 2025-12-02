#!/usr/bin/env bash
set -e

# Install any new pip requirements if they exist (optional)
# python -m pip install -r requirements.txt

# Run migrations (safe to run - idempotent)
echo "Running migrations..."
python3 manage.py migrate --noinput

# Collect static files
echo "Collecting static..."
python3 manage.py collectstatic --noinput

# Ensure media directory exists
mkdir -p /app/media

# Exec the CMD (gunicorn)
echo "Starting server..."
exec "$@"
