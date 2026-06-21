# AGENTS.md — Rural Weaver API

## Purpose

This repository contains the FastAPI backend for Rural Weaver / Tejido Rural. The backend owns the business rules, database schema, campaign workflow, orders, stock, pricing, producer settlement, financial summaries, payment reconciliation, operational scripts, API contracts and backend deployment documentation for the Delícias da Roça pilot.

## Production API

```text
https://api.tejidorural.com/api
```

## Main stack

```text
FastAPI
SQLAlchemy
Pydantic
Alembic
PostgreSQL
Docker Compose
Nginx / HTTPS
```

## Repository architecture

```text
apps/api/app/models/          SQLAlchemy models
apps/api/app/schemas/         Pydantic request/response schemas
apps/api/app/repositories/    data access and business logic
apps/api/app/api/routes/      FastAPI route modules
apps/api/app/api/router.py    route registration
apps/api/app/scripts/         seed, import and backfill scripts
migrations/versions/          Alembic migrations
docs/                         project documentation
```

## Core rules for agents

Do not place substantial business logic directly inside route functions. Routes should validate and route requests, while repositories should handle data access and business logic.

Any SQLAlchemy model change must include an Alembic migration. For non-null columns added to existing tables, use safe defaults or phased migrations. Never remove or rewrite migrations that may already have been applied to production.

Do not invent endpoints without updating `docs/architecture/backend-api-contract.md`.

Never commit `.env`, credentials, tokens, private keys, database dumps, customer private exports, production secrets or temporary zip patches.

When scripts or repositories touch models with foreign keys, ensure SQLAlchemy metadata is fully loaded. Importing `apps.api.app.db.base` can be necessary in standalone scripts or repositories.

## Validation

```bash
docker compose up -d --build
docker compose exec api alembic current
docker compose exec api alembic upgrade head
docker compose exec api pytest
docker compose logs api --tail=100
```

## Documentation rules

Every phase-level change must update or create a document under `docs/phases/`. Architecture changes must update `docs/architecture/`. Operational changes must update `docs/operations/`. Planning/product changes must update `docs/planning/`.

## Commit style

Use semantic commits: `feat(scope):`, `fix(scope):`, `docs(scope):`, `chore(scope):`, `refactor(scope):`, `test(scope):`.

## Current phase focus

```text
Phase 7.2 — Frontend Admin Operations, Settlement & Payment Reconciliation
```

Backend Phase 7.1 is already implemented and validated. Avoid changing backend contracts unless the frontend integration reveals a real issue.
