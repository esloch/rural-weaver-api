# Decision Log

| Date | Area | Decision | Reason | Consequence |
|---|---|---|---|---|
| 2026-06-20 | Payments | Payment reconciliation is manual in MVP | Alice receives proof outside the platform | No payment gateway integration yet |
| 2026-06-20 | Architecture | Frontend and backend are deployed separately | Lovable/Vite frontend and FastAPI API evolve independently | Requires CORS and production API URL configuration |
| 2026-06-20 | Finance | Store financial snapshots on order items | Prices can change after orders | Historical reports stay stable |
