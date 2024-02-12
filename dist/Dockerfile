FROM python:3.11-slim
WORKDIR /app

COPY alembic.ini .

COPY migrations migrations/

COPY translations translations/

COPY bot-1.0.0.tar.gz package/bot-1.0.0.tar.gz

RUN pip install package/bot-1.0.0.tar.gz --no-cache-dir

CMD ["python", "-O", "-m", "bot"]
