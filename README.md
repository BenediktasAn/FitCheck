# FitCheck

Well-being web app for people who sit at a desk all day. Planned features are manual mood check-ins, slouch detection with a USB distance sensor (Arduino), session tracking with break reminders, a wellness chatbot and gamification.

Right now this is just the project skeleton, nothing is implemented yet.

## Structure

```
FitCheck/
├── web/                 # web app (React, TypeScript, Vite)
├── backend/
│   ├── api/             # main API (Node.js, TypeScript, Express)
│   └── ml-service/      # ML stuff (Python, FastAPI, Celery)
└── docker-compose.yml   # Postgres + Redis for local dev
```

Ports:

- Web app: 5173
- API: 3000 (`/health`)
- ML service: 8000 (`/health`, docs at `/docs`)
- Postgres: 5432 (user, password and db are all `fitcheck`)
- Redis: 6379

## What you need installed

- Git
- Node.js 20+ (https://nodejs.org)
- Python 3.11+ (https://www.python.org/downloads)
- Docker Desktop (https://www.docker.com/products/docker-desktop), which has to be running when you use `docker compose`
- Chrome or Edge on desktop. The sensor features use the Web Serial API, which only works there

## Setup

You only need to do this once after cloning.

```bash
git clone <repo-url>
cd FitCheck
```

Start Postgres and Redis:

```bash
docker compose up -d
```

API:

```bash
cd backend/api
npm install
cp .env.example .env
```

ML service (Mac/Linux):

```bash
cd backend/ml-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

ML service (Windows, PowerShell):

```powershell
cd backend\ml-service
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Everyone makes their own `.venv`, it's not in git.

Web app:

```bash
cd web
npm install
```

## Running it

Open a separate terminal for each of these.

Postgres + Redis (from the repo root):

```bash
docker compose up -d
```

API:

```bash
cd backend/api
npm run dev
```

ML service:

```bash
cd backend/ml-service
source .venv/bin/activate    # Windows: .venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Celery worker (not needed yet, there are no tasks):

```bash
cd backend/ml-service
source .venv/bin/activate
celery -A app.worker worker --loglevel=info    # on Windows add --pool=solo
```

Web app:

```bash
cd web
npm run dev
```

Then open http://localhost:5173 in Chrome or Edge.

## Checking it works

Postgres and Redis:

```bash
docker compose ps
docker compose exec postgres psql -U fitcheck -c "select 1;"
docker compose exec redis redis-cli ping    # prints PONG
```

API: go to http://localhost:3000/health, you should get `{"status":"ok","service":"api"}`

ML service: go to http://localhost:8000/health, you should get `{"status":"ok","service":"ml-service"}`. http://localhost:8000/docs also lets you try the endpoints in the browser.

Celery: the log should say `Connected to redis://localhost:6379/0` and then `ready`.

Web app: http://localhost:5173 should show "FitCheck". If you change the text in `web/src/App.tsx` and save, the page updates straight away.

Type checks:

```bash
cd backend/api && npm run typecheck
cd web && npx tsc -b
```

The parts don't talk to each other yet, so for now this only checks that each one runs on its own.

## Stopping

- `Ctrl + C` stops the servers
- `docker compose down` stops Postgres and Redis (data is kept)
- `docker compose down -v` also deletes the database data

## Other commands

- Lint the web app: `npm run lint` in `web`
- Add a Python package: put it in `requirements.txt` and run `pip install -r requirements.txt`
- Build the API: `npm run build`, then `npm start` in `backend/api`
- Build the web app: `npm run build` in `web` (output goes to `web/dist`), `npm run preview` to try the build
