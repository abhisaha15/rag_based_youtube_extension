import requests
from urllib.parse import urlparse, parse_qs
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("SUPADATA_API_KEY")


class TranscriptService:

    BASE_URL = "https://api.supadata.ai/v1/youtube/transcript"

    @staticmethod
    def parse_video_id(url: str) -> str:
        """Extract video ID from various YouTube URL formats"""
        parsed_url = urlparse(url)

        if parsed_url.hostname == "youtu.be":
            return parsed_url.path[1:]

        if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
            if "shorts" in parsed_url.path:
                return parsed_url.path.split("/shorts/")[1]
            return parse_qs(parsed_url.query).get("v", [None])[0]

        raise ValueError("Invalid YouTube URL")

    @staticmethod
    def fetch_transcript(video_id: str, language: str = "en") -> tuple[str, list[dict]]:
        """
        Fetch transcript from Supadata API

        Returns:
            (language_used, transcript_list)
        """

        if not API_KEY:
            raise ValueError("API key not found. Set SUPADATA_API_KEY in .env")

        response = requests.get(
            TranscriptService.BASE_URL,
            headers={"x-api-key": API_KEY},
            params={"videoId": video_id, "lang": language}
        )

        data = response.json()

        # Handle API errors
        if "error" in data:
            raise Exception(f"{data['error']}: {data.get('message', '')}")

        transcript = [
            {
                "text": chunk["text"],
                "start": chunk["offset"] / 1000,
                "duration": chunk["duration"] / 1000,
            }
            for chunk in data.get("content", [])
        ]

        return language, transcript

    @staticmethod
    def get_transcript(url: str, language: str = "en") -> dict:
        """
        Full pipeline:
        URL → video_id → transcript

        Returns structured response
        """

        video_id = TranscriptService.parse_video_id(url)
        detected_language, transcript = TranscriptService.fetch_transcript(
            video_id, language
        )

        return {
            "video_id": video_id,
            "language": detected_language,
            "transcript": transcript
        }