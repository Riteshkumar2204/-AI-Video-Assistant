
import os
import shutil
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """Download YouTube audio and convert it to 16kHz mono WAV."""

    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "FFmpeg is not installed or not added to PATH."
        )

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "keepvideo": False,
        "extractor_args": {
            "youtube": {
                "player_client": [
                    "web_safari",
                    "web_embedded",
                    "-tv_downgraded",
                ]
            }
        },
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "0",
            }
        ],
        "postprocessor_args": {
            "ExtractAudio": ["-ac", "1", "-ar", "16000"]
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        wav_path = os.path.splitext(filename)[0] + ".wav"

        if not os.path.exists(wav_path):
            raise FileNotFoundError(
                f"YouTube audio conversion failed: {wav_path}"
            )

        return wav_path


def convert_to_wav(input_path: str) -> str:
    """Convert local audio/video files to 16kHz mono WAV."""

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_path, format="wav")

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split a WAV file into chunks of the specified length."""

    if chunk_minutes <= 0:
        raise ValueError("chunk_minutes must be greater than zero.")

    if not os.path.isfile(wav_path):
        raise FileNotFoundError(f"Audio file not found: {wav_path}")

    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    base_path = os.path.splitext(wav_path)[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{base_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    """Process a YouTube URL or local file into WAV chunks."""

    if not source or not source.strip():
        raise ValueError("Please provide a YouTube URL or local file path.")

    source = source.strip()

    if source.startswith(("http://", "https://")):
        print("Detected URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    if not wav_path or not os.path.isfile(wav_path):
        raise FileNotFoundError(
            f"Failed to process audio source: {source}"
        )

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)

    if not chunks:
        raise ValueError("No audio chunks were generated.")

    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
