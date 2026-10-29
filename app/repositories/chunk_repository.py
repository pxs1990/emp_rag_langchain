import re

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.orm_models import DocumentChunk
from app.utils.checksum import generate_checksum
from uuid import uuid4

class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def exists(self, checksum: str, version: str) -> bool:
        return self.db.query(DocumentChunk).filter_by(checksum=checksum, version=version).first() is not None

    def save(self, chunk, embedding, document_id: str, version: str):
        checksum = generate_checksum(chunk.page_content)
        if self.exists(checksum, version):
            return None  # Already ingested
        db_chunk = DocumentChunk(
            chunk_id=uuid4(),
            document_id=document_id,
            version=version,
            page_number=chunk.metadata["page"],
            chunk_text=chunk.page_content,
            checksum=checksum,
            embedding=embedding,
            chunk_metadata=chunk.metadata
        )
        self.db.add(db_chunk)
        self.db.commit()
        return db_chunk

    def search(self, question: str, version: str = "latest", limit: int = 5):
        keywords = [token for token in re.findall(r"[a-zA-Z0-9]+", question.lower()) if len(token) > 2]
        if not keywords:
            return []

        filters = []
        for keyword in keywords:
            filters.append(DocumentChunk.chunk_text.ilike(f"%{keyword}%"))

        query = self.db.query(DocumentChunk).filter(or_(*filters))
        if version != "latest":
            query = query.filter(DocumentChunk.version == version)

        return query.order_by(DocumentChunk.page_number).limit(limit).all()