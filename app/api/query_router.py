from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dto.query_dto import Citation, QueryRequest, QueryResponse
from app.repositories.chunk_repository import ChunkRepository
from app.models.orm_models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

router = APIRouter()

engine = create_engine(settings.postgres_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/query", response_model=QueryResponse)
def query_document(request: QueryRequest, db: Session = Depends(get_db)):
    chunk_repo = ChunkRepository(db)
    chunks = chunk_repo.search(request.question, version=request.version, limit=5)

    if not chunks:
        return QueryResponse(
            answer="No relevant content found in the ingested PDF.",
            confidence=0.0,
            citations=[],
        )

    answer_text = " ".join(chunk.chunk_text for chunk in chunks[:2])
    citations = [
        Citation(page=chunk.page_number, section=chunk.document_id, score=0.9)
        for chunk in chunks[:3]
    ]

    return QueryResponse(
        answer=answer_text,
        confidence=0.85,
        citations=citations,
    )