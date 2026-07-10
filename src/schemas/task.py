from pydantic import BaseModel, ConfigDict
class TaskBase(BaseModel):
    title: str
    isCompleted: bool = False


class TaskCreate(BaseModel):
    title: str
    isCompleted: bool = False
    
class TaskUpdate(BaseModel):
    title: str | None = None
    isCompleted: bool | None = None

    
class TaskResponse(TaskBase):
    id: int    
    
    
    model_config = ConfigDict(
        from_attributes=True
    )
    # when i pass the object of to pydantic, that time i need this, this will know the data will come like user.id
