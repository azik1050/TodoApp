from starlette.testclient import TestClient


class TaskClient:
    def __init__(self, session: TestClient):
        self._session = session

    def get_tasks(self):
        return self._session.get("/tasks")

    def get_task(self, task_id: int):
        return self._session.get(f"/tasks/{task_id}")

    def create_task(self, json: dict):
        return self._session.post("/tasks", json=json)

    def delete_task(self, task_id: int):
        return self._session.delete(f"/tasks/{task_id}")

    def update_task(self, task_id: int, json: dict):
        return self._session.put(f"/tasks/{task_id}", json=json)

    def create_task_comment(self, task_id: int, json: dict):
        return self._session.post(f"/tasks/{task_id}/comments", json=json)