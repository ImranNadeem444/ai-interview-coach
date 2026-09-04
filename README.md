# 🎙️ AI Interview Coach

> AI-powered interview preparation with personalized text and voice interactions.

---

## 📌 Overview

**AI Interview Coach** is a personalized interview preparation platform that uses a candidate's **resume** and **job description** to conduct adaptive mock interviews.

It combines **RAG, LLMs, speech-to-text, text-to-speech, FastAPI, React, PostgreSQL, and ChromaDB** to create a realistic interview experience.

---

## ✨ Features

- 📄 **Resume-Aware Interviews** — Questions are tailored to the candidate's background.
- 💼 **Job-Specific Questions** — Uses the target job description to focus the interview.
- 🧠 **RAG Pipeline** — Retrieves relevant information from uploaded documents using ChromaDB.
- 🔄 **Adaptive Interviews** — Previous questions, answers, and evaluations influence what comes next.
- 💬 **Text-to-Text Mode** — Type answers and receive AI-generated questions and feedback.
- 🎙️ **Voice-to-Voice Mode** — Listen to spoken questions and respond naturally using your voice.
- 📊 **AI Evaluation** — Analyzes answer quality, relevance, strengths, and improvement areas.
- 📝 **Interview Feedback** — Provides personalized insights and knowledge gaps.

---

## 🔄 Core Flow

```text
Resume + Job Description
          ↓
     RAG Retrieval
          ↓
   Interview Context
          ↓
    AI Question
          ↓
   ┌──────┴──────┐
   ↓             ↓
Text Answer   Voice Answer
   ↓             ↓
   └──────┬──────┘
          ↓
    AI Evaluation
          ↓
   Next Question
          ↓
   Final Feedback


              React + Vite
                     │
                     ▼
               FastAPI Backend
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
         RAG        LLM    Voice Services
          │          │          │
          ▼          ▼          ▼
      ChromaDB   LangChain   Whisper + TTS
                     │
                     ▼
                PostgreSQL
🛠️ Tech Stack
Layer	Technology
Frontend	React, Vite
Backend	FastAPI, Python
LLM	LangChain
RAG	ChromaDB
Database	PostgreSQL
Speech-to-Text	Faster-Whisper
Text-to-Speech	TTS
Migrations	Alembic
Testing	Pytest
Containerization	Docker
📁 Project Structure
ai-interview-coach/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── services/
│   │   └── schemas/
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/ImranNadeem444/ai-interview-coach.git
cd ai-interview-coach
2. Backend Setup
cd backend
python -m venv venv

Windows

venv\Scripts\activate

macOS / Linux

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Start the backend:

uvicorn app.main:app --reload
3. Frontend Setup

Open a new terminal:

cd frontend
npm install
npm run dev
4. Environment Configuration

Create a .env file from .env.example and configure your local database and required API credentials.

Never commit .env or secret keys to GitHub.

🎤 Interview Workflow
Upload Resume
      ↓
Add Job Description
      ↓
Start Interview
      ↓
AI Generates Question
      ↓
Text or Voice Answer
      ↓
AI Evaluates Answer
      ↓
Adaptive Next Question
      ↓
Final Interview Feedback
🧠 How It Works
Resume & Job Description

The candidate provides their resume and target job description.

RAG

Documents are processed, chunked, embedded, and stored in ChromaDB for retrieval.

Question Generation

The LLM uses the retrieved context and interview history to generate relevant questions.

Answer Processing

Answers can be provided through:

Text-to-Text
Voice-to-Voice

Voice responses are converted to text using Faster-Whisper before evaluation.

Evaluation

The AI evaluates the candidate's response and uses the result to guide the next question.

📌 Project Status

Active Development

Current focus:

Improving voice interaction
Improving adaptive evaluation
Improving feedback quality
Refining the overall interview experience
🗺️ Roadmap
 Advanced interview analytics
 Personalized learning recommendations
 Improved voice interaction
 Authentication and user accounts
 Persistent interview history
 Production deployment
👨‍💻 Author
Imran Nadeem

AI/ML Engineer · Software Developer · LLM & Generative AI

<p align="center"> ⭐ If you find the project useful, consider starring the repository. </p> ```
