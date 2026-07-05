from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from src.api.routers import api_router
from src.core.config import settings
from src.core.exceptions import http_exception_handler, validation_exception_handler
from src.database.connection import Base, engine

def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)
    app = FastAPI(
        title=settings.PROJECT_NAME
    )

    app.add_exception_handler(HTTPException, http_exception_handler)

    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    app.include_router(api_router)
    return app

app = create_app()
