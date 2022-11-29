from typing import TypeVar, Type, Union

from sqlalchemy import inspect
from sqlalchemy.orm import Mapper

from api.graphql.exceptions import UnresolvedSchemaException
from api.graphql.schemas import GQBase
from db.models import DBModel


T = TypeVar("T")


def check_is_list(annotation) -> bool:
    if getattr(annotation, '__origin__', None) is None:
        return False

    if getattr(annotation, '__origin__', None) is list:
        return True

    if getattr(annotation.__args__[0], '__origin__', None) is list:
        return True

    return False


def find_schema(annotation) -> Type[GQBase]:
    search_stack = [annotation]
    while search_stack:
        annotation = search_stack.pop(0)
        if type(annotation) is type and issubclass(annotation, GQBase):
            return annotation

        pretendents = [item for item in annotation.__args__ if issubclass(item, GQBase)]
        if pretendents:
            return pretendents[0]

        nested = [item for item in annotation.__args__ if check_is_list(item) or item.__origin__ is Union]
        search_stack.extend(nested)

    raise UnresolvedSchemaException


def map_db_to_gq(db_model: DBModel, gq_model: Type[T]) -> T:
    mapper: Mapper = inspect(db_model).mapper
    db_fields = mapper.columns.keys()
    db_relations = mapper.relationships.keys()

    gq_fields = gq_model.__annotations__

    build_params = {}
    for name, annotation in gq_fields.items():
        value = getattr(db_model, name)
        if name in db_fields:
            build_params[name] = value

        if name in db_relations:
            field = value
            schema = find_schema(annotation)
            if check_is_list(annotation):
                item = [map_db_to_gq(field_item, schema) for field_item in field]
            else:
                if field is None:
                    item = None
                else:
                    item = map_db_to_gq(field, schema)
            build_params[name] = item

    return gq_model(**build_params)
