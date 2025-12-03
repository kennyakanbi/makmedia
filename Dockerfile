# Use Python 3.12 slim as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY project /app/project

# Copy media files
COPY project/media /app/media

# Collect static files (optional in build)
RUN python /app/project/manage.py collectstatic --noinput || true

# Expose the port (Railway uses $PORT)
EXPOSE 8000

# Start the app
CMD ["gunicorn", "project.wsgi", "--bind", "0.0.0.0:8000"]
