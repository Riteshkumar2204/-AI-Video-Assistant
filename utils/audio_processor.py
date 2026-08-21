# import yt_dlp
# from pydub import AudioSegment
# import os

# DOWNLOAD_DIR = 'downloades'
# os.makedirs(DOWNLOAD_DIR,exist_ok = True)

# def download_youtube_audio(url :str) ->str:
#     output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": output_path,
#         "postprocessors": [
#             {
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "wav",
#                 "preferredquality": "192",
#             }
#         ],
#         "quiet": True,
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(url, download=True)
#         filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
#     return filename



# def convert_to_wav(input_path: str) -> str:
#     """Convert any audio/video file to WAV format using pydub."""
#     output_path = os.path.splitext(input_path)[0] + "_converted.wav"
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_channels(1).set_frame_rate(16000) #16khz
#     audio.export(output_path, format="wav")
#     return output_path



# def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
#     audio = AudioSegment.from_wav(wav_path)
#     chunk_ms = chunk_minutes * 60 * 1000 

#     chunks = []

#     for i, start in enumerate(range(0,len(audio),chunk_ms)):
#         chunk = audio[start : start + chunk_ms]
#         chunk_path = f"{wav_path}_chunk_{i}.wav"
#         chunk.export(chunk_path , format = "wav")

#         chunks.append(chunk_path)
    
#     return chunks

# def process_input(source: str) -> list:
#     if source.startswith("http://") or source.startswith("https://"):
#         print("Detected YouTube URL. Downloading audio...")
#         wav_path = download_youtube_audio(source)
#     else:
#         print("Detected local file. Converting to WAV...")
#         wav_path = convert_to_wav(source)

#     print("Chunking audio...")
#     chunks = chunk_audio(wav_path)
#     print(f"Audio ready — {len(chunks)} chunk(s) created.")
#     return chunks




import os
import yt_dlp
from pydub import AudioSegment

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """Downloads YouTube audio and converts it directly to 16kHz Mono WAV."""
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "quiet": False,
        "noplaylist": True,
        "keepvideo": False,
        # Bypass YouTube "The page needs to be reloaded" SABR error
        "extractor_args": {
            "youtube": {
                "player_client": ["tv", "mweb", "android", "ios"]
            }
        },
        # Extract audio using FFmpeg
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        # Enforce 1 channel (mono) and 16000 Hz sample rate during extraction
        "postprocessor_args": {
            "ExtractAudio": ["-ac", "1", "-ar", "16000"]
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # Safely replace any extension (.webm, .mp4, .m4a) with .wav
        wav_path = os.path.splitext(filename)[0] + ".wav"
        return wav_path


def convert_to_wav(input_path: str) -> str:
    """Converts local audio/video files to 16kHz Mono WAV using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)  # 16kHz Mono
    audio.export(output_path, format="wav")
    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Splits a WAV file into N-minute chunk files."""
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []
    base_path = os.path.splitext(wav_path)[0]

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{base_path}_chunk_{i}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    """Entry point: processes YouTube URLs or local files into chunked WAVs."""
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    if not wav_path or not os.path.exists(wav_path):
        raise FileNotFoundError(f"Failed to process audio source: {source}")

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks