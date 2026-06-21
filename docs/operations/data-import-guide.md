# Data Import Guide

Scripts used to seed and backfill operational and financial data:

```bash
docker compose exec api python -m apps.api.app.scripts.seed_campaigns
docker compose exec api python -m apps.api.app.scripts.seed_alice_operational_data
docker compose exec api python -m apps.api.app.scripts.seed_phase6_2_payment_fees
docker compose exec api python -m apps.api.app.scripts.backfill_financial_snapshots
```

Import Alice pricing from XLSX:

```bash
docker cp "TABELA DE VALORES 16-06-2026.xlsx" rural-weaver-api-api-1:/tmp/tabela.xlsx

docker compose exec api python -m apps.api.app.scripts.import_alice_pricing_from_xlsx   /tmp/tabela.xlsx   --campaign-id d5528e5d-f9d4-4424-9a32-b69cb3473e87
```

After import:

```bash
docker compose exec api python -m apps.api.app.scripts.backfill_financial_snapshots
```
