# Use Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure script is executable
RUN chmod +x /app/copy_media.sh

# Start app with copy script
ENTRYPOINT ["/app/copy_media.sh"]

# CMD runs Django
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers", "2"]
