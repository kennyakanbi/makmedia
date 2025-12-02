web: python manage.py collectstatic --noinput && gunicorn project.wsgi --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120
release: python manage.py migrate

# Create Procfile with the copy+start command
$proc = 'web: bash -lc "cp -r project/media/* /app/media/ || true && gunicorn project.wsgi --bind 0.0.0.0:$PORT"'
Set-Content -Path "Procfile" -Value $proc -Encoding UTF8

# Verify file
Get-Content Procfile

