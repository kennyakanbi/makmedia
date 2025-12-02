# Dockerfile at repo root
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Create media directory
RUN mkdir -p /app/media

ENV PORT=8080
EXPOSE 8080

# Entrypoint: run migrations, collect static, then start server
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "project.wsgi", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "120"]
