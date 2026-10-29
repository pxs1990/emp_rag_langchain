from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, JSON, Text, DateTime, UUID
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass



class DocumentChunk(Base):

    __tablename__ = "doc_chunks"
    __table_args__ = {"schema": "emp_ai"}

    chunk_id = Column(
        UUID,
        primary_key=True
    )

    document_id = Column(
        String,
        nullable=False
    )

    version = Column(
        String,
        nullable=False
    )

    page_number = Column(
        Integer,
        nullable=False
    )

    chunk_text = Column(
        Text,
        nullable=False
    )

    checksum = Column(
        String,
        nullable=False
    )

    embedding = Column(
        Vector(3072)
    )

    chunk_metadata = Column(
        JSONB
    )

    created_at = Column(
        DateTime
    )
