FROM python:3.7-alpine

RUN apk --update add --no-cache gcc python3-dev musl-dev hiredis

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config settings.virtualenvs.create false && poetry install --no-dev

COPY md5service md5service

EXPOSE 8080

ENV PYTHONPATH "${PYTHONPATH}:${PWD}"

CMD python md5service/app.py