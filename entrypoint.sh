#!/bin/sh
set -e

# ensure media dir exists and copy bundled media if any
mkdir -p /app/media
echo "📦 Copying media files into Railway volume..."
# Copy only if there are files in project/media
if [ -d "/app/project/media" ] && [ "$(ls -A /app/project/media)" ]; then
  cp -R /app/project/media/* /app/media/ || true
fi
echo "✅ Media files copied."

# run migrations (optional)
python manage.py migrate --noinput

# collectstatic (if using)
python manage.py collectstatic --noinput

exec "$@"
