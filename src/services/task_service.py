from src.db.models import Task

def create_task(db, task_data: Task):
    task = Task(
        title = task_data.title,
        completed = task_data.isCompleted
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

def get_task(db):
    return db.query(Task).all()

def get_task_by_id(db, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db, task_id: int, update_data):
    task = db.query(Task).filter(task_id == Task.id).first()
    if not task:
        return None
    task.title = update_data.title
    task.completed = update_data.isCompleted
    db.commit()
    db.refresh(task)
    return task