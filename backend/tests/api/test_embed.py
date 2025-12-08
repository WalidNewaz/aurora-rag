import pytest

from ..conftest import client

@pytest.mark.asyncio
def test_search_endpoint(client):
    response = client.get("/v1/embed?q=test")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test"
    assert len(data["results"]) == 3