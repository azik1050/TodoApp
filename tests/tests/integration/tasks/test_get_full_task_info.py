import pytest


@pytest.mark.integration
def test_get_full_task_info(client, task):
    response = client.get(f"/tasks/{task.id}/")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data and isinstance(data["history"], list)
    assert "comments" in data and isinstance(data["comments"], list)
    # freshly created task should have empty history and comments
    assert data["history"] == []
    assert data["comments"] == []

