FROM python:3.11-slim

COPY bot-1.0.0.tar.gz /package/bot-1.0.0.tar.gz
RUN pip install /package/bot-1.0.0.tar.gz
WORKDIR /app
CMD ["python", "-m", "bot"]
