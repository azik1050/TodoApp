import pytest


@pytest.mark.integration
def test_update_task_status(client, task):
    # Change status from default TO_DO to IN_PROGRESS
    response = client.patch(f"/tasks/{task.id}/", json={"status": "IN_PROGRESS"})
    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"

