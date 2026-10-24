# Deadlock Council project: index

Preserved snapshot of the working project, taken 2026-10-24. Nothing here was rewritten for the snapshot.

- `council/`: the Council itself. Existing authority documents: `council/PROTOCOL.md`, `council/rules.md`, `council/RULES_KIERAN.md`, `council/ROUTING.md`, `council/WEAKNESS_PROCESS.md`, agent instructions in `council/agents/*.md`. There is no CLAUDE.md.
- `council/COUNCIL_AUDIT.md`: independent audit of the current system (24 Oct 2026).
- `council/evidence/`: extracted effects, hypotheses (`interactions/`), measured results (`interactions/validated/`), strategy outputs.
- `council/sandbox/`: Sandbox tester docs (CONTINUE.md, SCOREBOARD.md), results, scenarios.
- `council/tools/`, `council/lib/`: optimiser, discovery and gate code.
- `council/frozen/`, `council/history/`, `council/approvals/`, `council/proposals/`: data.js freeze, gate reports, approval records, unapplied proposals.
- `site/`: the build site (`data.js` = the 81 builds, read-only by rule; `app.js`, `builds.html`).
- `plugin/`: Sandbox tester plugin sources (C#), no binaries.
- `sandbox_docs/`: handoff documents and test notes.

Not included: credentials, game binaries, raw PC logs (plugin.log etc.), compiled plugin DLLs, large caches. Raw sandbox logs and result files live on the PC under `E:\deadworks-server\` (`sbx_logs`, `sbx_queue\results`) and will be added with hashes when the evidence bridge is built.
