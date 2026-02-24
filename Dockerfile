FROM python:3.14-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml uv.lock README.md /app/
COPY . /app/

RUN uv sync


CMD ["uv", "run", "src/baseline/main.py"]
