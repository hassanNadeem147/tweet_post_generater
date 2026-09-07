# Automated Tweet Post Generator

An AI-powered web application that generates engaging tweets from a simple topic or idea.

Enter a topic such as **Artificial Intelligence**, and the application uses an LLM with a **LangGraph** workflow to generate a concise tweet ready to post.

## Features

- Generate a tweet from any topic
- LLM-powered tweet generation
- LangGraph workflow
- LangChain integration
- FastAPI backend
- Next.js frontend
- Pydantic request validation
- Simple project structure
- Easy local development setup

## Tech Stack

### Backend

- Python
- FastAPI
- LangChain
- LangGraph
- Pydantic
- OpenAI / LLM

### Frontend

- Next.js
- React
- Node.js
- npm

## Project Structure

```text
tweet_post_generater/
│
├── app/
│   ├── graph/
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── routes/
│   │   └── tweet_route.py
│   │
│   ├── schema/
│   │   └── tweet_schema.py
│   │
│   └── main.py
│
├── frontend/
│   └── nextjs/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

### Folder Overview

| File / Folder | Purpose |
|---|---|
| `app/` | Main backend application |
| `app/graph/` | LangGraph workflow and AI logic |
| `app/graph/nodes.py` | Workflow nodes |
| `app/graph/state.py` | LangGraph state |
| `app/graph/workflow.py` | LangGraph workflow definition |
| `app/routes/` | FastAPI API routes |
| `app/routes/tweet_route.py` | Tweet generation endpoint |
| `app/schema/` | Pydantic request/response schemas |
| `app/schema/tweet_schema.py` | Tweet API schemas |
| `app/main.py` | FastAPI application entry point |
| `frontend/nextjs/` | Next.js frontend |

## How It Works

```text
User
  │
  │ Enter topic
  ▼
Next.js Frontend
  │
  │ HTTP Request
  ▼
FastAPI Backend
  │
  ▼
LangGraph Workflow
  │
  ▼
LLM
  │
  │ Generate tweet
  ▼
FastAPI Response
  │
  ▼
Next.js Frontend
  │
  ▼
Generated Tweet
```

### Workflow

1. The user enters a topic in the Next.js frontend.
2. The frontend sends the topic to the FastAPI backend.
3. FastAPI validates the request with Pydantic.
4. The request is passed to the LangGraph workflow.
5. LangGraph executes the configured workflow nodes.
6. The LLM generates the tweet.
7. The generated tweet is returned by the backend.
8. The frontend displays the generated tweet.

## Requirements

Make sure you have:

- Python 3.13+
- Node.js 18+
- npm
- An API key for the configured LLM provider

Check your installed versions:

```bash
python --version
node --version
npm --version
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hassanNadeem147/tweet_post_generater.git
cd tweet_post_generater
```

### 2. Create a Python Virtual Environment

The backend uses a Python virtual environment.

#### Windows

```bash
py -3.13 -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Or in PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

### 3. Install Backend Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a template.

```env
OPENAI_API_KEY=your-openai-api-key
```

> **Important:** Never commit `.env` or your real API keys to GitHub.

## Run the Backend

From the project root, with the virtual environment activated:

```bash
python app/main.py
```

The FastAPI backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI interactive documentation:

```text
http://127.0.0.1:8000/docs
```

## Run the Frontend

Open a second terminal.

Go to the Next.js application:

```bash
cd frontend/nextjs
```

Install frontend dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:3000
```

## Generate a Tweet

After starting both the backend and frontend:

1. Open `http://localhost:3000`
2. Enter a topic, for example:

   ```text
   Artificial Intelligence
   ```

3. Click **Generate**.
4. The frontend sends the topic to the backend.
5. LangGraph runs the AI workflow.
6. The LLM generates the tweet.
7. The generated tweet is displayed in the frontend.

## API

The tweet generation API is defined in:

```text
app/routes/tweet_route.py
```

You can view and test the available endpoints through:

```text
http://127.0.0.1:8000/docs
```

The exact endpoint and request format depend on the implementation.

## LangGraph Workflow

The LangGraph implementation is located in:

```text
app/graph/
```

### Main Files

- `state.py` — defines the workflow state
- `nodes.py` — contains the workflow nodes
- `workflow.py` — builds and connects the LangGraph workflow

The workflow can later be extended:

```text
Topic
  │
  ▼
Generate Tweet
  │
  ▼
Review Tweet
  │
  ▼
Improve Tweet
  │
  ▼
Final Tweet
```

## Environment and Git

Do **not** commit these files or folders:

```text
.env
.venv/
venv/
node_modules/
.next/
__pycache__/
```

These files should be committed:

```text
.env.example
.gitignore
requirements.txt
frontend/nextjs/package.json
frontend/nextjs/package-lock.json
README.md
```

## Future Improvements

- Generate multiple tweet variations
- Add different writing styles
- Add tone selection
- Add tweet length control
- Add hashtag generation
- Add tweet quality scoring
- Add tweet regeneration
- Generate Twitter/X threads
- Add authentication
- Store generated tweets
- Add database support
- Add automated testing
- Deploy the application

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes.
4. Commit your changes:

```bash
git commit -m "Add new feature"
```

5. Push your branch:

```bash
git push origin feature/my-feature
```

6. Open a Pull Request.

## License

This project is available for learning and development purposes.

## Project Goal

This project demonstrates how **LangGraph, LangChain, LLMs, FastAPI, Pydantic, and Next.js** can be combined to build a simple end-to-end AI application.

The project is intentionally kept small so the backend, frontend, API communication, and LangGraph workflow are easy to understand and extend.
