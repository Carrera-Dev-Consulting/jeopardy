from ariadne.asgi import GraphQL
from .schema import build_schema
import zombie_nomnom_api.graphql_app.resolvers

# TODO(Milo): Make this configurable somehow.
graphql_app = GraphQL(build_schema(), debug=True)
