# Phase 6.1 — Alice Operational Data Model

Modeled real Delícias da Roça operational data.

Implemented entities: customers, subscription plans, subscriptions, payment methods, order payment details, payment confirmations, campaign rules, pickup points, delivery zones, expanded product flags, expanded campaign product fields and expanded order fields.

Reference endpoints live under `/api/reference`.

Seed command:

```bash
docker compose exec api python -m apps.api.app.scripts.seed_alice_operational_data
```
