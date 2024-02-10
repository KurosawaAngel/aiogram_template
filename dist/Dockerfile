FROM python:3.11-slim
WORKDIR /app

COPY translations translations/

COPY migrations migrations/

COPY alembic.ini .

COPY bot-1.0.0.tar.gz /package/bot-1.0.0.tar.gz

RUN pip install /package/bot-1.0.0.tar.gz

CMD ["python", "-m", "bot"]
