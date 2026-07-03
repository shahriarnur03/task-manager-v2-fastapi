from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    isCompleted: bool = False
    
class Task(TaskCreate):
    id: int