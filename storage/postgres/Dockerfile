FROM postgis/postgis:17-3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-17-pgvector \
    && rm -rf /var/lib/apt/lists/*

COPY init/enable-extensions.sql \
    /docker-entrypoint-initdb.d/enable-extensions.sql