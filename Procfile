web: bash -c "cp -r project/media/* /app/media/ || true && python manage.py collectstatic --noinput && gunicorn project.wsgi --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120"
release: python manage.py migrate
