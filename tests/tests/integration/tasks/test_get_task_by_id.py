import pytest


@pytest.mark.integration
def test_get_task_info_by_id(client, task):
    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200