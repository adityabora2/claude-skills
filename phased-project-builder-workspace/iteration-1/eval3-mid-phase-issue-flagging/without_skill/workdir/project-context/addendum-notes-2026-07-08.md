# Addendum — Platform Team Update (2026-07-08)

Quick note from the platform team, relevant to whoever builds the order-lookup integration:

The Order Management API finished its migration to OAuth2 client-credentials auth last week. The old API-key auth path is being sunset. New details:

- Base URL: `https://orders-v2.internal.company.com`
- Auth: OAuth2 client-credentials flow (token endpoint `/oauth/token`), bearer token on requests
- Endpoint shape is mostly the same: `GET /orders/{order_id}`

Not sure if this made it into the original product spec doc — flagging here so it's not missed.
