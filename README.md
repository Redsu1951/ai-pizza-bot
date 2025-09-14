# 🍕 AI Pizza Bot

A Retrieval-Augmented Generation (RAG) chatbot with a retro **pygame** UI and local **Ollama + LangChain** LLM backend.

## 🚀 Features
- Local **LLM inference** with Ollama
- RAG over restaurant reviews (Chroma vector DB)
- **pygame UI** with:
  - Video background
  - Transparent chatbox
  - Typing animation for AI responses
- Streaming output letter by letter

## 🛠️ Tech Stack
- Python
- LangChain
- Ollama
- ChromaDB
- pygame + OpenCV
- CUDA acceleration (RTX 3050 GPU)

## ▶️ Run
```bash
git clone https://github.com/USERNAME/ai-pizza-bot.git
cd ai-pizza-bot
python -m venv venv
.\venv\Scripts\Activate.ps1   # (Windows PowerShell)
pip install -r requirements.txt
python main.py
