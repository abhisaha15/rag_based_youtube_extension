from langchain_google_genai import GoogleGenerativeAIEmbeddings

class EmbeddingService:

    def get_embeddings(self):
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )