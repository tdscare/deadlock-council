# Strategy evidence index (stable paths; all read-only for readers)
Every file carries BODY-SHA and INPUT-SHA; if INPUT-SHA differs from `python3 -I council/tools/abtimeline.py --input-sha` the file is stale and must not be quoted.
Tags: VERIFIED MECHANIC / CONTROLLED SANDBOX RESULT / MODELLED ESTIMATE / UNVERIFIED HYPOTHESIS. Tiers: MODEL-ONLY / SUPPORTED / INSUFFICIENT.

| what | path | regenerate |
|---|---|---|
| purchase-timing flags, all builds (pipe table: build, item, bought at, net cost, value now %, per 1000 souls, delay alternative, same-cost alternatives, flag) | evidence/timing/ALL.txt | --timing ALL |
| selling / thresholds / item roles / ledger / branches, one per build | evidence/path/<id>_sequence.txt | --seq <id...> |
| sales JSON used by the gate (rule 4f) | stdout | --sales <id> |
| contribution profile by match phase | evidence/profile/<id>.txt | --profile <id...> |
| range / spacing / multi-target plan and requests | evidence/range/<id>_<checkpoint>.txt | --range <id> --at N [--item X --vs Y --queue] |
| situational swaps | evidence/situational/<id>_<item>.txt | --situational <id> <item> |
| team composition | evidence/team/*.txt | --team <id> --allies a,b --at N |
| investment totals | evidence/investment/<id>.txt | --investment <id> |
Caveats to keep in any caption: resale refund 0.5 and the full-tier-price investment rule are UNVERIFIED HYPOTHESES; the trade model overvalues cheap defensive greens (the as-built path wins no grid cell in any of the 81 builds), so a "weak now" / "delay looks better" flag is a review flag, not a verdict.
