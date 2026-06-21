# PO Follow-up

## Current product goal

Build a working MVP for campaign-based rural/agroecological commerce operations, using Delícias da Roça as the first pilot.

## Current phase

```text
Phase 7.2 — Frontend Admin Operations, Settlement & Payment Reconciliation
```

## Immediate priorities

1. Reflect operations data in admin campaign detail.
2. Reflect pricing and settlement reports.
3. Add payment reconciliation interface.
4. Validate deployment on VPS.
5. Prepare demo flow for Alice.

## Open product questions

- Should Alice edit pickup points from frontend now, or keep them seed-based?
- Should cost price be editable in campaign product UI?
- Should payment confirmation require amount validation against order total?
- Should payment status changes require notes?
- Should campaign closing freeze all financial snapshots?
- Should cancelled orders release campaign reserved stock?

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Frontend/API drift | High | Maintain API contract docs |
| Manual payment mistakes | Medium | Add confirmation dialogs and history |
| Settlement mismatch | High | Validate against Alice spreadsheets |
| Scope drift | Medium | Keep phase docs and task boundaries |
