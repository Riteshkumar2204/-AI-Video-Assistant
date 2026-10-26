
import os
from typing import Union
import whisper
from dotenv import load_dotenv

load_dotenv()

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

_model = None


def load_model():
    global _model
    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")
    return _model


def transcribe_chunk_whisper(chunk_path: str) -> str:
    model = load_model()
    result = model.transcribe(chunk_path, task="transcribe")
    return result["text"]


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    if language.lower() == "hinglish":
        result = load_model().transcribe(chunk_path, task="transcribe")
        return result["text"]

    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(
    chunks: Union[list, str], language: str = "english"
) -> str:
    if isinstance(chunks, str):
        chunks = [chunks]

    print("Using Whisper (Local) for transcription.")

    full_transcript = ""

    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_chunk(chunk, language=language)
        full_transcript += text + " "

    print("Transcription complete.")
    return full_transcript.strip()
