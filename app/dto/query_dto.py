from typing import Optional

from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    version: str = "latest"
    session_id: Optional[str] = None


class Citation(BaseModel):
    page: int
    section: str
    score: float

class QueryResponse(BaseModel):
    answer:str
    confidence:float
    citations:list[Citation]