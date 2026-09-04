🎙️ AI Interview Coach
<p align="center"> <strong>AI-powered interview preparation with personalized text and voice interactions.</strong> </p>
Overview

AI Interview Coach is a personalized interview preparation platform that uses a candidate's resume and job description to conduct adaptive mock interviews.

It combines RAG, LLMs, speech-to-text, text-to-speech, FastAPI, React, PostgreSQL, and ChromaDB to create a realistic interview experience.

Core Flow
Resume + Job Description
          ↓
     RAG Retrieval
          ↓
   Interview Context
          ↓
    AI Question
          ↓
 ┌────────┴────────┐
 ↓                 ↓
Text Answer     Voice Answer
 ↓                 ↓
AI Evaluation   Speech-to-Text
 ↓                 ↓
 └────────┬────────┘
          ↓
   Next Question
          ↓
   Final Feedback
✨ Features
Resume-Aware Interviews — Questions are tailored to the candidate's background.
Job-Specific Questions — Uses the target job description to focus the interview.
RAG Pipeline — Retrieves relevant information from uploaded documents using ChromaDB.
Adaptive Interviews — Previous questions, answers, and evaluations influence what comes next.
Text-to-Text Mode — Type answers and receive AI-generated questions and feedback.
Voice-to-Voice Mode — Listen to spoken questions and respond naturally using your voice.
AI Evaluation — Analyzes answer quality, relevance, strengths, and improvement areas.
Interview Feedback — Provides personalized insights and knowledge gaps.
🏗️ Architecture
React + Vite
     │
     ▼
FastAPI Backend
     │
 ┌───┼───────────────┐
 ▼   ▼               ▼
RAG  LLM         Voice Services
 │   │               │
 ▼   ▼          Whisper + TTS
ChromaDB
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
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── services/
│   │   └── schemas/
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
1. Clone
git clone https://github.com/ImranNadeem444/ai-interview-coach.git
cd ai-interview-coach
2. Backend
cd backend
python -m venv venv

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
3. Frontend
cd frontend
npm install
npm run dev
4. Environment

Create .env from .env.example and configure your local database and required API credentials.

Never commit .env or secret keys.

🔄 Interview Workflow
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
📌 Project Status

Active Development

Current focus includes improving voice interaction, adaptive evaluation, feedback quality, and the overall interview experience.

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

<p align="center"> ⭐ If you find the project useful, consider starring the repository. </p>
