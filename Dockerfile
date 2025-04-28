FROM python:3.12-slim

RUN apt-get update && apt-get install -y curl build-essential python3-dev

# Install Poetry, and set up PATH so we can use it !
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

COPY . .

RUN poetry install --no-interaction --no-root

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]