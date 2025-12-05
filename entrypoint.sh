#!/usr/bin/env bash
set -euo pipefail

# Optional: show environment for debugging (comment out in prod)
echo "=== Entrypoint start ==="
echo "PORT=${PORT:-not-set}"
echo "DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-project.settings}"

# Wait for volume to be mounted (simple check loop)
VOL=/app/media
n=0
while [ ! -d "$VOL" ] && [ "$n" -lt 6 ]; do
  echo "Waiting for volume $VOL to be present..."
  sleep 1
  n=$((n+1))
done

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Copy committed media from repo into mounted volume if volume empty
# This is safe / idempotent
if [ -d "project/media" ]; then
  echo "📦 Copying media files into Railway volume..."
  mkdir -p /app/media
  cp -r project/media/* /app/media/ 2>/dev/null || true
  echo "✅ Media files copied."
else
  echo "No project/media directory in the image — skipping copy."
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Healthcheck test (optional, comment out to reduce noise)
# python manage.py check

# Start Gunicorn on $PORT
: "${PORT:?Environment variable PORT must be set by Railway}"
echo "🚀 Starting Django..."
exec gunicorn project.wsgi --bind 0.0.0.0:"$PORT" --workers 2 --threads 2 --timeout 120
