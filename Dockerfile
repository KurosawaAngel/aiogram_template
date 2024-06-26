FROM python:3.11-slim

WORKDIR /app

RUN apt-get update &&\
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install . --no-cache-dir

CMD [ "python", "-m", "aiogram_template" ]