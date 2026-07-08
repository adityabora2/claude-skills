# Customer Support RAG Agent — Product Spec

## Overview
Build a RAG-based AI agent for Tier-1 customer support on our e-commerce platform. It should answer questions about orders, returns, shipping, and product info by retrieving relevant context from our knowledge base.

## Scale & Requirements
- Traffic: 5,000 queries/day at launch, scaling to 50,000 within 6 months
- Latency: p95 < 3 seconds
- Availability: 99.9% uptime
- Languages: English only for v1

## Data Sources
- Product catalog: daily CSV export from Shopify (100k+ SKUs)
- Support KB: 2,000+ FAQ articles in Confluence
- Policy docs: internal PDF policy documents (~80 pages)
- Historical resolved tickets: Zendesk export (50k+ tickets, for few-shot examples)

## Core Capabilities
1. Answer product questions (specs, availability, pricing)
2. Answer policy questions (returns, shipping, warranties)
3. Look up live order status via internal Order Management API
4. Escalate to a human agent (create Zendesk ticket) when confidence is low or the user asks for a human

## Hard Constraints
- No PII may leave our AWS VPC — rules out third-party embedding/LLM APIs that process raw customer data outside our infrastructure
- Every AI-generated answer must cite its source
- All interactions logged for 90 days for audit purposes
