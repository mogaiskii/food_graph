from re import sub
from typing import Tuple, Type

from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy.orm import RelationshipProperty, joinedload, lazyload
from strawberry.types import Info

from db.models import DBModel


def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


class NodeParser:
    def __init__(self, root_field):
        self.root_field = root_field
        self.fields = []
        self.relations = {}
        self.name = root_field.name
        for item in root_field.selections:
            if item.selections:
                self.relations[item.name] = NodeParser(item)
            else:
                self.fields.append(item.name)


class GQDBMapper:
    def __init__(self, info: Info, model: Type[DBModel]):
        self.info = info
        self.model = model
        self.parser = NodeParser(info.selected_fields[0])
        self.joins, self.lazy = self._resolve_nodes(self.parser, self.model)

    def _resolve_nodes(self, node_parser: NodeParser, model: Type[DBModel], current_chain=None):
        joins = []
        lazy = []
        relation: RelationshipProperty
        for name, relation in sa_inspect(model).relationships.items():
            if camel_case(name) in node_parser.relations:
                inner_model = relation.argument

                if current_chain is None:
                    chain = joinedload(getattr(model, name))
                else:
                    chain = current_chain.joinedload(getattr(model, name))

                joins.append(chain)

                inner_joins, inner_lazy = self._resolve_nodes(
                    node_parser.relations[camel_case(name)], inner_model, chain
                )
                joins.extend(inner_joins)
                lazy.extend(inner_lazy)

            else:
                if current_chain is None:
                    chain = lazyload(getattr(model, name))
                else:
                    chain = current_chain.lazyload(getattr(model, name))
                lazy.append(chain)

        return joins, lazy

    def patch_statement(self, stmt):
        for join_option in self.joins:
            stmt = stmt.options(join_option)

        for lazy_option in self.lazy:
            stmt = stmt.options(lazy_option)

        return stmt
