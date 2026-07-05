from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    isCompleted: bool = False
    
class Task(TaskCreate):
    id: int

    model_config = {"from_attributes": True}
    # when i pass the object of to pydantic, that time i need this, this will know the data will come like user.id
