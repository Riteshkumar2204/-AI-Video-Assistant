
from dotenv import load_dotenv

load_dotenv()

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)

source = "https://www.youtube.com/watch?v=_Q-e_nczWqM&t=223s"
language = "english"  # "english" or "hinglish"

try:
    print("Processing video...")
    chunks = process_input(source)

    if not chunks:
        raise ValueError("No audio chunks were generated.")

    print("Transcribing audio...")
    transcript = transcribe_all(chunks, language=language)

    if not transcript or not transcript.strip():
        raise ValueError("Transcription is empty.")

    print("\n" + "=" * 60)
    print("📝 TRANSCRIPT")
    print("=" * 60)
    print(transcript[:500] + "..." if len(transcript) > 500 else transcript)

    print("\nGenerating title and summary...")
    title = generate_title(transcript)
    summary = summarize(transcript)

    print("\n" + "=" * 60)
    print(f"📌 TITLE: {title}")
    print("=" * 60)
    print("\n📋 SUMMARY")
    print("-" * 60)
    print(summary)

    print("\nExtracting key information...")
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    print("\n" + "=" * 60)
    print("✅ ACTION ITEMS")
    print("=" * 60)
    print(action_items)

    print("\n" + "=" * 60)
    print("🔑 KEY DECISIONS")
    print("=" * 60)
    print(decisions)

    print("\n" + "=" * 60)
    print("❓ OPEN QUESTIONS")
    print("=" * 60)
    print(questions)

except Exception as e:
    print(f"\nError: {e}")
