from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class RAGService:

    def __init__(self, vector_store):
        self.retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )

        self.prompt = PromptTemplate(
            template="""
You are a helpful assistant.

Answer ONLY from the provided transcript context.
If the context is insufficient, say "I don't know".

Provide:
- A clear summary
- Key points (bullet format)

Context:
{context}

Question:
{question}
""",
            input_variables=["context", "question"]
        )

    def retrieve_context(self, query: str) -> str:
        docs = self.retriever.invoke(query)
        return "\n\n".join(doc.page_content for doc in docs)

    def generate_answer(self, query: str) -> str:
        context = self.retrieve_context(query)

        final_prompt = self.prompt.invoke({
            "context": context,
            "question": query
        })

        response = self.llm.invoke(final_prompt)

        return response.content

    def summarize_video(self) -> str:
        query = "Summarize the video based on the transcript"
        return self.generate_answer(query)