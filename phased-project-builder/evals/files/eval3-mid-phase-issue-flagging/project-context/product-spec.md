# Customer Support RAG Agent — Product Spec

## Core Capabilities
1. Answer product questions (specs, availability, pricing)
2. Answer policy questions (returns, shipping, warranties)
3. Look up live order status via internal Order Management API
4. Escalate to a human agent when confidence is low or the user asks for a human

## Order Management API (for the order-lookup tool)
- Base URL: `https://orders.internal.company.com/v1`
- Auth: API key, passed as header `X-API-Key: <key>`
- Endpoint: `GET /orders/{order_id}` returns status, carrier, ETA

## Hard Constraints
- No PII may leave our AWS VPC
- Every AI-generated answer must cite its source
- All interactions logged for 90 days for audit purposes
