# TweetAI Generator

TweetAI Generator is a full-stack application that turns a topic or idea into a polished tweet. The backend uses FastAPI and a LangGraph workflow to generate, review, and improve the tweet with OpenRouter-hosted language models. The frontend is a Next.js writing studio with style presets, copy support, and browser-local generation history.

## What It Does

1. The user enters a topic and selects a writing style in the Next.js frontend.
2. The frontend sends the topic to the FastAPI endpoint `POST /api/generate_tweet`.
3. FastAPI validates the request with Pydantic.
4. LangGraph generates an initial tweet.
5. A reviewer model checks relevance, clarity, length, tone, and formatting.
6. If the tweet is rejected, an improvement model revises it.
7. The workflow repeats review and improvement until the tweet is approved or five iterations have been reached.
8. The final tweet is returned to the frontend and saved in the browser's local storage history.

The generated tweet is instructed to be plain text, between 150 and 280 characters, without hashtags, markdown, greetings, or unnecessary symbols.

## Technology

### Backend

- Python 3.13+
- FastAPI
- Uvicorn
- Pydantic and pydantic-settings
- LangChain
- LangGraph
- `langchain-openrouter`
- Loguru

### Frontend

- Next.js 15.5.25
- React 19
- TypeScript
- CSS
- Node.js and npm

## Project Structure

```text
 tweet_post_generater/
 ├── app/
 │   ├── config/
 │   │   └── settings.py              # Environment-backed application settings
 │   ├── graph/
 │   │   ├── nodes.py                 # Generate, review, improve, and routing logic
 │   │   ├── state.py                 # LangGraph state and reviewer schema
 │   │   └── workflow.py               # LangGraph graph definition
 │   ├── logging/
 │   │   └── logger.py                # Console and rotating file logging
 │   ├── routes/
 │   │   └── tweet_route.py            # Tweet generation API endpoint
 │   ├── schema/
 │   │   └── tweet_schema.py           # Request and response models
 │   ├── tests/
 │   │   └── tweet_generation_workflow_test.py
 │   ├── Dockerfile                     # Backend container image
 │   └── main.py                       # FastAPI application entry point
 ├── frontend/
 │   └── nextjs/
 │       ├── app/
 │       │   ├── page.tsx              # Interactive generator page
 │       │   ├── layout.tsx            # App metadata and root layout
 │       │   └── globals.css            # Frontend visual system
 │       ├── next.config.mjs           # API rewrite to FastAPI
 │       ├── package.json
 │       ├── tsconfig.json
 │       ├── Dockerfile                # Frontend production image
 │       └── .dockerignore             # Frontend build-context exclusions
 ├── logs/                             # Runtime log files
 ├── docker-compose.yaml               # Backend/frontend service orchestration
 ├── .dockerignore                     # Backend build-context exclusions
 ├── .env-example                      # Backend environment template
 ├── .gitignore
 ├── requirements.txt
 └── README.md
```

Generated folders such as `.venv`, `__pycache__`, `node_modules`, and `.next` are local runtime/build artifacts and should not be committed.

## Prerequisites

Install the following before starting the project:

- Python 3.13 or newer
- Node.js 18 or newer
- npm
- An OpenRouter API key with access to the configured models

Verify the tools:

```powershell
python --version
node --version
npm --version
```

## Configuration

Create a `.env` file in the repository root. Use `.env-example` as the template:

```env
OPENROUTER_API_KEY=your-openrouter-api-key
MODEL_NAME_TWEET_GENERATION=liquid/lfm-2.5-2.6b:free
TEMPERATURE_TWEET_GENERATION=0.7
MODEL_NAME_TWEET_REVIEW=minimax/minimax-m3:free
TEMPERATURE_TWEET_REVIEW=0.3
MODEL_NAME_IMPROVE_TWEET=liquid/lfm-2.5-2.6b:free
TEMPERATURE_IMPROVE_TWEET=0.7
```

`app/config/settings.py` loads these values from `.env` when the backend starts. Never commit `.env` or expose the API key in frontend code.

## Backend Setup

From the repository root, create and activate the Python virtual environment.

### Windows PowerShell

```powershell
py -3.13 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Start the API from the repository root:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at:

- API root: `http://127.0.0.1:8000/`
- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

The backend is started with Uvicorn. Running `python app/main.py` does not start a server because `app/main.py` defines the FastAPI application but does not call Uvicorn directly.

## Frontend Setup

Open a second terminal and move to the Next.js directory:

```powershell
cd frontend\nextjs
npm install
npm run dev
```

Open `http://localhost:3000` in a browser. If that port is already in use, Next.js selects another available port and prints it in the terminal.

The frontend sends requests to `/api/generate_tweet`. `next.config.mjs` rewrites that request to:

```text
http://127.0.0.1:8000/api/generate_tweet
```

This keeps the browser request same-origin and avoids requiring frontend CORS configuration during local development.

## Run with Docker

Docker Compose runs the backend and frontend as separate services. The backend is published on port `8000`, and the frontend is published on port `3000`.

Create a valid `.env` file in the repository root before starting the stack. Compose passes it to the backend container. Keep the OpenRouter API key out of the frontend image and out of `docker-compose.yaml`.

From the repository root:

```powershell
docker compose up --build
```

Open `http://localhost:3000` after startup. The frontend container reaches the backend through the Docker service name `backend` at `http://backend:8000`. Inside a container, `127.0.0.1` refers to that same container.

Run in the background:

```powershell
docker compose up --build -d
```

Check service status and logs:

```powershell
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
```

The backend health check must pass before Compose starts the frontend. Application logs are persisted to the host through `./logs:/app/logs`:

```text
logs/app_info.log
logs/app_error.log
```

Stop the stack:

```powershell
docker compose down
```

Rebuild from scratch after Dockerfile or dependency changes:

```powershell
docker compose down
docker compose build --no-cache
docker compose up
```

Direct image builds:

```powershell
docker build -f app/Dockerfile -t tweetai-backend .
docker build -t tweetai-frontend frontend/nextjs
```

For local development, Compose is recommended because it configures service networking, environment variables, log persistence, and health-based startup ordering.

## Frontend Features

- Topic textarea with a 500-character input limit
- Professional, Casual, Funny, Informative, and Engaging style presets
- Starter topic suggestions
- Loading and validation states
- Generated tweet display with character count
- Copy-to-clipboard action
- Recent generation history stored in browser local storage
- Responsive layout for desktop and mobile screens
- Clear display of backend error details, including provider rate-limit responses

The selected style is included in the topic sent to the current backend contract. The API intentionally accepts one `topic` string and returns one `tweet` string.

## API Reference

### `GET /`

Returns a basic health and welcome message.

### `POST /api/generate_tweet`

Request body:

```json
{
  "topic": "The future of AI in healthcare"
}
```

Successful response:

```json
{
  "tweet": "A generated tweet appears here."
}
```

The endpoint returns HTTP `200` when generation completes, including when the workflow stops after the maximum number of review iterations.

When the OpenRouter provider rate limit is reached, the endpoint returns HTTP `429`:

```json
{
  "detail": "The AI provider rate limit has been reached. Please try again later or add credits to your OpenRouter account."
}
```

Unexpected workflow failures continue to return an error response and are recorded with their traceback in the error log.

## LangGraph Workflow

The graph in `app/graph/workflow.py` follows this path:

```text
START
  |
  v
Generate tweet
  |
  v
Review tweet
  |---------------- approved ----------------> END
  |
 rejected
  v
Improve tweet
  |
  +----------------------> Review tweet
```

The workflow state contains the topic, current tweet, reviewer decision, feedback, current iteration, maximum iteration count, and an improvement field. The router ends the workflow when the reviewer approves the tweet or when the iteration count reaches five.

The reviewer uses structured output defined by `TweetEvaluation`, with:

- `evaluation`: `approved` or `rejected`
- `feedback`: actionable review feedback

## Logging

Logging is configured centrally in `app/logging/logger.py` with Loguru.

### Console

INFO and higher messages are printed to the terminal with timestamps, log levels, module names, function names, and line numbers.

### Files

- `logs/app_info.log`: INFO and WARNING records, including workflow stages, approvals, rejected reviews, maximum-iteration stops, health checks, and OpenRouter rate-limit events
- `logs/app_error.log`: ERROR records and full exception tracebacks for unexpected failures

Log files rotate at 10 MB, are retained for seven days, and are compressed after rotation.

The application avoids logging the API key. Topics are currently included in request logs to help diagnose generation requests, so treat log files as application data.

## Troubleshooting

### `npm` is not recognized

The Python virtual environment does not install or activate Node.js. Install Node.js, restart VS Code or open a new terminal, and verify:

```powershell
node --version
npm --version
```

If Node.js is installed at `C:\Program Files\nodejs` but the current terminal cannot find it, open a fresh terminal or temporarily add it to the current PowerShell session:

```powershell
$env:Path += ';C:\Program Files\nodejs'
```

### Missing `.next` manifest or HTTP 500 from Next.js

A stale or incomplete development build can leave the `.next` directory without required generated manifests. Stop the frontend server and rebuild the generated directory:

```powershell
cd frontend\nextjs
Remove-Item .next -Recurse -Force
npm run dev
```

### OpenRouter `free-models-per-day` rate limit

The configured free models can exhaust the provider's daily quota. The backend records this as a WARNING and returns HTTP `429`. Wait for the quota to reset, add credits to the OpenRouter account, or update the model names in `.env` to models available to your account.

### Frontend shows a generation error

Check both running terminals and inspect:
## Validation

Backend syntax can be checked without calling the LLM:
The frontend can be checked and built with:

```powershell
cd frontend\nextjs
npm run build
```

The file under `app/tests/` is a workflow smoke script that invokes the real LLM workflow. It is not a fully isolated pytest suite and may consume provider quota when executed.

## Security and Repository Hygiene

- Keep `.env` and API keys out of version control.
- Do not commit `.venv`, `node_modules`, `.next`, or Python cache directories.
- Review log files before sharing them because request topics may be included.
- Use provider models and API credits appropriate for production workloads; free-model quotas are intended for limited development use.

