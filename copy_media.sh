#!/bin/bash

echo "📦 Copying media files into Railway volume..."

# Make sure directories exist
mkdir -p /app/media

# Copy local media files to the volume (overwrite enabled)
cp -r /app/app_media_source/* /app/media/ 2>/dev/null || true

echo "✅ Media files copied."

# Start Django server
echo "🚀 Starting Django..."
exec "$@"
