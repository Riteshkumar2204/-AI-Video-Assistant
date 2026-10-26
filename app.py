
import os
import streamlit as st
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

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False


def run_analysis(source, language):
    progress = st.progress(0)
    status = st.empty()

    try:
        status.info("Step 1/5: Processing video or audio...")
        chunks = process_input(source)
        progress.progress(20)

        if not chunks:
            raise ValueError("No audio chunks were generated.")

        status.info("Step 2/5: Transcribing audio...")
        transcript = transcribe_all(chunks, language)

        if not transcript or not transcript.strip():
            raise ValueError("No transcript was generated.")

        progress.progress(40)

        status.info("Step 3/5: Generating summary and title...")
        title = generate_title(transcript)
        summary = summarize(transcript)
        progress.progress(60)

        status.info("Step 4/5: Extracting important information...")
        action_items = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions = extract_questions(transcript)
        progress.progress(80)

        status.info("Step 5/5: Building the question-answering system...")
        rag_chain = build_rag_chain(transcript)
        progress.progress(100)

        st.session_state.result = {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "decisions": decisions,
            "questions": questions,
            "rag_chain": rag_chain,
        }

        st.session_state.chat_history = []
        st.session_state.pipeline_done = True

        status.success("Analysis completed successfully!")

    except Exception as e:
        st.session_state.pipeline_done = False
        status.error(f"Analysis failed: {e}")

    finally:
        progress.empty()


st.title("🎥 AI Video Assistant")
st.caption("TRANSCRIBE · SUMMARISE · ANALYSE · CHAT")

st.write(
    "Upload your own content through a local file path or provide a "
    "YouTube URL to generate summaries and ask questions about the content."
)

with st.sidebar:
    st.header("⚙️ Settings")

    source = st.text_input(
        "YouTube URL or File Path",
        placeholder="Paste a YouTube URL or local file path",
        key="source_input",
    )

    language = st.selectbox(
        "Transcription Language",
        ["English", "Hinglish"],
        index=0,
    )

    st.caption("Local AI models run through Ollama.")

    model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
    st.write(f"**LLM model:** `{model_name}`")

    analyse_clicked = st.button(
        "🚀 Analyse Content",
        use_container_width=True,
        type="primary",
    )

    if st.button("🗑️ Clear Results", use_container_width=True):
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_done = False
        st.rerun()

    if st.session_state.pipeline_done:
        st.success("Pipeline completed")
    else:
        st.info("Ready to analyse")


if analyse_clicked:
    if not source.strip():
        st.warning("Please enter a YouTube URL or local file path.")
    else:
        run_analysis(source.strip(), language)


result = st.session_state.result

if result:
    st.divider()

    st.header(f"📌 {result['title']}")

    st.subheader("📋 Summary")
    with st.container(border=True):
        st.markdown(result["summary"])

    with st.expander("📄 View Full Transcript"):
        st.text(result["transcript"])

    st.divider()
    st.subheader("🔍 Key Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ Action Items")
        with st.container(border=True):
            st.markdown(str(result["action_items"]))

    with col2:
        st.markdown("### 💡 Key Decisions")
        with st.container(border=True):
            st.markdown(str(result["decisions"]))

    with col3:
        st.markdown("### ❓ Open Questions")
        with st.container(border=True):
            st.markdown(str(result["questions"]))

    st.divider()
    st.header("💬 Chat with Your Video")
    st.caption(
        "Ask questions about the transcript. Answers are generated "
        "using retrieval-augmented generation (RAG)."
    )

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    with st.form("chat_form", clear_on_submit=True):
        question = st.text_input(
            "Ask a question",
            placeholder="What are the main points discussed?",
        )
        send_clicked = st.form_submit_button(
            "Send",
            use_container_width=True,
        )

    if send_clicked:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            st.session_state.chat_history.append(
                {"role": "user", "content": question.strip()}
            )

            try:
                with st.spinner("Thinking..."):
                    answer = ask_question(
                        result["rag_chain"],
                        question.strip(),
                    )

                if answer is None:
                    answer = "I couldn't generate an answer."

                answer = str(answer)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Could not answer the question: {e}")

            st.rerun()

else:
    st.divider()
    st.info(
        "Enter a YouTube URL or local audio/video file path in the sidebar "
        "and click **Analyse Content** to get started."
    )
