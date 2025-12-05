release: bash -lc 'python3 -m pip install -r requirements.txt && python3 manage.py migrate'
web: bash -lc 'mkdir -p /app/media && cp -r project/media/* /app/media/ 2>/dev/null || true && python3 manage.py collectstatic --noinput && exec gunicorn project.wsgi --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120'
web: bash ./entrypoint.sh
