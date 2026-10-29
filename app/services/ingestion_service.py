from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService
from app.utils.checksum import generate_checksum

class IngestionService:
    def __init__(self, chunk_repo: ChunkRepository, embedding_service: EmbeddingService, chunk_size: int = 800, chunk_overlap: int = 150):
        self.chunk_repo = chunk_repo
        self.embedding_service = embedding_service
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def ingest(self, path: str, document_id: str, version: str):
        loader = PyPDFLoader(path)
        pages = loader.load()
        chunks = self.splitter.split_documents(pages)
        ingested, skipped = 0, 0
        for chunk in chunks:
            checksum = generate_checksum(chunk.page_content)
            embedding = self.embedding_service.embed(chunk.page_content)
            result = self.chunk_repo.save(chunk, embedding, document_id, version)
            if result:
                ingested += 1
            else:
                skipped += 1
        return {"ingested": ingested, "skipped": skipped, "total": len(chunks)}