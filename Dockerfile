FROM python:3.7-alpine as base

FROM base as build_base

RUN apk --update add --no-cache gcc python3-dev musl-dev hiredis

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config settings.virtualenvs.create false && poetry install --no-dev

COPY . .
COPY env/docker.env .env

EXPOSE 8080

CMD python md5service/app.py