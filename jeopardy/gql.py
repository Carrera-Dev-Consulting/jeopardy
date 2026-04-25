from datetime import timedelta
from logging import getLogger
import os

from ariadne import (
    MutationType,
    make_executable_schema,
    load_schema_from_path,
    QueryType,
)
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLTransportWSHandler
from fastapi import Request
from graphql import GraphQLResolveInfo
from pydantic_settings import BaseSettings, SettingsConfigDict
from .auth import parse_token, BEARER_SCHEMA

logger = getLogger(__name__)


class GQLAPISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GQL_",
    )

    CONNECTION_TIMEOUT_SECONDS: int = 60


gql_settings = GQLAPISettings()


# Creating the initial type definitions
QUERY_TYPE = QueryType()
MUTATION_TYPE = MutationType()

types = [
    QUERY_TYPE,
    MUTATION_TYPE,
]

# Create and Register the resolvers


def drop_nones(d):
    return {k: v for k, v in d.items() if v is not None}


@QUERY_TYPE.field("boards")
async def filter_boards(
    parent,
    info: GraphQLResolveInfo,
    filter,
    page,
    total,
):
    filter = filter = {}
    filter = drop_nones(filter)

    return {
        "items": [],
        "meta": {
            "totalItems": 0,
            "totalPages": 1,
            "currentPage": page,
            "size": total,
        },
    }


@MUTATION_TYPE.field("createBoard")
async def create_board(_, __):
    return {"errors": ["Not implemented"]}


# Creating the GQL All Together
raw_schema_str = load_schema_from_path(
    os.path.join(os.path.dirname(__file__), "schema.gql"),
)

gql_schema = make_executable_schema(raw_schema_str, *types)


async def handle_request_context(request: Request, _):
    try:
        result = await BEARER_SCHEMA(request)
    except Exception:
        logger.info("Anonymous User...", extra={"user": None})
        return {"request": request, "auth": None}

    user = parse_token(result.credentials)
    logger.info("Welcome %s", user.name, extra={"user": user.email})
    return {"request": request, "auth": user}


gql = GraphQL(
    gql_schema,
    context_value=handle_request_context,
    websocket_handler=GraphQLTransportWSHandler(
        connection_init_wait_timeout=timedelta(
            seconds=gql_settings.CONNECTION_TIMEOUT_SECONDS
        ),
    ),
)
