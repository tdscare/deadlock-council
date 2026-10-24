# Model routing

Goal: Opus only where judgement is the product. Everything checkable runs on the cheapest model that passes the task's gate.

| Tier | Model | Used for | Agents |
|---|---|---|---|
| T0 mechanical | haiku | run scripts, validators, merges, file/format work, data extraction into kit sheets, ledger runs | `clerk` |
| T1 working | sonnet | everyday coding, plugin/tester implementation and debugging, Sandbox experiments and their orchestration, routine analysis, research (patches, public builds, Reddit), full item scans, build comparison, ability timelines, test planning, drafting builds, computer use, imports | `researcher`, `hero-analyst`, `item-analyst`, `comparer`, `ability-checker`, `sandbox-planner`, `sandbox-tester`, `builder`, `importer`; ad-hoc runner/coder agents (spawn with model sonnet explicitly) |
| T2 judgement | opus | Council architecture, theorycraft (unconventional strategies, synergies, kit-first theses), weakness/dependency-chain analysis, investigating contradictory or surprising results, adversarial review of important decisions, final sign-off | `theorycrafter`, `weakness-solver`, `reviewer` |

Never routed: fable (cost; only if Kieran asks).

## Rules
1. Each agent file pins its own `model:`. Do not set `CLAUDE_CODE_SUBAGENT_MODEL` (it overrides every agent file and flattens the routing).
2. Gate-based escalation: an agent's output must pass its gate (validators, schema, checklist). On failure retry once at the next tier up with the failure text attached. Never escalate on a hunch.
3. Opus works from curated kit sheets, item tables, timelines and test results produced by haiku/sonnet; targeted lookups in game data are fine, bulk extraction/scanning is not.
4. Independence: `reviewer` gets the finished build + rules + evidence, not the author's reasoning.
5. Computer use (Sandbox, import) is sonnet minimum; haiku is not reliable at reading small on-screen numbers.
6. Verified, not assumed: agent files pin `model:` and the Agent tool honours it (checked in agent transcripts: theorycrafter and weakness-solver ran as claude-opus-5-5; general-purpose/runner agents ran as claude-sonnet-5-5). Re-check a transcript's model field after changing routing. Agents already running keep the model they started with.
7. No repeated work: weakness/theory analyses are cached in sandbox/weaknesses/*.md; re-run Opus on a hero only when the build, the item/hero data (patch) or the evidence changed, or a test contradicts a verdict. Orchestration, test running, log reading and data extraction stay on sonnet/haiku; Opus is called for the decision steps (thesis, synergy pricing, contradiction analysis, review), with the sheets as input.
8. Escalate on evidence: a sonnet result that fails its gate or contradicts another result goes to Opus with the failure text; Opus handing back mechanical work (re-running scripts, collecting numbers) goes down to sonnet/haiku.
9. Reasoning effort is not set per call here (the Agent tool only accepts an effort override when explicitly requested for a specific level); effort follows the model/agent definition defaults. Do not claim otherwise.
