# Phase 7.1 — Payment Reconciliation Backend

This phase adds the backend workflow for manual payment reconciliation.

## Goal

Allow Alice/admin to track payment proof, confirm payments, cancel payments and generate campaign-level payment summaries.

## Supported statuses

`orders.payment_status`:

- pending
- proof_received
- confirmed
- cancelled
- refunded

`orders.confirmation_status`:

- pending
- requires_review
- confirmed
- cancelled

## New API endpoints

```text
GET   /api/admin/orders/{order_id}/payment-reconciliation
GET   /api/admin/orders/{order_id}/payment-confirmations
POST  /api/admin/orders/{order_id}/payment-confirmations

GET   /api/admin/orders/{order_id}/payment-detail
PUT   /api/admin/orders/{order_id}/payment-detail

PATCH /api/admin/orders/{order_id}/payment-status
POST  /api/admin/orders/{order_id}/mark-proof-received
POST  /api/admin/orders/{order_id}/confirm-payment
POST  /api/admin/orders/{order_id}/cancel-payment

GET   /api/admin/campaigns/{campaign_id}/payment-summary
GET   /api/admin/campaigns/{campaign_id}/payments.csv
```

## Example curl

```bash
ORDER_ID=<order-id>
CAMPAIGN_ID=<campaign-id>

curl -s https://api.tejidorural.com/api/admin/orders/$ORDER_ID/payment-reconciliation | jq

curl -s -X PUT https://api.tejidorural.com/api/admin/orders/$ORDER_ID/payment-detail \
  -H 'Content-Type: application/json' \
  -d '{
    "methodCode": "pix",
    "proofReceived": true,
    "notes": "Comprovante recebido por WhatsApp"
  }' | jq

curl -s -X POST https://api.tejidorural.com/api/admin/orders/$ORDER_ID/payment-confirmations \
  -H 'Content-Type: application/json' \
  -d '{
    "methodCode": "pix",
    "status": "confirmed",
    "amount": "44.50",
    "proofReceived": true,
    "notes": "Pagamento confirmado manualmente"
  }' | jq

curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/payment-summary | jq
```

## Frontend notes

The admin campaign detail page should add a Payments tab with:

- payment summary cards
- list of orders by payment status
- quick actions:
  - mark proof received
  - confirm payment
  - cancel payment
- payment history modal
- payment detail form for boleto/card link data
