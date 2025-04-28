FROM python:3.11-alpine AS dev

ENV PYTHONUNBUFFERED=1

WORKDIR /TrelloReminder

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]

FROM python:3.11-alpine AS prod

ENV PYTHONUNBUFFERED=1

WORKDIR /TrelloReminder

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN adduser -D appuser

USER appuser

ENTRYPOINT ["python", "main.py"]