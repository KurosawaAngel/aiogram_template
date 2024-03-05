FROM python:3.11-slim
WORKDIR /app

COPY . .

RUN chmod +x scripts/docker-entrypoint.sh

RUN pip install . --no-cache-dir

ENTRYPOINT ["scripts/docker-entrypoint.sh"]
