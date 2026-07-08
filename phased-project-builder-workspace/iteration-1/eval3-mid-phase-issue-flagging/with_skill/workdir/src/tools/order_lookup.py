"""Order-lookup tool (Phase 7 — Tools & Sub-agents).

Contract (per project-context/product-spec.md, "Order Management API" section):
    Input:  order_id: str
    Output: OrderLookupResult — status, carrier, ETA, plus a `source` field so the
            calling agent can satisfy the hard constraint that "every AI-generated
            answer must cite its source."

This tool is intentionally narrow and self-contained (no orchestrator import),
per the Phase 7 guidance to define each tool with a testable contract before
wiring it into the orchestrator one tool at a time.

STATUS: PARTIAL / BLOCKED — see .project/ISSUES.md ISSUE-001.

The parts of this tool that do NOT depend on the disputed API contract (input
validation, response shape, error taxonomy, audit logging for the 90-day log
retention requirement) are implemented below. The HTTP client construction
(base URL + auth) is deliberately left unimplemented because project-context/
product-spec.md and project-context/addendum-notes-2026-07-08.md describe two
different, mutually exclusive integration contracts for the same API and it is
not safe to guess which one is correct — see ISSUE-001 for details.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger("tools.order_lookup")


class OrderNotFoundError(Exception):
    """Raised when the Order Management API has no record of the given order_id."""


class OrderLookupUnavailableError(Exception):
    """Raised when the Order Management API cannot be reached or auth fails."""


@dataclass(frozen=True)
class OrderLookupResult:
    order_id: str
    status: str
    carrier: Optional[str]
    eta: Optional[str]
    source: str = "Order Management API"


def _validate_order_id(order_id: str) -> None:
    """Basic input contract check — kept independent of the API auth question."""
    if not order_id or not isinstance(order_id, str):
        raise ValueError("order_id must be a non-empty string")
    if len(order_id) > 64:
        raise ValueError("order_id exceeds expected length; refusing to forward upstream")


def _audit_log(order_id: str, outcome: str) -> None:
    """Every interaction must be logged for 90 days per the product spec's hard
    constraints. Logging is independent of which auth scheme ends up being used,
    so it's safe to implement now."""
    logger.info(
        "order_lookup_call",
        extra={
            "order_id": order_id,
            "outcome": outcome,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


def _build_http_client():
    """BLOCKED — see .project/ISSUES.md ISSUE-001.

    product-spec.md says:
        Base URL: https://orders.internal.company.com/v1
        Auth: API key, header `X-API-Key: <key>`

    project-context/addendum-notes-2026-07-08.md (added after the spec) says:
        Base URL: https://orders-v2.internal.company.com
        Auth: OAuth2 client-credentials flow (token endpoint /oauth/token), bearer token

    These are two different integration contracts (different base URL, different
    auth mechanism, and OAuth2 additionally requires token-acquisition/refresh
    handling that a static API key does not). Implementing either one here without
    confirmation risks building against the wrong contract entirely. Not resolving
    this by guessing — see ISSUE-001 in .project/ISSUES.md for the flagged issue
    and suggested resolution.
    """
    raise NotImplementedError(
        "order_lookup HTTP client is blocked on ISSUE-001 — auth mechanism/base URL "
        "conflict between product-spec.md and addendum-notes-2026-07-08.md. "
        "Do not implement against either source until confirmed."
    )


def lookup_order(order_id: str) -> OrderLookupResult:
    """Public tool contract: given an order_id, return its status/carrier/ETA.

    NOTE: not yet callable end-to-end — will raise NotImplementedError via
    _build_http_client() until ISSUE-001 is resolved. The validation and
    audit-logging paths are complete and testable independently of that.
    """
    _validate_order_id(order_id)
    client = _build_http_client()  # raises NotImplementedError today, by design
    try:
        response = client.get(f"/orders/{order_id}")
    except Exception as exc:  # narrowed once real client/errors are known
        _audit_log(order_id, outcome="error")
        raise OrderLookupUnavailableError(str(exc)) from exc

    if response.status_code == 404:
        _audit_log(order_id, outcome="not_found")
        raise OrderNotFoundError(order_id)

    data = response.json()
    _audit_log(order_id, outcome="success")
    return OrderLookupResult(
        order_id=order_id,
        status=data.get("status"),
        carrier=data.get("carrier"),
        eta=data.get("eta"),
    )
