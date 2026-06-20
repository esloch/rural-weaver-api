# Phase 6.1 — Alice Operational Data Model

This phase aligns the backend with the real Delícias da Roça operation.

## Adds

- customers
- subscription_plans
- subscriptions
- payment_methods
- order_payment_details
- payment_confirmations
- campaign_rules

## Extends

- pickup_points with city, time window, refrigeration and condo-only flags
- delivery_zones with city, area and restrictions
- products with offer_type, refrigerated/frozen/addon/donation flags
- campaign_products with offer_type and campaign-specific ordering/limits
- orders with customer, delivery zone, pickup point, payment method, source and confirmation status

## Seed

Run after migration:

```bash
docker compose exec api python -m apps.api.app.scripts.seed_alice_operational_data
```

## New public reference endpoints

```text
GET /api/reference/pickup-points
GET /api/reference/delivery-zones
GET /api/reference/payment-methods
GET /api/reference/subscription-plans
```

## Offer types

```text
csa_basket
hortifruti
grocery
weekly_offer
collective_purchase
donation
hygiene_cleaning
plants
```
