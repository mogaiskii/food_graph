# Food planning graphql web server

## Env variables

- `DB_URL` - url string for pg database
- `DEBUG` [Optional] - debug mode. `False` by default

## Running

### Option (a) - easy one

`docker-compose up -d`

### Option (b) - not so easy one

From root (here):
- `DB_URL=<your db url> uvicorn main:app --reload --app-dir src`

### Prerequisites & development

- Install poetry
  - https://python-poetry.org/docs/#installation
- Install dependencies
  - `poetry install`
- Update databse
  - `DB_URL=<your db url> alembic upgrade head`
