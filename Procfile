# Procfile

# Run migrations on deploy
release: python manage.py migrate

# Copy media (from project/media in repo) to /app/media, collect static, and start Gunicorn
web: bash -c "cp -r project/media/* /app/media/ 2>/dev/null || true && python manage.py collectstatic --noinput && gunicorn project.wsgi --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120"
