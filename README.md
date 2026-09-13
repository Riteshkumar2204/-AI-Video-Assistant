
# 🧾 AI-Video-Assistant 

 AI Video Assistant is an AI-powered platform designed to analyze and understand video content. It converts YouTube videos and local media into transcripts, generates LLM-powered summaries, action items, key decisions, and open questions, and provides an interactive RAG-based Q&A system for querying video content.

### 🔧 Features

- **Video Processing**
  - Supports YouTube videos and local audio/video files.
  - Converts video/audio into text using **OpenAI Whisper**.
  - Handles long videos by processing audio in manageable chunks.
  - Provides complete video transcripts for further analysis.

- **AI-Powered Insights**
  - Generates video titles and concise summaries using **Mistral AI**.
  - Extracts important **action items, key decisions, and open questions**.
  - Converts raw transcripts into structured and meaningful insights.

- **Intelligent Q&A**
  - Allows users to ask questions about processed videos.
  - Uses **RAG with LangChain and ChromaDB** for contextual information retrieval.
  - Provides answers based on the actual video transcript.

## ⚙️ Local Setup

### 1. Clone the Repo
git clone https://github.com/Riteshkumar2204/-AI-Video-Assistant.git

### 2. Environment Variables
To run this project, you will need to add the following environment variables to your .env file
```env
MISTRAL_API_KEY=your_mistral_api_key
WHISPER_MODEL=base
SARVAM_API_KEY=your_sarvam_api_key
SARVAM_STT_MODEL=saaras:v2.5
```

### 3. Deployment

#### Run Application

```bash
streamlit run app.py
```


## 🚀Live Demo
https://aivideoassistance.streamlit.app/


## 🛠️ Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **AI/ML:** OpenAI Whisper, Mistral AI
- **RAG:** LangChain, ChromaDB
- **Video/Audio Processing:** yt-dlp, FFmpeg, Pydub
- **Embeddings:** Sentence Transformers
## 🔗 Links

[![Portfolio](https://img.shields.io/badge/MY%20PORTFOLIO-000000?style=for-the-badge&logo=googlechrome&logoColor=white)](YOUR_PORTFOLIO_LINK)

[![LinkedIn](https://img.shields.io/badge/LINKEDIN-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](YOUR_LINKEDIN_LINK)

[![GitHub](https://img.shields.io/badge/GITHUB-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Riteshkumar2204)

[![LeetCode](https://img.shields.io/badge/LEETCODE-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/u/oNL20WwRDU/)
