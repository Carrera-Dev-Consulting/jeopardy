from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from .gql import gql


class APISettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 5000


api_settings = APISettings()

app = FastAPI()

app.mount("/graphql", gql, name="graphql")


class HealthCheckValue(str, Enum):
    ok = "ok"
    error = "error"


class HealthcheckResponse(BaseModel):
    status: HealthCheckValue


@app.get(
    "/healthz",
    response_model=HealthcheckResponse,
)
def healthz():
    # TODO: Add actual health check i.e. for services and make sure they are good.
    return {"status": "ok"}


@app.get("/version")
def version():
    from importlib.metadata import version

    runtime_version = version("jeopardy-cdc")
    return runtime_version
