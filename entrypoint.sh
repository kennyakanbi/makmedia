#!/bin/sh
# entrypoint.sh - Run migrations, copy media to volume, collectstatic, then start gunicorn

set -e

# If MEDIA source exists in repo, copy files into mounted volume /app/media
# (This is safe: uses /app/media which Railway mounts from the volume)
if [ -d "/app/project/media" ]; then
  echo "📦 Copying media files into Railway volume..."
  mkdir -p /app/media
  cp -r /app/project/media/* /app/media/ 2>/dev/null || true
  chmod -R a+rX /app/media || true
  echo "✅ Media files copied and permissions set."
fi

# Run migrations (safe to run every start)
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Ensure PORT is set (Railway will set it). Default to 8000 if missing (useful for local debugging)
PORT=${PORT:-8000}

# Start gunicorn (use exec so it becomes PID 1)
echo "🚀 Starting Django..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:"${PORT}" --workers 2 --threads 2 --timeout 120
