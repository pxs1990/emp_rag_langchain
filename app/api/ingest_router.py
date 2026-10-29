from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.ingestion_service import IngestionService
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService
from app.config import settings
from app.models.orm_models import Base
from app.dto.query_dto import QueryResponse
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()

# Setup DB session
engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ingest", response_model=QueryResponse)
def ingest_pdf(document_id: str, version: str, db: Session = Depends(get_db)):
    """Ingests the PDF, chunks, embeds, and stores in pgvector with caching/versioning."""
    chunk_repo = ChunkRepository(db)
    embedding_service = EmbeddingService()
    ingestion_service = IngestionService(chunk_repo, embedding_service)
    result = ingestion_service.ingest(
        path="app/data/emp_handbook.pdf",
        document_id=document_id,
        version=version
    )
    return JSONResponse(content=result)
