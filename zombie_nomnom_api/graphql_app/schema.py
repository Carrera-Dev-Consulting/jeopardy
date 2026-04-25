from enum import Enum
from logging import getLogger
import os

from ariadne import (
    EnumType,
    ObjectType,
    SchemaBindable,
    make_executable_schema,
    load_schema_from_path,
)
from typing import TypeVar
from zombie_nomnom import DieColor, Face


_logger = getLogger(__name__)
_registry: dict[str, SchemaBindable] = {}

TRegistry = TypeVar("TRegistry", bound=SchemaBindable)


def register(graphql_type: TRegistry) -> TRegistry:
    """Adds bindable type to schema registry for the instantiation of the graphql executable schema.

    **Parameters**
    - graphql_type (SchemaBindable): The type we are registering.

    **Returns**
    - SchemaBindable: The type that was registered
    """
    if not isinstance(graphql_type, SchemaBindable):
        _logger.warning(
            f"Failed to register a non bindable type, Type must implement SchemaBindable from ariadne."
        )
        return

    try:
        key = (
            graphql_type.name
        )  # not defined in base type but all used types will have it.
    except AttributeError:
        _logger.warning(f"Unable to resolve name for schema {graphql_type}")
        return
    if key in _registry:
        _logger.warning(
            f"{key} is already defined as a type skipping duplicate registration."
        )
        return
    _logger.debug(f"Registered type: {key}")
    _registry[key] = graphql_type
    return graphql_type


def register_enum(enum_type: type[Enum], *, name: str = None):
    """Shortcut function to register the enum type to the graphql type registry.

    **Parameters**
    - enum_type (EnumType): The enum type we want to add to graphql schema.
    - name (str, optional): An alias name used by grapqhl to refer to the enum if the enum name is different then what is in the schema.
    """
    return register(EnumType(name or enum_type.__name__, enum_type))


def build_schema():
    path_to_schema = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "schema.gql",
        ),
    )
    _logger.debug(f"Loading schema from path: {path_to_schema}")
    _logger.debug(f"Registered schemas: {list(_registry.keys())}")
    raw_schema = load_schema_from_path(path_to_schema)
    return make_executable_schema(raw_schema, *_registry.values())


Query = register(ObjectType("Query"))
"""
Query type that is used as the entrypoint for reads in grapqhl
"""
Mutation = register(ObjectType("Mutation"))
"""
Mutation type that is used as the entrypoint for writes in grapqhl
"""
GameResource = register(ObjectType("Game"))
"""
Game type that we expose in graphql
"""
Round = register(ObjectType("Round"))
"""
Round type that we expose in graphql
"""
PlayerResource = register(ObjectType("Player"))
"""
Player type that we expose in graphql
"""
DieBagResource = register(ObjectType("DieBag"))
"""
DieBag type that we expose in graphql
"""
DieResource = register(ObjectType("Die"))
"""
Die type that we expose in graphql
"""
Move = register(ObjectType("Move"))
"""
Move type that we expose in graphql
"""

# Register enums for GQL
register_enum(DieColor)
register_enum(Face, name="DieFace")
