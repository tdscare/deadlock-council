# Deadlock Build Council

Builds on the existing system (SP = scratchpad root): `data.js` (81 builds) → `rebuild.sh` (site) → `mkcodes.js` (import codes) → in-game import. Nothing in that pipeline changes. The Council sits in front of it and decides *what goes into data.js*.

| Piece | Where |
|---|---|
| Agent definitions (model per agent) | `agents/*.md` (installed to `/home/claude/.claude/agents/`) |
| Model routing policy | `ROUTING.md` |
| Workflow + gates | `PROTOCOL.md` |
| Kieran's rules (unchanged, authoritative) | `RULES_KIERAN.md`, `CHECKLIST.md`, `rules.md` + memory file deadlock-building |
| Sandbox Tester | `sandbox/` (scenarios, schema, results) |
| Evidence → decisions | `tools/ledger.js`, `evidence/<hero>.json` |
| Existing checks the Council must pass | `a3/walk1.js`, `a12/check.js`, `a7/sp.js`, `a25/full.js` |

Principle: a claim about a build (item X helps, order Y is better) is either backed by game-file numbers, by Sandbox results graded A/B, or flagged as untested. Sandbox results can overturn a calculation; a calculation cannot overturn a clean A-grade result without a stated reason.
