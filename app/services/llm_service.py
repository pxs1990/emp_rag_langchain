from langchain_google_genai import ChatGoogleGenerativeAI

class LLMService:

    def __init__(self):

        self.llm=ChatGoogleGenerativeAI(
            model="gemini-2.5-pro"
        )

    def answer(self, question, context):

        prompt=f"""
        Answer only using the context.
        Context:
        {context}
        Question:
        {question}

        Provide citations.
        """
        response=self.llm.invoke(prompt)

        return response.content