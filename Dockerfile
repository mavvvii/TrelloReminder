FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
ENV POETRY_VERSION=1.4.2

RUN pip install poetry==${POETRY_VERSION}

WORKDIR /TrelloReminder

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

ENTRYPOINT ["poetry", "run", "python", "src/main.py"]