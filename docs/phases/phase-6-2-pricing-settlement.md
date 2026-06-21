# Phase 6.2 — Pricing, Cost & Producer Settlement Model

Added financial structure needed to replace spreadsheet-based campaign settlement.

Implemented capabilities: cost price/Preço Revenda, sale price/Preço Venda, campaign product financial snapshots, order item financial snapshots, producer settlement report, campaign financial summary, order matrix, manual financial adjustments, financial CSV exports, payment fee fields, backfill scripts and pricing import script.

Main endpoints include `/financial-summary`, `/producer-settlement`, `/order-matrix`, `/financial-adjustments` and their CSV exports.

Known limitation: if real spreadsheet pricing is not imported, cost totals may show `0.00`, and producer settlement may group rows as `Sem produtor informado`.
