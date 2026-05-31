from application.task.mappers import TaskServiceMapper


def get_task_service_mapper() -> TaskServiceMapper:
    return TaskServiceMapper()