# ai-first-hcp-crm

AI-first Healthcare Professional CRM MVP centered on a split-screen Log Interaction experience.

## Planned Stack
- Frontend: React, TypeScript, Redux Toolkit
- Backend: FastAPI, LangGraph, Groq, Pydantic
- Database: PostgreSQL
- Orchestration: Docker Compose for local database services

## Repository Structure
```text
backend/
  app/
    api/
    core/
    db/
    graph/
    models/
    schemas/
    services/
    tools/
  tests/
frontend/
  public/
  src/
    app/
    components/
    features/
      chat/
      interaction-form/
    store/
    styles/
```

## Setup Status
This is the initial scaffold only. Business logic, API routes, LangGraph flows, database models, and UI implementation are intentionally not added yet.

## Next Steps
- Wire PostgreSQL through the backend config
- Bootstrap the FastAPI service
- Bootstrap the React application shell
- Add LangGraph orchestration and tool implementations
