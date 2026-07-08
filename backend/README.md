# Backend

Backend service scaffold for the AI-first HCP CRM.

## Planned Responsibilities
- Expose FastAPI endpoints for chat, interaction state, and HCP profile access
- Run LangGraph orchestration
- Integrate Groq for tool selection and extraction tasks
- Persist HCP profiles and interaction history in PostgreSQL

## Package Layout
- `app/api/`: HTTP routes
- `app/core/`: settings and shared infrastructure
- `app/db/`: database session and persistence setup
- `app/graph/`: LangGraph orchestration
- `app/models/`: ORM models
- `app/schemas/`: Pydantic schemas
- `app/services/`: non-tool service logic
- `app/tools/`: tool modules required by the architecture
