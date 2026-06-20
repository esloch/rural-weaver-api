# Phase 6.1 schema fields patch

This patch exposes the operational fields introduced in Phase 6.1 to the frontend.

## Updated responses

CampaignProductRead adds:

- producer_name_snapshot
- offer_type
- display_order
- min_quantity
- max_quantity
- requires_confirmation

SalesCampaignDetailRead adds:

- rule

ProductRead adds:

- producer_name_snapshot
- offer_type
- is_refrigerated
- is_frozen
- is_addon
- is_donation

BasketTypeRead adds:

- average_items
- average_weight_kg
- serves_people

OrderRead adds:

- customer_id
- pickup_point_id
- delivery_zone_id
- payment_method_id
- source
- confirmation_status
- submitted_at
- confirmed_at
- delivery_fee
- created_at
- updated_at

Frontend should map snake_case to camelCase in its API adapter.
