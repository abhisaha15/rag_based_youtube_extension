from fastapi import FastAPI, HTTPException
from models.request_models import VideoRequest

from services.transcript_service import TranscriptService
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from services.rag_service import RAGService

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API running 🚀"}


@app.post("/summarize")
async def summarize_video(request: VideoRequest):
    try:
        transcript_data = TranscriptService.get_transcript(request.youtube_url)
        transcript = transcript_data["transcript"]

        chunking_service = ChunkingService()
        documents = chunking_service.process(transcript)

        embedding_service = EmbeddingService()
        embeddings = embedding_service.get_embeddings()

        vector_store_service = VectorStoreService()
        vector_store = vector_store_service.create_vector_store(documents, embeddings)

        rag_service = RAGService(vector_store)
        answer = rag_service.generate_answer(request.question)

        return {
            "video_id": transcript_data["video_id"],
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))