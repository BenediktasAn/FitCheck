# FitCheck

Well-being app for people who sit at a desk all day. Planned features are mood detection, posture tracking, session tracking and a wellness chatbot.

Right now this is just the project skeleton, nothing is implemented yet.

## Structure

```
FitCheck/
├── mobile/              # Android + iOS app (Expo, React Native, TypeScript)
├── backend/
│   ├── api/             # main API (Node.js, TypeScript, Express)
│   └── ml-service/      # ML stuff (Python, FastAPI, Celery)
└── docker-compose.yml   # Postgres + Redis for local dev
```

Ports:

- API: 3000 (`/health`)
- ML service: 8000 (`/health`, docs at `/docs`)
- Postgres: 5432 (user, password and db are all `fitcheck`)
- Redis: 6379

## What you need installed

- Git
- Node.js 20+ (https://nodejs.org)
- Python 3.11+ (https://www.python.org/downloads)
- Docker Desktop (https://www.docker.com/products/docker-desktop), which has to be running when you use `docker compose`
- Expo Go on your phone (App Store / Google Play)

If you want to use a simulator instead of your phone, you also need Xcode (iOS, Mac only) or Android Studio (Android).

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

Mobile:

```bash
cd mobile
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

Mobile:

```bash
cd mobile
npm start
```

Scan the QR code with Expo Go (on iPhone use the normal camera app). Your phone has to be on the same wifi as your laptop. You can also press `i` for the iOS simulator or `a` for the Android emulator.

Note: from a real phone `localhost` won't reach the backend, you need your laptop's local IP instead (e.g. `http://192.168.1.20:3000`).

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

Mobile: you should see a white screen saying "Open up App.tsx to start working on your app!". If you change that text in `mobile/App.tsx` and save, it should update on the phone straight away.

Type checks:

```bash
cd backend/api && npm run typecheck
cd mobile && npx tsc --noEmit
```

The parts don't talk to each other yet, so for now this only checks that each one runs on its own.

## Stopping

- `Ctrl + C` stops the servers
- `docker compose down` stops Postgres and Redis (data is kept)
- `docker compose down -v` also deletes the database data

## Other commands

- Add a mobile package: `npx expo install <package>` (use this instead of `npm install` so the versions match Expo)
- Add a Python package: put it in `requirements.txt` and run `pip install -r requirements.txt`
- Build the API: `npm run build`, then `npm start` in `backend/api`
