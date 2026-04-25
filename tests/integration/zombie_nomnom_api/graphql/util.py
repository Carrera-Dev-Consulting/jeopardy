from fastapi.testclient import TestClient


def query_api(client: TestClient, query: str, variables: dict = {}):
    return client.post("/graphql", json={"query": query, "variables": variables})
