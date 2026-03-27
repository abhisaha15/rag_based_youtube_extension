from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:

    def __init__(self, chunk_size=800, chunk_overlap=150):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def process(self, transcript: list[dict]) -> list[Document]:
        """
        Convert transcript → chunked documents with metadata
        """

        # Step 1: Convert to Documents with timestamps
        documents = [
            Document(
                page_content=item["text"],
                metadata={
                    "start": item["start"],
                    "end": item["start"] + item["duration"]
                }
            )
            for item in transcript
        ]

        # Step 2: Chunk documents
        chunked_documents = self.splitter.split_documents(documents)

        return chunked_documents