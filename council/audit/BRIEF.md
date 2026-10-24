# Council audit brief (Kieran, 05:37)
Goal: find what the Council/build system ACTUALLY does vs what documents say. Be adversarial toward our own work. Do not trust any doc, agent report or summary as evidence; evidence = code you read and ran, data.js builds, generated outputs, logs, measured results.
Classification per item (one level, the highest PROVEN):
 R = only written in rules/docs/agent prompts
 C = coded (a script/tool/plugin function exists)
 I = integrated (the tool's output is actually consumed in the real workflow and visibly changes/gates the final build; show where)
 T = tested (run on real data and checked against a known answer or measured result; show the run)
Each conclusion needs: file path + line or command + observed output. If you cannot prove a level, give the lower level. Try to FIND cases where the Council claims to handle something but doesn't (e.g. run a tool on a crafted case, find builds that violate a claimed rule).
HARD CONSTRAINTS: read-only on /scratchpad/data.js and all builds (never edit builds, never run rebuild/merge). Do NOT send sandbox_cmd files or touch the PC / game / running tests (read logs only if present locally; the PC files are via device tools only if essential, read-only). Do not create new rules/agents/features. Write findings only to council/audit/<your-name>.md (scratchpad root = /tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad). Be concise: table rows of requirement | level | evidence | gap. Finish with TOP 10 gaps ranked by impact on build correctness.
Main transcript for requirements history: /root/.claude/projects/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f.jsonl (earlier sessions may exist in memory files /areas/deadlock-build-council.md, /topics/deadlock-building.md via mcp__memory__memory_read).
Key docs: council/{README,PROTOCOL,RULES_KIERAN,CHECKLIST,ROUTING,WEAKNESS_PROCESS}.md, council/rules.md, rules.md, council/sandbox/{TEST_MATRIX,PILOT,AUTORUN,GAPS}.md, council/agents/*.md. Tools: council/tools/*, gen/*, audit/*, prac/*, rebuild.sh.
