# API Contract

Base prefix:

```text
/api
```

## Public

```text
GET /health
HEAD /health
GET /products
GET /payment-settings/active
POST /orders
```

## Admin

```text
GET /admin/dashboard
GET /admin/products
POST /admin/products
PATCH /admin/products/{id}
PATCH /admin/products/{id}/stock
GET /admin/orders
PATCH /admin/orders/{id}
GET /admin/orders/export.csv
GET /admin/payment-settings
PATCH /admin/payment-settings
```

Admin product create and update now accept either camelCase or snake_case payload keys. Blank `image_url` values are normalized to `null`. When `producer_id` is omitted, the MVP uses the first active producer until admin RBAC and producer assignment are expanded.

## Producer

```text
GET /producer/products
PATCH /producer/products/{id}/stock
GET /producer/orders
```
