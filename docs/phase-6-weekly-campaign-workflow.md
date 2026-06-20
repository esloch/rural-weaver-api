# Phase 6 — Weekly Campaign Workflow

This phase aligns the platform with Alice's real weekly operation.

## Adds

- `sales_campaigns`
- `campaign_products`
- `pickup_points`
- `delivery_zones`
- campaign-based orders
- campaign labels CSV
- campaign picking list CSV

## Main workflow

```text
Weekly campaign
  -> available products
  -> customer orders
  -> reserved quantities
  -> labels
  -> picking list
  -> payment reconciliation
```

## Public API

```text
GET /api/campaigns/active
GET /api/campaigns/{id}
POST /api/orders
```

## Admin API

```text
GET /api/admin/campaigns
POST /api/admin/campaigns
PATCH /api/admin/campaigns/{id}
GET /api/admin/campaigns/{id}
GET /api/admin/campaigns/{id}/orders
GET /api/admin/campaigns/{id}/products
POST /api/admin/campaigns/{id}/products
PATCH /api/admin/campaign-products/{id}
GET /api/admin/campaigns/{id}/labels
GET /api/admin/campaigns/{id}/picking-list
```
