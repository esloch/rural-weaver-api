# API Contract

Base prefix:

```text
/api
```

## Public

```text
GET /health
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

## Producer

```text
GET /producer/products
PATCH /producer/products/{id}/stock
GET /producer/orders
```
