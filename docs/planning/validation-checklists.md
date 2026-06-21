# Validation Checklists

## Backend health

```bash
curl -s https://api.tejidorural.com/api/campaigns/active | jq
curl -s https://api.tejidorural.com/api/reference/pickup-points | jq 'length'
```

## Campaign validation

```bash
CAMPAIGN_ID=d5528e5d-f9d4-4424-9a32-b69cb3473e87
curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/payment-summary | jq
curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/financial-summary | jq
curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/producer-settlement | jq
curl -s https://api.tejidorural.com/api/admin/campaigns/$CAMPAIGN_ID/order-matrix | jq
```
