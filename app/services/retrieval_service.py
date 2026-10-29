class RetrievalService:

    def search(self,question):

        vector_results = self.vector_search(
            question
        )

        keyword_results = self.keyword_search(
            question
        )

        merged = self.merge(
            vector_results,
            keyword_results
        )

        return merged[:5]