from langchain_community.vectorstores import FAISS

class VectorStoreService:

    def create_vector_store(self, documents, embeddings):
        return FAISS.from_documents(documents, embeddings)