from sqlalchemy.orm import Session
from src.repositories.task_repository import TaskRepository
from src.schemas.task import TaskCreate


repository = TaskRepository()

def create_task(db: Session, task_data: TaskCreate):
    return repository.create(
        db=db,
        title=task_data.title,
        is_completed=task_data.isCompleted
    )

def get_tasks(db: Session, page: int, limit: int):
    return repository.get_all(
        db=db,
        page=page,
        limit=limit
    )

def get_task_by_id(db: Session, task_id: int):
    return repository.get_by_id(
        db=db,
        task_id=task_id
    )

def update_task(db: Session, task_id: int, update_data: TaskCreate):
    task = repository.get_by_id(db=db, task_id=task_id)
    if not task:
        return None
    task.title = update_data.title
    task.isCompleted = update_data.isCompleted
    return repository.update(
        db=db,
        task=task
    )

def delete_task(db: Session, task_id: int):
    task = repository.get_by_id(db=db, task_id=task_id)
    
    if not task:
        return None
    repository.delete(
        db=db,
        task=task
    )
    
    return True
