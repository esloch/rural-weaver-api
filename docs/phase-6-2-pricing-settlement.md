# Phase 6.2 — Pricing, Cost & Producer Settlement Model

This phase adds the spreadsheet financial layer to the backend.

## Main purpose

Alice's spreadsheet uses both:

- Preço Revenda
- Preço Venda

The system previously had only one price field, which represented customer sale price. Phase 6.2 adds cost/sale/margin snapshots so the platform can calculate producer settlements and campaign financial summaries.

## New/updated data model

### products

- cost_price
- sale_price

The existing `price` field remains for backwards compatibility and should mirror `sale_price`.

### campaign_products

- cost_price_snapshot
- sale_price_snapshot
- margin_unit_snapshot

The existing `price` field remains for backwards compatibility and should mirror `sale_price_snapshot`.

### order_items

- unit_cost_snapshot
- unit_sale_price_snapshot
- cost_total_snapshot
- sale_total_snapshot
- margin_total_snapshot

### orders

- neighborhood
- city
- complement
- delivery_agent
- payment_fee_amount
- net_total_after_fees

### payment_methods

- fee_fixed
- fee_percent

### campaign_financial_adjustments

Manual financial adjustments by campaign:

- payment_fee
- delivery_cost
- admin_share
- donation_cost
- extra_item
- manual_discount
- other

## New API endpoints

```text
GET    /api/admin/campaigns/{campaign_id}/financial-summary
GET    /api/admin/campaigns/{campaign_id}/producer-settlement
GET    /api/admin/campaigns/{campaign_id}/order-matrix
GET    /api/admin/campaigns/{campaign_id}/financial-adjustments
POST   /api/admin/campaigns/{campaign_id}/financial-adjustments
DELETE /api/admin/financial-adjustments/{adjustment_id}
GET    /api/admin/campaigns/{campaign_id}/producer-settlement.csv
GET    /api/admin/campaigns/{campaign_id}/financial-summary.csv
GET    /api/admin/campaigns/{campaign_id}/order-matrix.csv
```

## Scripts

```bash
python -m apps.api.app.scripts.seed_phase6_2_payment_fees
python -m apps.api.app.scripts.import_alice_pricing_from_xlsx /path/to/TABELA.xlsx --campaign-id <campaign-id>
python -m apps.api.app.scripts.backfill_financial_snapshots
```

## Migration note

Generate the migration from the live model state:

```bash
docker compose exec api alembic revision --autogenerate -m "add pricing settlement model"
docker compose exec api alembic upgrade head
```

Most new columns added to existing tables are nullable to avoid NOT NULL failures on existing records.
