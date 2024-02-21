FROM python:3.11-slim
WORKDIR /app

COPY . .

RUN chmod +x scripts/docker-entrypoint.sh

RUN pip install dist/bot-1.0.0.tar.gz --no-cache-dir

ENTRYPOINT ["scripts/docker-entrypoint.sh"]
