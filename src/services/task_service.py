from database.models.task import Task
from src.schemas.task import TaskCreate

def create_task(db, task_data: TaskCreate):
    task = Task(
        title=task_data.title,
        isCompleted=task_data.isCompleted
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_tasks(db, page: int = 1, limit: int = 10):
    offset = (page - 1) * limit
    query = db.query(Task)

    return {
        "items": query.offset(offset).limit(limit).all(),
        "total": query.count(),
    }

def get_task_by_id(db, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db, task_id: int, update_data):
    task = db.query(Task).filter(task_id == Task.id).first()
    if not task:
        return None
    task.title = update_data.title
    task.isCompleted = update_data.isCompleted
    db.commit()
    db.refresh(task)
    return task

def delete_task(db, task_id: int):
    task = db.query(Task).filter(task_id == Task.id).first()
    
    if not task:
        return None
    db.delete(task)
    db.commit()
    return True
