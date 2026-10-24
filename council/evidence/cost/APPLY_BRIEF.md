# Apply cost-efficiency fixes (one chunk)
Scratchpad: /tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad (cd there). Rules: council/RULES_KIERAN.md, CHECKLIST.md. Kieran wants every colour at 4.8k early on most heroes; Mercurial Magnum counts as GUN per his rule; swap/"sell X for Y" boxes must not drop a colour below 4.8k; T3 items never in the T4-only rich box; notes only where needed, captions <=112 chars; core fills 12 slots.

Inputs per build: council/evidence/cost/<id>.md (findings + tested minimal fix) and your chunk summary council/evidence/cost/SUMMARY_<n>.md; renames: council/evidence/names/renames.json ({id:{old,new,why}}).

For every build id in YOUR chunk (list given below) EXCEPT nurse, mirage, graves_ult (another agent owns these):
1. Apply every HIGH/MED flagged fix whose fix is stated (swap-box repair, sell-for repair, buy-timing move). LOW fixes: apply if free (no spike moves, no cost). "Colours that never reach 4.8k" items are policy decisions: do NOT change them, list them.
2. Apply the rename from renames.json (data.js stores names as "Rizuhble's <name>", no suffix).
3. For each changed build add/extend its `changes` entry with one short line per change.
4. Re-verify each changed build: `node a3/walk1.js`, `node a12/check.js`, `node a7/sp.js` on a temp copy (see how council/work files are checked; the work files in council/work/*.js are the format), spikes intact or improved, 12 core slots, no box >8 items.
5. Write each changed build as an out file to council/apply/chunk<n>/out/<id>.js (same object format as council/work/*.js and a19 out files). DO NOT run merge.js and DO NOT edit data.js (the main session merges all chunks).
Reply with: builds changed (id: one line list of changes), fixes skipped and why, policy items left, and any build that failed a check.
