from fastapi import FastAPI, HTTPException, Request
from importlib.metadata import version

from fastapi.responses import JSONResponse

from .graphql_app import graphql_app
from fastapi.middleware.cors import CORSMiddleware
from zombie_nomnom_api import configs
from zombie_nomnom_api.rest_app.authentication import (
    get_verifier,
    token_auth_scheme,
)


try:
    _version = version("zombie-nomnom-api")
except:  # pragma: no cover
    _version = "dev"

fastapi_app = FastAPI(
    title="Zombie Nom Nom API",
    version=_version,
)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=configs.cors_origins,
    allow_credentials=configs.cors_allow_credentials,
    allow_methods=configs.cors_methods,
    allow_headers=configs.cors_headers,
)


@fastapi_app.middleware("http")
async def hydrate_user(
    request: Request,
    call_next,
):
    try:
        token = await token_auth_scheme(request)
    except HTTPException as e:
        if e.detail == "Not authenticated":
            return await call_next(request)
        return JSONResponse(
            {"status": "error", "message": "Not Authenticated"}, status_code=401
        )

    result = get_verifier().verify(token.credentials)

    if result.get("status"):
        return JSONResponse(result, status_code=403)
    request.state.user = result
    return await call_next(request)


@fastapi_app.get("/healthz")
def healthz():
    return {"o": "k"}


@fastapi_app.get("/version")
def version():
    return {"version": _version}


@fastapi_app.get("/me")
def get_me(request: Request):
    return getattr(request.state, "user", None)


fastapi_app.mount("/", graphql_app)
