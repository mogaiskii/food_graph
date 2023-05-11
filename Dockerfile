FROM python:3.10

WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY poetry.lock .
COPY pyproject.toml .

COPY ./alembic ./alembic
COPY alembic.ini .
COPY ./tasks ./tasks
COPY ./src .

RUN poetry install --no-root

COPY start.sh .

EXPOSE 8000

ENTRYPOINT ["bash", "start.sh"]
