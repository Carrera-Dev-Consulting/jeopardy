"""
Module that contains the click entrypoint for our cli interface.

We only handle a handful of configurations for out webserver.
"""

from typing import Any
import re
import click
import uvicorn

from .server import fastapi_app


class HostnameParameter(click.ParamType):
    def __init__(self) -> None:
        super().__init__()
        self.name = "hostname"

    hostname_format = re.compile(
        r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    )

    def convert(
        self,
        value: Any,
        param: click.Parameter | None,
        ctx: click.Context | None,
    ) -> Any:
        if not isinstance(value, str):
            value = str(value)
        if not self.hostname_format.match(value):
            self.fail("String value is not a valid hostname.")
        return value


@click.command()
@click.option("--port", "-p", type=int, default=5000)
@click.option("--host", "-h", type=HostnameParameter(), default="localhost")
@click.option("--worker-count", "-w", type=int, default=1)
def main(port: int, host: str, worker_count: int):  # pragma: no cover
    uvicorn.run(fastapi_app, port=port, host=host, workers=worker_count)


if __name__ == "__main__":  # pragma: no cover
    main()
