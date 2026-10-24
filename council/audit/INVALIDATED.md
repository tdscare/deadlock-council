# Invalidated results (audit, 05:5x)
- Root cause FIXED in tooling: spirit/level was hardcoded 1.1 (a7/sp.js, gen/ac1_sp.js, gen/spirit3.js). Now read from heroes.vdata via council/lib/herostat.js. Originals: *.pre_tp. abtimeline.py already correct.
- Affected builds (spirit-per-level differs from 1.1): haze, haze_assassin (0.5); greytalon, greytalon_gun (1.6); kelvin, kelvin_support, viscous, viscous_damage, sinclair, sinclair_bolt (1.3); ivy, ivy_carry (1.2). Any sp.js/ac/spirit3 output for these before this fix is INVALID; re-run before relying. contam.md: no shipped decision flips found (needs re-run confirmation; Viscous Tankbuster delay is the only borderline).
- Haze worked example + haze_model.py: weapon-investment table above 4.8k wrong (E2), vitality investment omitted (E3, changes survival results a lot), self-referential enemy damage, no farming/income. All its order/survival claims and confidence numbers are INVALID as decision evidence. Haze reorder stays UNAPPROVED.
- Victor lifesteal sandbox table + "VB > Infuser ~ none > Leech": INVALID (unlock 15, no setup checks).
- Any Sandbox run using accseed: not seeded; unvalidated.
- Open: strict-queue vs two-queue ability-point model (24 builds differ; nurse, lash have enabling items in the window) needs one live-game check.
