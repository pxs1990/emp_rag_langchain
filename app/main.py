import sys
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy import text

# ROOT_DIR = Path(__file__).resolve().parent.parent
# if str(ROOT_DIR) not in sys.path:
#     sys.path.insert(0, str(ROOT_DIR))

from app.api import ingest, query
from app.config import settings
from app.models.orm_models import Base

engine = create_engine(settings.postgres_url)

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS emp_ai"))

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee RAG API"
)

app.include_router(
    query.router,
    prefix="/api/v1"
)

app.include_router(
    ingest.router,
    prefix="/api/v1"
)
