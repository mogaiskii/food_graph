import inspect
from typing import TypeVar, Type, Union, get_type_hints

from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import Mapper

from api.graphql.exceptions import UnresolvedSchemaException
from api.graphql.schemas import GQBase
from core.interactors.users.interactor import trial_user_token
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
    mapper: Mapper = sa_inspect(db_model).mapper
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


async def get_user(session, request):
    token = request.headers.get("authorization", None)
    return await trial_user_token(session, token)


# came to nowhere. ```strawberry.exceptions.MissingArgumentsAnnotationsError:
# Missing annotation for arguments "args" and "kwargs" in field "async_map_response_wrapper", did you forget to add it?
# ```
# And it seems to be meaningless to create function args programmatically
# caution: black magic
def map_response(arg):
    """
    wraps return into expected GQ model mapping
    :param arg:
        if callable is the only arg - tries to wrap callable using typehints
        if GQBase class is the only arg - uses it as a return type
    """
    if callable(arg) and not inspect.isclass(arg):
        _func = arg
    elif inspect.isclass(arg) and issubclass(arg, GQBase):
        _func = None
    else:
        raise RuntimeError("only GQBase classes could be mapped")

    def determine_response_type(func, outer_arg):
        if inspect.isclass(outer_arg) and issubclass(outer_arg, GQBase):
            return outer_arg
        hint = get_type_hints(func).get('return', None)
        if hint is None:
            return None
        if hasattr(hint, '__origin__') and issubclass(hint.__origin__, list):
            return hint.__args__[0]
        if inspect.isclass(hint) and issubclass(hint, GQBase):
            return hint
        return None

    async def async_map_response_wrapper(*args, **kwargs):
        if _func is None:
            raise RuntimeError

        response_type = determine_response_type(_func, arg)
        result = await _func(*args, **kwargs)
        if isinstance(result, list):
            return [map_db_to_gq(item, response_type) for item in result]
        return map_db_to_gq(result, response_type)

    def map_response_wrapper(*args, **kwargs):
        if _func is None:
            raise RuntimeError("Unable to determine function to wrap")

        response_type = determine_response_type(_func, arg)
        if response_type is None:
            raise RuntimeError("Unable to determine return type")
        result = _func(*args, **kwargs)
        if isinstance(result, list):
            return [map_db_to_gq(item, response_type) for item in result]
        return map_db_to_gq(result, response_type)

    if _func is None and issubclass(arg, GQBase):
        def map_response_decorator(func):
            nonlocal _func
            _func = func

            if inspect.iscoroutinefunction(_func):
                async_map_response_wrapper.__annotations__ = getattr(_func, '__annotations__')
                return async_map_response_wrapper

            map_response_wrapper.__annotations__ = getattr(_func, '__annotations__')
            return map_response_wrapper

        return map_response_decorator

    else:
        if inspect.iscoroutinefunction(_func):
            async_map_response_wrapper.__annotations__ = getattr(_func, '__annotations__')
            return async_map_response_wrapper
        map_response_wrapper.__annotations__ = getattr(_func, '__annotations__')
        return map_response_wrapper
