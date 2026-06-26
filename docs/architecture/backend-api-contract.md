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

## Public order endpoint

```text
POST /orders
```

Phase 7.2.3 backend foundation adds registered customer identity support to public order creation.

Request direction:

```text
customer or top-level fields
- first_name / firstName
- last_name / lastName
- cpf
- email
- phone_country_code / phoneCountryCode
- phone_area_code / phoneAreaCode
- phone_number / phoneNumber

delivery_address or deliveryAddress for delivery orders
- address_line / addressLine
- address_number / addressNumber
- address_complement / addressComplement
- neighborhood
- city
- state
- postal_code / postalCode
- country
```

Response direction:

```text
- id
- order_number
- customer_id
- customer_name
- customer_phone
- customer_email
- total
- status
- payment_status
- created_at
```

Validation direction:

- invalid CPF returns validation error
- missing first name returns validation error
- missing last name returns validation error
- missing email returns validation error
- invalid email returns validation error
- missing phone country code returns validation error
- missing DDD for Brazil returns validation error
- delivery without address returns validation error

Compatibility note:

Legacy snapshot-only order payloads remain temporarily accepted while the frontend transitions to the registered-customer flow. They are now deprecated for real stock-reserving production use.

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
