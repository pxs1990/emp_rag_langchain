from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings


class EmbeddingService:

    def __init__(self):

        self.model = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )

    def embed(self, text):

        return self.model.embed_query(text)