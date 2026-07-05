from sqlalchemy.orm import Session
from src.database.models import Task

class TaskRepository:

    def create(
            self,
            db: Session,
            title: str,
            is_completed: bool = False
    ) -> Task:
        task = Task(
            title=title,
            isCompleted=is_completed
        )

        db.add(task)
        db.commit()
        db.refresh(task)

        return task
    
    def get_all(
            self,
            db: Session,
            page: int,
            limit: int
    ):
        offset = (page - 1) * limit

        query = db.query(Task)

        return {
            "items": query.offset(offset).limit(limit).all(),
            "total": query.count()
        }

    def get_by_id(
            self,
            db: Session,
            task_id: int,
    ) -> Task :
        return (
            db.query(Task).filter(Task.id == task_id).first()
        )
    
    def update(
            self,
            db: Session,
            task: Task,
    ) -> Task:
        db.commit()
        db.refresh(task)
        return task
    
    def delete(
            self,
            db: Session,
            task: int
    ) -> None:
        db.delete(task)
        db.commit()
