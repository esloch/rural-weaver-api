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

`POST /orders` now supports a Phase 7.2.3 customer identity payload for registered order creation.

Implemented backend direction:

- internal IDs stay UUID-based
- `orders.order_number` is the human-facing order reference
- `orders.customer_id` links to `customers.id`
- customer identity can be sent with either camelCase or snake_case keys
- legacy snapshot-only payloads remain temporarily accepted for backward compatibility until the frontend rollout is coordinated

Supported identity fields for the registered flow:

```text
customer / top-level
- first_name / firstName
- last_name / lastName
- cpf
- email
- phone_country_code / phoneCountryCode
- phone_area_code / phoneAreaCode
- phone_number / phoneNumber

delivery_address / deliveryAddress when delivery
- address_line / addressLine
- address_number / addressNumber
- address_complement / addressComplement
- neighborhood
- city
- state
- postal_code / postalCode
- country
```

Registered-order validation now rejects invalid CPF, invalid email, missing phone country code, missing DDD for Brazil, and missing delivery address for delivery orders. Successful order creation returns `order_number` and `customer_id` in addition to the existing order snapshot fields.

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
