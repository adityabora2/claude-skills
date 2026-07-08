## ISSUE-1 — Order Management API integration conflict (product-spec.md vs. addendum)

- **Date flagged**: 2026-07-07
- **Phase**: 7 (Tools & Sub-agents)
- **Status**: Open — blocking
- **Summary**: `product-spec.md` says the order-lookup tool should hit `https://orders.internal.company.com/v1` `GET /orders/{order_id}` with API-key auth (`X-API-Key` header). `addendum-notes-2026-07-08.md` (platform team) says the Order Management API migrated to OAuth2 client-credentials auth at a new base URL `https://orders-v2.internal.company.com` (token endpoint `/oauth/token`, bearer token on requests), with the old API-key path being sunset. These are mutually exclusive integration details — different base URL, different auth mechanism, different credentials/config, different token-refresh handling.
- **Impact**: Blocks implementing the order-lookup tool until resolved. Also affects secrets/config setup and possibly the "no PII leaves the VPC" constraint depending on where token exchange happens.
- **Resolution**: Awaiting user clarification on which integration spec is authoritative.

