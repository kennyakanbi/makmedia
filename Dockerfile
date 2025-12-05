# Dockerfile - Django on Railway (Python 3.12 slim)
FROM python:3.12-slim

# set workdir
WORKDIR /app

# install system deps (needed for some packages like psycopg2)
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# copy only requirements first (better layer caching)
COPY requirements.txt /app/requirements.txt

# upgrade pip and install Python deps
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy project code
COPY . /app/

# make entrypoint executable (entrypoint.sh must exist)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# expose (informational only)
EXPOSE 8000

# use entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
