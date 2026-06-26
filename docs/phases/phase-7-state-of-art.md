# Phase 7.x Backend — State of Art

## Scope

This document summarizes the current backend state of art for Phase 7.x work completed so far in the Rural Weaver / Tejido Rural API.

It is the concise backend reference for:

- production API context
- Phase 7.1 payment reconciliation backend
- Phase 7.2 backend support for frontend admin operations
- Phase 7.2.3 customer identity registration foundation
- admin product create/update backend contract
- known backend gaps
- recommended next backend tasks

## Production API context

- Direct backend API domain: `https://api.ruralweaver.com`
- Real backend API base: `https://api.ruralweaver.com/api`
- Browser frontend traffic in production goes through the same-origin `/api` proxy on the frontend domain.
- Admin API routes are protected by temporary Nginx Basic Auth in production.
- App-level authentication and authorization are still future work.

## Phase 7.1 — Payment Reconciliation Backend

Phase 7.1 implemented backend payment reconciliation.

Implemented endpoints and capabilities:

- order payment reconciliation
- order payment confirmations
- payment detail upsert
- mark proof received
- confirm payment
- cancel payment
- campaign payment summary
- payments CSV export

Implemented state handling:

- payment status transitions
- confirmation status transitions

Operationally relevant statuses:

- payment status:
  - `pending`
  - `proof_received`
  - `confirmed`
  - `cancelled`
  - `refunded` where applicable
- confirmation status:
  - `pending`
  - `requires_review`
  - `confirmed`

Validation:

- endpoint-level validation was performed
- pending → `proof_received` → `confirmed` workflow was tested
- campaign payment summary updated correctly after confirmation

## Phase 7.2 — Backend Support for Frontend Admin

Phase 7.2 backend support provides the data and write paths required by the frontend admin for phases 6, 6.1, 6.2, and 7.1.

Backend support currently includes:

- campaign details
- campaign products
- campaign orders
- reference data
- settlement/acerto
- payment summary
- CSV exports
- admin product list
- admin product create/update

This backend support underpins frontend pages such as:

- `/admin`
- `/admin/campaigns`
- `/admin/products`
- `/admin/orders`
- `/admin/inventory`
- `/admin/payment-settings`
- `/admin/campaigns/:campaignId`

## Phase 7.2.3 — Customer Identity Registration Foundation

Relevant backend goal:

- create or update a registered customer before real stock reservation
- keep UUID internal primary keys
- add human-facing `customer_number` and `order_number`
- preserve order snapshot fields for historical support and fulfillment context

Implemented backend foundation:

- extended `customers` with `customer_number`, `first_name`, `last_name`, `cpf_normalized`, normalized phone fields, and nullable `tenant_id`
- extended `orders` with `order_number` and structured delivery snapshot fields `state`, `postal_code`, and `country`
- added CPF, email, and phone normalization/validation helpers
- added customer upsert before order creation when the registered identity payload is used
- linked created orders to `customer_id`
- generated human-facing `CLI-000001` / `PED-000001` style references through database sequences
- kept legacy snapshot-only order payloads temporarily accepted for compatibility until the frontend rollout is coordinated

Behavior notes:

- registered customer validation runs before stock reservation
- invalid CPF, missing name parts, invalid email, missing phone country code, missing Brazilian DDD, and missing delivery address for delivery orders now return validation errors
- public responses expose `order_number` and `customer_id` but do not expose CPF
- `customer_name`, `customer_phone`, `customer_email`, and address snapshots remain on orders

Validation run for this backend task:

- host `python3 -m compileall apps tests` passed after sandbox escalation
- container `docker compose exec api python -m compileall apps tests` compiled the application code and reported that `tests/` is not mounted in the container image
- container `docker compose exec api pytest` ran in the container image but collected `0` tests because the image does not include the repo `tests/` directory
- container `docker compose exec api alembic upgrade head` succeeded
- OpenAPI inspection was performed against the container runtime for `/api/orders` schema changes

## Admin Product Create/Update

Relevant backend commit:

- `37b37c0 feat(admin): add product create and update endpoints`

Root cause:

- frontend already had create/edit product UI
- backend lacked `POST /api/admin/products`
- backend lacked `PATCH /api/admin/products/{product_id}`
- create/edit therefore returned `405 Method Not Allowed`

Implemented routes:

- `POST /api/admin/products`
- `PATCH /api/admin/products/{product_id}`

Existing related routes:

- `GET /api/admin/products`
- `PATCH /api/admin/products/{product_id}/stock`
- `GET /api/producer/products`
- `PATCH /api/producer/products/{product_id}/stock`

Implementation notes:

- accept camelCase and snake_case payloads
- normalize blank `image_url` to `null`
- default missing `producer_id` to the first active producer for the MVP
- preserve stock movement history on edit by applying stock deltas through the stock repository
- allow category as a free-form string
- allow products with empty or missing category to be updated

## Known Backend Gaps

- `/api/admin/orders` does not implement query filtering for `status` or `payment_status`
- frontend currently filters admin orders locally
- backend query filtering can be added later if dataset size or CSV parity requires it
- backend test environment should include `pytest` or a documented test runner setup
- real producer, cost, sale, and margin import/backfill remains needed
- duplicate campaign product prevention should eventually be enforced backend-side with uniqueness validation
- legacy anonymous order payload support should be removed once the frontend customer identity rollout is complete
- app-level authentication and authorization remain future work
- normalized `CustomerAddress` is still follow-up work

## Next Recommended Backend Tasks

1. Coordinate the frontend rollout for the registered customer payload.
2. Add a normalized `CustomerAddress` table if structured customer-address reuse is needed.
3. Add backend filter support for admin orders only if needed.
4. Add duplicate campaign product validation.
5. Improve real pricing and producer import/backfill.
6. Expand order/customer integration tests with a database-backed test environment.
7. Add campaign closing workflow endpoints later.

## Related Documents

- `docs/phases/phase-7-2-3-customer-identity-registration.md`
- `docs/phases/phase-7-1-payment-reconciliation.md`
- `docs/phases/phase-7-2-frontend-admin-ops-settlement-payments.md`
- `docs/api-contract.md`
- `docs/planning/roadmap.md`
