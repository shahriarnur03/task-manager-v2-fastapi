from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from src.api.routers.task_route import router as task_router
from src.core.exceptions import http_exception_handler, validation_exception_handler
from src.db.connection import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(task_router)
