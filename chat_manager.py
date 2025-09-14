from ai_setup import chain, retriever

class ChatManager:
    def get_ai_response(self, question: str) -> str:
        """
        Retrieve relevant reviews and get streaming AI response.
        """
        reviews = retriever.invoke(question)
        response = ""
        for token in chain.stream({"reviews": reviews, "question": question}):
            response += token
        return response
