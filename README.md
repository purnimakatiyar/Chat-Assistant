# AI Chat Assistant

An AI-powered chat interface with real-time conversation insights.
Built with **FastAPI** (backend) · **React + Vite** (frontend) · **Groq AI** (LLM).

---

## Features

- Chat with an AI assistant powered by LLaMA 3.1 via Groq
- Per-message **intent** detection (15 categories) and **sentiment** analysis (7 levels)
- Conversation history maintained within the session
- Structured logging with rotating file output
- Health check endpoint for monitoring
- Docker support for production deployment

---

## Project Structure

```
chat-assistant/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── api/                # Route handlers
│   │   │   ├── chat.py         # POST /api/chat
│   │   │   └── health.py       # GET  /health
│   │   ├── core/               # App-wide configuration
│   │   │   ├── config.py       # Settings (pydantic-settings)
│   │   │   ├── constants.py    # All magic strings and prompt templates
│   │   │   ├── exceptions.py   # Custom exceptions + handlers
│   │   │   └── logging.py      # Console + rotating file logging setup
│   │   ├── middleware/
│   │   │   └── logging.py      # Request/response logging middleware
│   │   ├── schemas/
│   │   │   ├── chat.py         # ChatRequest, ChatResponse, Insights models
│   │   │   └── health.py       # HealthResponse model
│   │   ├── services/
│   │   │   ├── groq_client.py  # Groq client singleton
│   │   │   ├── chat_service.py # AI response generation
│   │   │   └── insight_service.py # Intent + sentiment extraction
│   │   └── main.py             # App factory (create_app)
│   ├── main.py                 # Uvicorn entrypoint
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   # React + Vite application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatContainer.jsx  # Parent — state management + API calls
│   │   │   ├── MessageList.jsx    # Renders message thread + typing indicator
│   │   │   ├── MessageItem.jsx    # Single bubble + insights badge
│   │   │   └── InputBox.jsx       # Textarea + send button
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   └── vite.config.js         # Proxies /api → localhost:8000
│
├── docker-compose.yml
└── README.md
```

---

## Prerequisites

| Tool | Minimum version |
|------|----------------|
| Python | 3.12 |
| Node.js | 18 |
| npm | 9 |
| Docker *(optional)* | 24 |

You will also need a free **Groq API key** → [console.groq.com](https://console.groq.com)

---

## Backend Setup

### 1. Create and activate a virtual environment

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `backend/.env` and set your Groq API key:

```env
GROQ_API_KEY=gsk_your_key_here
```

Full list of available settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | *(required)* | Your Groq API key |
| `GROQ_MODEL` | `llama-3.1-8b-instant` | Model to use |
| `GROQ_CHAT_MAX_TOKENS` | `512` | Max tokens for chat replies |
| `GROQ_INSIGHT_MAX_TOKENS` | `60` | Max tokens for insight extraction |
| `CORS_ORIGINS` | `["http://localhost:5173"]` | Allowed frontend origins |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_TO_FILE` | `true` | Write logs to file |
| `LOG_FILE_PATH` | `logs/app.log` | Log file location |

### 4. Start the development server

```bash
uvicorn main:app --reload --port 8000
```

The API is now running at `http://localhost:8000`
Interactive docs are available at `http://localhost:8000/docs`

---

## Frontend Setup

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Start the development server

```bash
npm run dev
```

The app is now running at `http://localhost:5173`

> The Vite dev server automatically proxies all `/api` requests to `http://localhost:8000`, so no extra CORS configuration is needed during development.

---

## Running with Docker

Build and start the backend container:

```bash
# From the project root
docker compose up --build
```

Or build and run the image directly:

```bash
cd backend
docker build -t chat-assistant-backend .
docker run --env-file .env -p 8000:8000 chat-assistant-backend
```

Environment variables can be overridden at runtime:

```bash
docker run --env-file .env -e WORKERS=4 -e LOG_LEVEL=DEBUG -p 8000:8000 chat-assistant-backend
```

---

## API Reference

### `POST /api/chat`

Send a user message and receive an AI response with conversation insights.

**Request body:**
```json
{
  "message": "My order hasn't arrived yet and it's been two weeks!",
  "history": [
    { "role": "user",      "content": "Hi there" },
    { "role": "assistant", "content": "Hello! How can I help you?" }
  ]
}
```

**Response:**
```json
{
  "response": "I'm sorry to hear that. Let me help you track your order...",
  "insights": {
    "intent": "complaint",
    "sentiment": "negative"
  }
}
```

### `GET /health`

Returns service health and dependency status.

```json
{
  "status": "ok",
  "version": "1.0.0",
  "dependencies": {
    "groq": { "status": "ok" }
  }
}
```

Returns `503` with `"status": "degraded"` if Groq is unreachable.

---

## Conversation Insights

### Intent categories (15)

| Intent | Description |
|--------|-------------|
| `greeting` | Opening hello or hi |
| `farewell` | Goodbye or sign-off |
| `query` | Asking for information |
| `request` | Asking the assistant to do something |
| `complaint` | Expressing dissatisfaction |
| `praise` | Complimenting or appreciating |
| `feedback` | Giving an opinion or suggestion |
| `clarification` | Asking to rephrase or expand |
| `confirmation` | Verifying or agreeing |
| `denial` | Disagreeing or correcting |
| `troubleshooting` | Reporting a technical problem |
| `small_talk` | Casual conversation |
| `opinion` | Sharing a personal view |
| `urgent` | Time-sensitive or emergency message |
| `other` | Anything else |

### Sentiment levels (7)

| Sentiment | Meaning |
|-----------|---------|
| `very_positive` | Enthusiastic, excited, delighted |
| `positive` | Happy, satisfied, pleased |
| `slightly_positive` | Mildly happy or content |
| `neutral` | No emotional tone |
| `slightly_negative` | Mildly unhappy or disappointed |
| `negative` | Frustrated, unhappy, upset |
| `very_negative` | Angry, furious, extremely distressed |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend framework | React 18 |
| Frontend build tool | Vite |
| Backend framework | FastAPI |
| AI provider | Groq (LLaMA 3.1 8B Instant) |
| Data validation | Pydantic v2 |
| Logging | Python `logging` + RotatingFileHandler |
| Containerisation | Docker (multi-stage build) |
