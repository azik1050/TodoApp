import pytest

from application.task.schemas import TaskCommentWrite


@pytest.mark.integration
def test_create_task_comment(task_client, task):
    response = task_client.create_task_comment(
        task_id=task.id,
        json=TaskCommentWrite(
            text="This is a comment",
        ).model_dump(by_alias=True),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "This is a comment"
    assert "id" in data
    assert "createdAt" in data
