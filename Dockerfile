FROM python:3.12-slim

RUN apt-get update &&\
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.4.18 /uv /bin/uv

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

# Run the application.
CMD ["uv", "run", "-m", "aiogram_template"]