# Phase 7.2 — Frontend Admin Operations, Settlement & Payment Reconciliation

Backend is already prepared with reference operational data, pricing snapshots, settlement reports, financial summary, order matrix, financial adjustments, payment reconciliation, payment summary and CSV exports.

Frontend target page:

```text
/admin/campaigns/:campaignId
```

Required frontend tabs:

```text
Overview
Operations
Products & Pricing
Orders
Settlement
Payments
```

The frontend should call documented API endpoints and display data safely: no raw null, no Invalid Date, safe currency formatting, safe empty states, loading states and toast feedback.

Out of scope: authentication, permissions, payment proof file upload, automatic Pix/boleto/card gateway integration, WhatsApp automation and backend endpoint changes.
