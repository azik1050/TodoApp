import pytest


@pytest.mark.integration
def test_get_tasks(client, task):
    response = client.get("/tasks")
    assert response.status_code == 200
