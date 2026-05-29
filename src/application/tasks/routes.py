from src.application.app import application

router = application.create_router(prefix="/tasks")


@router.get("/")
def get_tasks():
    pass