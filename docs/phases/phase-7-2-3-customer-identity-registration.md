# Phase 7.2.3 — Customer Identity Registration for Orders

## Goal

Implement the backend foundation for registered customer identity before real stock reservation.

## Scope in this backend repo

- keep UUID internal IDs for `customers.id` and `orders.id`
- add human-facing `customer_number` and `order_number`
- validate CPF, email, and phone before customer upsert and order creation
- create or update `Customer` before stock reservation when the registered identity payload is used
- preserve existing order snapshot fields for historical order integrity
- keep frontend compatibility during the transition period

## Implemented backend foundation

Customer model updates:

- `tenant_id` nullable for future SaaS tenant scope
- `customer_number`
- `first_name`
- `last_name`
- `cpf_normalized`
- `phone_country_code`
- `phone_area_code`
- `phone_number`
- `phone_e164`

Order model updates:

- `customer_id` link remains in place and is now used by the registered-customer flow
- `order_number`
- structured delivery snapshot support with `state`, `postal_code`, and `country`
- existing snapshots such as `customer_name`, `customer_phone`, `customer_email`, and `address` remain preserved

Validation utilities:

- `normalize_cpf`
- `validate_cpf`
- `normalize_email`
- `normalize_phone`

Current validation behavior:

- reject invalid CPF
- reject repeated-digit CPF values
- reject missing first or last name
- reject missing or invalid email
- reject missing phone country code
- reject missing Brazilian DDD
- reject delivery orders without delivery address

## Compatibility note

Legacy snapshot-only order payloads are still accepted temporarily to avoid breaking the current production frontend before the coordinated frontend rollout. That path is now deprecated for the final registered-customer flow.

## Remaining follow-up

- frontend `/order` rollout for the registered customer payload
- remove the legacy anonymous payload path after rollout
- add normalized `CustomerAddress` if structured address reuse is required
- add tenant-scoped uniqueness when tenant foundation work begins
