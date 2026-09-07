# Automated Tweet Post Generator

An AI-powered web application that generates engaging tweets from a topic or idea.

Enter a topic such as **Artificial Intelligence**, and the application uses an LLM with a **LangGraph** workflow to generate a concise tweet ready to post.

## Features

- Generate a tweet from any topic
- LLM-powered tweet generation
- LangGraph workflow
- LangChain integration
- FastAPI backend
- Next.js frontend
- Pydantic request validation
- Simple and clean project structure
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
- JavaScript / TypeScript
- Node.js
- npm

## Project Structure

```text
automated-tweet-post-generator/
│
├── app/
│   ├── graph/
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── models/
│   │
│   ├── routes/
│   │   └── tweet_route.py
│   │
│   ├── schema/
│   │
│   └── main.py
│
├── frontend/
│   └── nextjs/
│
├── .env
├── .env-example
├── .gitignore
├── README.md
└── requirements.txt
```

### Backend Structure

| File / Folder | Description |
|---|---|
| `app/` | Main backend application |
| `app/graph/` | LangGraph workflow |
| `app/graph/nodes.py` | AI workflow nodes |
| `app/graph/state.py` | Workflow state |
| `app/graph/workflow.py` | LangGraph workflow definition |
| `app/models/` | Application models |
| `app/routes/` | FastAPI routes |
| `app/routes/tweet_route.py` | Tweet generation API |
| `app/schema/` | Pydantic schemas |
| `app/main.py` | FastAPI application entry point |

### Frontend

The Next.js application is located in:

```text
frontend/nextjs/
```

Its dependencies are installed with `npm install` and stored locally in `node_modules/`.

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
3. FastAPI validates the request using Pydantic.
4. The request is passed to the LangGraph workflow.
5. LangGraph executes the configured workflow nodes.
6. The LLM generates the tweet.
7. The generated tweet is returned by the backend.
8. The frontend displays the result.

## Requirements

Make sure the following are installed:

- Python 3.10+
- Node.js 18+
- npm
- An API key for the configured LLM provider

Check your versions:

```bash
python --version
node --version
npm --version
```

## Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a Python Virtual Environment

It is recommended to use a virtual environment for the backend.

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
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Backend Dependencies

From the project root:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Use `.env-example` as a template:

```env
OPENAI_API_KEY=your-openai-api-key
```

> **Important:** Never commit `.env` or your real API keys to GitHub.

Make sure `.env` is included in `.gitignore`.

### 5. Start the Backend

From the project root:

```bash
python app/main.py
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

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

The frontend will be available at:

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
4. The topic is sent to the backend.
5. The LangGraph workflow generates a tweet using the LLM.
6. The generated tweet is displayed in the frontend.

## API

The tweet generation API is defined in:

```text
app/routes/tweet_route.py
```

You can inspect the available API endpoints using FastAPI's interactive documentation:

```text
http://127.0.0.1:8000/docs
```

The exact endpoint and request schema depend on the implementation.

## LangGraph Workflow

The LangGraph implementation is located in:

```text
app/graph/
```

The main components are:

- `state.py` — defines the workflow state
- `nodes.py` — contains workflow nodes
- `workflow.py` — builds and connects the LangGraph workflow

The workflow can later be extended with additional steps such as:

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

The following files should **not** be committed:

```text
.env
.venv/
venv/
node_modules/
.next/
__pycache__/
```

The following files should be committed:

```text
.env-example
.gitignore
requirements.txt
frontend/nextjs/package.json
frontend/nextjs/package-lock.json
README.md
```

## Future Improvements

- Generate multiple tweet variations
- Add tone and writing-style options
- Add tweet length controls
- Generate hashtags
- Add tweet quality scoring
- Add tweet regeneration
- Generate Twitter/X threads
- Add authentication
- Store generated tweets
- Add database support
- Add automated tests
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

The project is intentionally kept small so the backend, frontend, API flow, and LangGraph workflow are easy to understand and extend.
