from re import sub
from typing import Type

from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy.orm import RelationshipProperty, joinedload, lazyload, with_polymorphic
from strawberry.types import Info

from db.models import DBModel


def camel_case(s):
  s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
  return ''.join([s[0].lower(), s[1:]])


class NodeParser:
    def __init__(self, root_field):
        self.root_field = root_field
        fields, relations = self._parse_selections(root_field.selections)
        self.fields = fields
        self.relations = relations

    def _parse_selections(self, selections):
        fields = []
        relations = {}
        for item in selections:
            if getattr(item, 'type_condition', None):
                subfields, subrelations = self._parse_selections(item.selections)
                fields.extend(subfields)
                relations.update(subrelations)
            elif getattr(item, 'selections', None):
                relations[item.name] = NodeParser(item)
            else:
                fields.append(item.name)
        return fields, relations


class GQDBMapper:
    def __init__(self, info: Info, model: Type[DBModel]):
        self.info = info
        self.model = model
        self.parser = NodeParser(info.selected_fields[0])
        self.joins, self.lazy, self.poly = self._resolve_nodes(self.parser, self.model)

    def _resolve_nodes(self, node_parser: NodeParser, model: Type[DBModel], current_chain=None):
        joins = []
        lazy = []
        poly = []
        relation: RelationshipProperty
        inspected = sa_inspect(model)
        for name, relation in inspected.relationships.items():
            if camel_case(name) in node_parser.relations:
                inner_model = relation.argument

                if current_chain is None:
                    chain = joinedload(getattr(model, name))
                else:
                    chain = current_chain.joinedload(getattr(model, name))

                joins.append(chain)

                inner_joins, inner_lazy, inner_poly = self._resolve_nodes(
                    node_parser.relations[camel_case(name)], inner_model, chain
                )
                joins.extend(inner_joins)
                lazy.extend(inner_lazy)
                poly.extend(inner_poly)

            else:
                if current_chain is None:
                    chain = lazyload(getattr(model, name))
                else:
                    chain = current_chain.lazyload(getattr(model, name))
                # lazy.append(chain)

        if inspected.polymorphic_map:
            variations = [v.class_ for v in inspected.polymorphic_map.values() if v.class_ is not model]
            poly.append((model, variations))

        return joins, lazy, poly

    def patch_statement(self, stmt):
        for join_option in self.joins:
            stmt = stmt.options(join_option)

        for lazy_option in self.lazy:
            stmt = stmt.options(lazy_option)

        # for poly_option in self.poly:
        #     stmt = stmt.options(with_polymorphic(poly_option[0], '*'))

        return stmt
