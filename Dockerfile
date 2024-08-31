FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV READ_ENV 1

RUN apt-get update
RUN pip install -U pip
RUN pip install "poetry==1.6.1"

WORKDIR /app

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
