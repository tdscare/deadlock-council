# Review bridge: setup (proposal, 24 Oct 2026)

Status: nothing below is built or verified yet. Step 0 (preserve the project) is done.

## Trust boundary (what is actually enforced, and by what)
- Two private GitHub repos in your account:
  1. `deadlock-council`: the project. Claude pushes here. ChatGPT reads here.
  2. `deadlock-review`: owned only by you. Holds the reviewer charter, reviewer prompts, the review workflow and the API key (as a repository secret). Claude has NO write access to it. The boundary is repository ownership, not a folder rule.
- The review workflow lives in `deadlock-review`. It only reads project files as text (checkout of an exact commit, no project code is run), builds prompts from your charter plus Claude's review request, calls the Anthropic API, and commits the reviewer's answer to `deadlock-review/reviews/`.
- Claude submits requests as files in `deadlock-council/review_requests/` (question, exact commit, evidence paths) and answers criticism in `deadlock-council/review_responses/`. Requests are treated as untrusted data by the workflow.
- Claude reads reviews with a read-only view of `deadlock-review` (Step 5; needs a check that this environment can hold read-only access).
- ChatGPT gets read access to both repos through your existing ChatGPT GitHub connection.
- Round limit and spend limit are enforced in the review repo and in the Console, not by Claude.
- Anthropic-funded reviewers are Claude models in a fresh context. They are independent of the development agents' summaries, not a second vendor. ChatGPT is the cross-vendor reviewer.

## What you do (no scripts)
1. GitHub: create two empty private repos named `deadlock-council` and `deadlock-review`.
2. Tell me when done. I will push the preserved project snapshot to `deadlock-council` (needs GitHub linked to this chat: claude.ai Settings > Connectors > GitHub, grant it ONLY `deadlock-council`, not `deadlock-review`).
3. Console (console.anthropic.com): Workspaces > create `deadlock-review`; set its monthly spend limit; create an API key inside that workspace. Check the promotional credit shows under Billing/credits.
4. In `deadlock-review` on GitHub: Settings > Secrets and variables > Actions > New repository secret, name `ANTHROPIC_API_KEY`, paste the key. Never paste it into chat.
5. In `deadlock-review`: create a fine-grained read-only access token for it (Contents: read) only if we confirm this environment can hold one; otherwise ChatGPT relays, or we use a different read path.
6. You and ChatGPT write the reviewer charter and roles in `deadlock-review/charter/`. I will not write or edit it. I can supply a minimal workflow file for you/ChatGPT to inspect and commit yourselves, so the privileged code is yours.
7. Add ChatGPT's GitHub access: read-only on both repos.

## First acceptance test
Request: why does the optimiser rank "as-built" first in 0 of 81 builds? Evidence: COUNCIL_AUDIT.md plus `council/tools/abtimeline.py`, `council/evidence/strategy/`. Reviewer must cite code or data, challenge assumptions, propose a verifiable next step. I reply with evidence. Max 2 rounds, then escalate to you. Full exchange stays in git for ChatGPT.

## Cost controls
Promo credits first (check Console), workspace limit set below the credit balance, per-run token cap in the workflow, review only on explicit request, never per experiment. Spend report from Console usage per workspace plus a log of each review's request, tokens and outcome.
