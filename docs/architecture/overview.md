# Backend Architecture Overview

The Rural Weaver API is the source of truth for operational and financial data. It owns campaigns, campaign products, orders, order items, stock reservations, pickup points, delivery zones, payment methods, CSA plans, campaign rules, pricing snapshots, producer settlement, financial summaries, payment reconciliation and CSV exports.

```text
Frontend browser
  ↓
https://tejidorural.com
  ↓
Frontend API calls
  ↓
https://api.tejidorural.com/api
  ↓
FastAPI
  ↓
SQLAlchemy
  ↓
PostgreSQL
```

## Backend layers

```text
Routes → Schemas → Repositories → Models → Database
```

## Snapshot principle

Financial reports must use snapshots saved at the moment of sale, not only current product data. Important fields include producer, cost price, sale price, margin, unit values and totals.
