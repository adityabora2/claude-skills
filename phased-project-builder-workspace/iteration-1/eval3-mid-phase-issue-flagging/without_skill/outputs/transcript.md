# Transcript — Phase 7 (Tools & Sub-agents): order-lookup tool

## Task
User: "Let's move on to Phase 7 (Tools & Sub-agents) -- start with the order-lookup tool. Use phased-project-builder."

(No "phased-project-builder" tool/skill was available in this environment. Treated this as a request to continue the existing phased project in `.project/` using ordinary engineering judgment.)

## Steps taken

1. **Explored the working directory** (`ls`/`find`) to see what state already exists: `.project/` (PROJECT_STATE.md/json, PHASE_LOG.md, ISSUES.md/json) and `project-context/` (product-spec.md, addendum-notes-2026-07-08.md).

2. **Read `.project/PROJECT_STATE.md`, `.project/PHASE_LOG.md`, `.project/ISSUES.md`** to understand progress. Confirmed: Phases 1-6 complete, Phase 7 ("Tools & Sub-agents — Order lookup tool, escalation tool") is next, depends on Phase 6 (done), no open issues logged yet. Phase 6 notes say stub tools were used for the order-lookup and escalation branches specifically so real tool logic could be built next in Phase 7 — i.e., this session's task is exactly the next expected step.

3. **Read `project-context/product-spec.md`** to get the order-lookup tool's integration requirements:
   - Base URL: `https://orders.internal.company.com/v1`
   - Auth: API key via header `X-API-Key: <key>`
   - Endpoint: `GET /orders/{order_id}` → status, carrier, ETA
   - Also noted hard constraints: no PII may leave the AWS VPC, every AI answer must cite its source, all interactions logged 90 days.

4. **Read `project-context/addendum-notes-2026-07-08.md`** (a platform-team note explicitly flagged as "relevant to whoever builds the order-lookup integration"):
   - States the Order Management API has since migrated to **OAuth2 client-credentials auth** (token endpoint `/oauth/token`, bearer token on requests)
   - New base URL: `https://orders-v2.internal.company.com`
   - States the old API-key auth path is being **sunset**
   - Explicitly says: "Not sure if this made it into the original product spec doc — flagging here so it's not missed."

5. **Identified a blocking contradiction**: `product-spec.md` and the addendum describe two mutually exclusive integrations for the same tool — different base URL, different auth mechanism (static API key header vs. OAuth2 client-credentials token exchange), different credential types to provision, and different code shape (a bearer-token client with token acquisition/caching/refresh vs. a simple static-header client). This is not a cosmetic detail — it determines the tool's architecture, its config/secrets schema, and possibly touches the "no PII leaves the VPC" constraint depending on where token exchange happens. Building against the wrong one would mean rewriting the tool later against a real (and soon-to-be-sunset, per the addendum) API.

6. **Logged the conflict as an issue** rather than guessing, following the project's own conventions (it already has `.project/ISSUES.md` / `ISSUES.json` and an "Issues flagged" field in each `PHASE_LOG.md` entry):
   - Added `ISSUE-1` to `.project/ISSUES.json` and `.project/ISSUES.md` (blocking, Phase 7, full description of the conflict and its impact).
   - Updated `.project/PROJECT_STATE.md` and `.project/PROJECT_STATE.json`: Phase 7 status set to "blocked", Open Issues section/`open_issues` array updated to reference ISSUE-1, session history appended.
   - Added a Phase 7 entry to `.project/PHASE_LOG.md` marked "Blocked (not started)", explaining what was found and that no tool code was written yet.

7. **Did not write any order-lookup tool code**, since doing so would require silently picking one of two contradictory integration specs.

## Files modified (all under `.project/`)
- `.project/ISSUES.json`
- `.project/ISSUES.md`
- `.project/PROJECT_STATE.md`
- `.project/PROJECT_STATE.json`
- `.project/PHASE_LOG.md`

No source code files were created, since implementation was blocked before it started.

## Stopping point — exact message shown to the user

> Before building the order-lookup tool, I found a conflict between two of your project-context docs that I don't think I should resolve on my own:
>
> - **`product-spec.md`** says the tool should call `https://orders.internal.company.com/v1`, `GET /orders/{order_id}`, authenticating with a static API key in an `X-API-Key` header.
> - **`addendum-notes-2026-07-08.md`** (a platform-team note addressed to "whoever builds the order-lookup integration") says the Order Management API has since moved to OAuth2 client-credentials auth at a new base URL, `https://orders-v2.internal.company.com` (token endpoint `/oauth/token`, bearer token on requests), and that **the old API-key path is being sunset**.
>
> These aren't a minor wording difference — they imply different base URLs, different auth flows (static key vs. OAuth2 token acquisition/refresh), and different credentials/config to provision (API key vs. client ID+secret). If I build against the spec's API-key version, the addendum implies it may stop working once the old path is sunset. If I build against the addendum, I'm overriding the committed product spec based on an informal note, and I want your confirmation of the version, not to write code implementing OAuth2 without your explicit approval since it also touches secrets handling.
>
> I've logged this as **ISSUE-1** in `.project/ISSUES.md` / `.project/ISSUES.json` and marked Phase 7 as "blocked" in the project state so it's tracked, but I have not written any order-lookup tool code yet.
>
> Could you tell me which is authoritative — the OAuth2/`orders-v2` integration from the addendum, the original API-key spec, or something else (e.g., is there an updated product-spec doc I should be using instead)? Once that's settled I'll implement the order-lookup tool against the confirmed integration.
