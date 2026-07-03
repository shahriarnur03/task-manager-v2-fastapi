from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://:shahriar@localhost/task-manager-v2"

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    authcommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()