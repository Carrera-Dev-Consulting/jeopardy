FROM python:3.10-slim AS deploy

ARG PDM_BUILD_SCM_VERSION="0.0.0"

WORKDIR /app

COPY zombie_nomnom_api zombie_nomnom_api
COPY README.md README.md
COPY pyproject.toml pyproject.toml

RUN pip install .
EXPOSE 5000
ENTRYPOINT ["zombie-nomnom-api", "--port", "5000", "--host", "0.0.0.0"]

FROM deploy AS test

COPY tests tests
COPY requirements-dev.txt requirements-dev.txt
COPY makefile makefile
RUN apt update && apt install -y make && apt clean && pip install -r requirements-dev.txt

ENTRYPOINT [ "make", "all-test" ]