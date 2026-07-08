# Architecture Notes

## Preliminary thinking
Leaning toward LangGraph for orchestration since we want explicit state control — the agent needs to branch between retrieval, order-status API lookup, and escalation.

## Retrieval
- Dense retrieval (embeddings) as primary strategy
- Vector store: pgvector preferred (we already run RDS)

## Known constraints
- Cannot use OpenAI API (PII) — must use self-hosted or in-VPC models
- Embedding model: open source preferred (BGE, E5)
- LLM: self-hosted (Llama 3, Mistral) or Bedrock (keeps data in AWS)

## Open questions we haven't resolved yet
1. Which LLM for generation — Bedrock Claude vs. self-hosted Llama 3?
2. What's the escalation threshold — confidence score, or explicit user request only?
