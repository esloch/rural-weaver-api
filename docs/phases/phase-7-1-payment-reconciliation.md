# Phase 7.1 — Payment Reconciliation Backend

Implemented backend workflow for manual payment reconciliation.

Capabilities: consult payment state for an order, mark proof as received, upsert payment detail, create manual payment confirmation, confirm payment, cancel payment, payment confirmation history, campaign payment summary and payments CSV export.

Validated flow:

```text
pending → proof_received / requires_review → confirmed / confirmed
```

Important implementation note: repositories or scripts that perform ORM writes may need `import apps.api.app.db.base  # noqa: F401` to load all model metadata for foreign key resolution.
