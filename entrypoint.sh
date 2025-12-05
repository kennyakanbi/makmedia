#!/bin/sh

# Exit immediately if a command fails
set -e

# Paths
LOCAL_MEDIA_DIR="/app/project/media"
RAILWAY_MEDIA_DIR="/app/media"

echo "📦 Copying media files into Railway volume..."

# Create target directory if it doesn't exist
mkdir -p "$RAILWAY_MEDIA_DIR"

# Copy files from local media to Railway volume
cp -R "$LOCAL_MEDIA_DIR/"* "$RAILWAY_MEDIA_DIR/"

# Ensure Django can read/write files
chmod -R 755 "$RAILWAY_MEDIA_DIR"

echo "✅ Media files copied and permissions set."

# Start Django via gunicorn
echo "🚀 Starting Django..."
exec gunicorn project.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2
