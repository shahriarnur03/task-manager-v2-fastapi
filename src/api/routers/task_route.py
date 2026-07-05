from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.core.response import paginated_response, success_response
from src.database.deps import get_db
from src.schemas.task import Task, TaskCreate
from src.schemas.response import ApiResponse, PaginatedResponse
from src.services import task_service

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post(
    "/",
    response_model=ApiResponse[Task],
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, db: Session=Depends(get_db)):
    created_task = task_service.create_task(db, task)
    return success_response(
        message="Task created successfully.",
        data=created_task,
        status_code=status.HTTP_201_CREATED,
    )

@router.get(
    "/",
    response_model=PaginatedResponse[Task],
)
def get_tasks(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session=Depends(get_db),
):
    result = task_service.get_tasks(db, page=page, limit=limit)
    return paginated_response(
        message="Tasks retrieved successfully.",
        data=result["items"],
        page=page,
        limit=limit,
        total=result["total"],
    )

@router.get(
    "/{task_id}",
    response_model=ApiResponse[Task],
    response_model_exclude_none=True,
)
def get_task(task_id: int, db: Session=Depends(get_db)):
    task = task_service.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return success_response(
        message="Task retrieved successfully.",
        data=task,
    )

@router.put(
    "/{task_id}",
    response_model=ApiResponse[Task],
    response_model_exclude_none=True,
)
def update_task(task_id: int, task: TaskCreate, db: Session=Depends(get_db)):
    updated = task_service.update_task(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return success_response(
        message="Task updated successfully.",
        data=updated,
    )

@router.delete(
    "/{task_id}",
    response_model=ApiResponse[None],
    response_model_exclude_none=True,
)
def delete_task(task_id: int, db: Session=Depends(get_db)):
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return success_response(message="Task deleted successfully.")
