import pytest


@pytest.mark.integration
def test_create_task_comment(client, task):
    response = client.post(
        f"/tasks/{task.id}/comments/",
        json={"text": "This is a comment"},
        content_type="application/json",
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "This is a comment"
    assert "id" in data
    assert "createdAt" in data
