FROM python:3.12.2

RUN set -eux; \
    apt-get update && \
    apt-get install -y --no-install-recommends curl python3-dev && \
    curl -fsSL --proto '=https' https://install.python-poetry.org | python3 - && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root

ENV PYTHONPATH="/app/src"

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
