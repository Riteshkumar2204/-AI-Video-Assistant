
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()


def run_pipeline(source: str, language: str = "english") -> dict:
    print("Starting AI Video Assistant...")

    if not source or not source.strip():
        raise ValueError("Please provide a YouTube URL or local file path.")

    language = language.strip().lower()

    if language not in ("english", "hinglish"):
        raise ValueError("Language must be 'english' or 'hinglish'.")

    chunks = process_input(source.strip())

    if not chunks:
        raise ValueError("No audio chunks were generated.")

    print("Transcribing audio...")
    transcript = transcribe_all(chunks, language)

    if not transcript or not transcript.strip():
        raise ValueError("Transcription is empty.")

    print(f"Raw transcription (first 300 characters):\n{transcript[:300]}")

    print("Generating title...")
    title = generate_title(transcript)

    print("Generating summary...")
    summary = summarize(transcript)

    print("Extracting action items...")
    action_items = extract_action_items(transcript)

    print("Extracting key decisions...")
    decisions = extract_key_decisions(transcript)

    print("Extracting open questions...")
    questions = extract_questions(transcript)

    print("Building RAG question-answering system...")
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


if __name__ == "__main__":
    try:
        source = input("Enter YouTube URL or local file path: ").strip()
        language = input("Language (english/hinglish): ").strip() or "english"

        result = run_pipeline(source, language)

        print("\n" + "=" * 60)
        print(f"Title: {result['title']}")
        print(f"\nSummary:\n{result['summary']}")
        print(f"\nAction Items:\n{result['action_items']}")
        print(f"\nKey Decisions:\n{result['key_decisions']}")
        print(f"\nOpen Questions:\n{result['open_questions']}")
        print("=" * 60)

        print("\nChat with your video (type 'exit' to quit)\n")

        rag_chain = result["rag_chain"]

        while True:
            question = input("You: ").strip()

            if question.lower() in ("exit", "quit", "q"):
                print("Goodbye!")
                break

            if not question:
                continue

            try:
                answer = ask_question(rag_chain, question)
                print(f"\nAssistant: {answer}\n")
            except Exception as e:
                print(f"Error answering question: {e}")

    except Exception as e:
        print(f"\nPipeline failed: {e}")
