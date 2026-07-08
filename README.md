# ai-first-hcp-crm

AI-first Healthcare Professional CRM MVP focused on a controlled `Log Interaction` workflow. The UI is split into a read-only CRM form and an AI chat panel. Users describe the interaction in natural language, the backend LangGraph agent chooses a tool, and validated tool output updates the form state.

## Project Overview
- AI-assisted CRM flow for healthcare rep interactions with HCPs.
- Backend-owned form updates only; manual field editing is disabled.
- Seeded HCP profiles support profile lookup before or during interaction logging.
- Saved interaction records can be persisted to PostgreSQL after AI fills enough useful data.

## Tech Stack
- Frontend: React, TypeScript, Vite, Redux Toolkit, React Redux, Inter font
- Backend: FastAPI, Pydantic, SQLAlchemy, LangGraph, Groq
- Database: PostgreSQL 16
- Local infra: Docker Compose

## Architecture
```text
frontend/
  src/app            Redux store
  src/features       Chat panel and read-only interaction form
  src/components     Tool/compliance/profile UI cards
  src/api            Chat and interaction save clients

backend/
  app/api/routes     health, hcps, chat, interactions
  app/agent          LangGraph state, graph, prompts, tools
  app/models         SQLAlchemy models
  app/repositories   HCP, follow-up, interaction persistence
  app/services       Groq client, agent service, merge logic
  app/db             init + seed data
  tests              backend test suite
```

## LangGraph Tools
- `search_hcp_profile`: finds a seeded HCP and hydrates profile fields.
- `log_interaction`: extracts structured interaction data from natural language.
- `edit_interaction`: applies partial corrections without re-extracting the full record.
- `set_follow_up_action`: extracts follow-up action and date.
- `check_compliance`: flags risky pharma claims and suggests safer wording.

## Environment Variables
Backend in `backend/.env`:
```env
DATABASE_URL=postgresql+psycopg://hcp_crm:hcp_crm@localhost:5433/hcp_crm
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Frontend in `frontend/.env`:
```env
VITE_API_BASE_URL=http://localhost:8000
```

## Setup Instructions
### 1. Run PostgreSQL
```bash
docker compose up -d
```
Postgres is exposed on `localhost:5433`.

### 2. Run Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API base: `http://localhost:8000`

### 3. Run Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend base: `http://localhost:5173`

## Demo Prompts
1. `Show me Dr. Amit Mehta's profile before I log the meeting.`
2. `I met Dr. Amit Mehta today in person. We discussed CardioPlus efficacy and patient adherence. He was positive and I shared a product brochure.`
3. `Actually, change the sentiment to neutral and add that he had concerns about pricing.`
4. `Set a follow-up for next Friday to send clinical study data.`
5. `Check compliance: CardioPlus guarantees complete cure and has no side effects.`

## How To Save Interactions
- Let the assistant populate the read-only form.
- Click `Save interaction` once an HCP and at least one meaningful interaction detail are present.
- The frontend calls `POST /api/interactions` and persists the current AI-filled form to PostgreSQL.

## Screenshots
- `[Placeholder] Main split-screen CRM view`
- `[Placeholder] Compliance review state`
- `[Placeholder] Saved interaction confirmation`

## Demo Video
- `[Placeholder] Add Loom or YouTube walkthrough link here`

## Known Limitations
- Conversation memory is not persisted by `session_id`; each request relies on the submitted `current_interaction`.
- UI E2E browser automation is not set up.
- `samples_shared` exists in the form model, but extraction coverage is lighter than the main interaction fields.
- Startup uses lightweight schema patching in `init_db` rather than formal migrations.
