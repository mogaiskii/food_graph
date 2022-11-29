__all__ = ['settings', 'app']

from api.graphql.base import graphql_app
from app import app
from settings import settings

app.include_router(graphql_app, prefix="/graphql")
