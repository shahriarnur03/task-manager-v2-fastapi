from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.deps import get_db
from src.schemas.task import Task, TaskCreate
from src.services import task_service

router = APIRouter()

@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session=Depends(get_db)):
    return task_service.create_task(db, task)

@router.get("/tasks")
def get_tasks(db: Session=Depends(get_db)):
    return task_service.get_task(db)

@router.get("/tasks/{task_id}")
def get_tast(task_id: int, db: Session=Depends(get_db)):
    task = task_service.get_task_by_id(task_id, db)
    if not task:
        return {"error": "Task is not found"}
    return task

@router.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskCreate, db: Session=Depends(get_db)):
    updated = task_service.update_task(task_id, task, db)
    if not updated:
        return {"error": "Task not found"}
    return updated

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session=Depends(get_db)):
    task_service.delete_task(task_id)
    return {"message": "Deleted"}