# Backend API Contract

## Base URL

```text
https://api.tejidorural.com/api
```

## Public campaign endpoints

```text
GET /campaigns/active
GET /campaigns/{campaign_id}
```

## Reference endpoints

```text
GET /reference/pickup-points
GET /reference/delivery-zones
GET /reference/payment-methods
GET /reference/subscription-plans
```

Expected seeded counts: pickup-points 6, delivery-zones 4, payment-methods 4, subscription-plans 6.

## Admin campaign endpoints

```text
GET   /admin/campaigns
POST  /admin/campaigns
GET   /admin/campaigns/{campaign_id}
PATCH /admin/campaigns/{campaign_id}
GET   /admin/campaigns/{campaign_id}/orders
GET   /admin/campaigns/{campaign_id}/products
POST  /admin/campaigns/{campaign_id}/products
PATCH /admin/campaign-products/{campaign_product_id}
GET   /admin/campaigns/{campaign_id}/labels
GET   /admin/campaigns/{campaign_id}/picking-list
```

## Admin settlement endpoints

```text
GET    /admin/campaigns/{campaign_id}/financial-summary
GET    /admin/campaigns/{campaign_id}/producer-settlement
GET    /admin/campaigns/{campaign_id}/order-matrix
GET    /admin/campaigns/{campaign_id}/financial-adjustments
POST   /admin/campaigns/{campaign_id}/financial-adjustments
DELETE /admin/financial-adjustments/{adjustment_id}
GET    /admin/campaigns/{campaign_id}/producer-settlement.csv
GET    /admin/campaigns/{campaign_id}/financial-summary.csv
GET    /admin/campaigns/{campaign_id}/order-matrix.csv
```

## Admin payment reconciliation endpoints

```text
GET   /admin/orders/{order_id}/payment-reconciliation
GET   /admin/orders/{order_id}/payment-confirmations
POST  /admin/orders/{order_id}/payment-confirmations
GET   /admin/orders/{order_id}/payment-detail
PUT   /admin/orders/{order_id}/payment-detail
PATCH /admin/orders/{order_id}/payment-status
POST  /admin/orders/{order_id}/mark-proof-received
POST  /admin/orders/{order_id}/confirm-payment
POST  /admin/orders/{order_id}/cancel-payment
GET   /admin/campaigns/{campaign_id}/payment-summary
GET   /admin/campaigns/{campaign_id}/payments.csv
```

Payment statuses: `pending`, `proof_received`, `confirmed`, `cancelled`, `refunded`.

Confirmation statuses: `pending`, `requires_review`, `confirmed`, `cancelled`.

## Curl validation

```bash
CAMPAIGN_ID=d5528e5d-f9d4-4424-9a32-b69cb3473e87
curl -s https://api.tejidorural.com/api/campaigns/active | jq
curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/payment-summary | jq
curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/financial-summary | jq
```
