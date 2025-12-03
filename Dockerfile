# Dockerfile (repo root) — installs libpq-dev so psycopg2 can build
FROM python:3.12-slim

# system deps required to build psycopg2, Pillow, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy only requirements first for caching
COPY requirements.txt /app/

# upgrade pip and install Python deps
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# copy project files
COPY . /app

# create media dir and copy entrypoint
RUN mkdir -p /app/media
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PORT=8080
EXPOSE 8080

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "project.wsgi", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "120"]
