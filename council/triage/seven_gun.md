# seven_gun (Static Shock Seven) - triage vs CLEANBASE
Base: council/frozen/data.CLEANBASE_pre_spikefix.js. Current: data.js. Proposal: council/proposals/seven_gun.json -> council/work/seven_gun.js (gate check: PASSES with one waiver, not applied). Calc: council/triage/seven_calc/m7.py (assumptions in header), tables seven_gun_N_compare.txt, seven_gun_paths_hero.txt, early_orders.txt.
Grade: calculated, unvalidated. Percentages are model outputs, not accuracy. No evidence/seven_gun.json: nothing measured to apply. 6819 changed no stat used here; Spiritual Overflow text now says "heroes" (ally proc unconfirmed, not relied on).

## Kit facts used
Seven's gun: 3-round burst, 10.8 per bullet, 0.2625 s cycle, 29 mag, 2.35 s reload. Power Surge: one proc per burst shot (LOC), DamagePerChain 10 +0.14x spirit, T2 +8 +0.23x, T3 +10 s and -15% spirit resist, chains to 4. So fire rate multiplies both gun and Power Surge damage. Surge of Power's 20% fire rate is conditional (8 s after casting the imbued ability).

## What changed since the clean base (silent "sevengun" pass; audit/builds.md:41-42,67)
1. Enchanter's Emblem removed; Rapid Rounds -> Swift Striker added before Cultist. 2. Spiritual Overflow moved before Unstoppable. 3. Witchmail removed from rich (it sold Enchanter's). 4. Escalating Exposure / Surge of Power box moves (order otherwise same). 5. Ability order 3311234324141224 -> 1331234324141224. 6. desc "Gun-spirit Seven" -> "Gun Seven".
Spikes clean -> current: gun 5.6k -> 7.2k, spirit 11.2k -> 11.2k, health 14.4k -> 40.0k.

## Verdicts
| change | verdict | evidence |
|---|---|---|
| Enchanter's out, Rapid Rounds -> Swift Striker in | MISTAKE as done | Health 4.8k at 40.0k (HP 2.4k at 36.8k); gun 4.8k 1.6k later with a 1.6k overshoot; Swift Striker a dead-end T2 with no upgrade or sell. Current vs proposed: +11..+30% gun+Power Surge damage at 7.2k-12.8k, +9..+12% at 14.4k-28.8k, but HP -10..-30%. |
| fire-rate idea itself | INCONCLUSIVE, not adopted | V5 (Swift Striker in Improved Spirit's slot, spikes kept): +2..+5% damage, -7..-10% storm DPS, -3% HP, Boundless +1.6k, 13th slot. Burst Fire variant (on-hit 32% counted as always up): +10..+17% at 17.6k-24k but a 3.2k T3 not in same-style builds and an optimistic proc assumption. Possible cap: Power Surge ChainTickRate 0.2 s vs bursts every 0.19 s at +40% fire rate (UNVERIFIED). Hypothesis seven_gun_N2. |
| Spiritual Overflow before Unstoppable | MISTAKE | Consumes Spirit Lifesteal before Unstoppable: health invest drops to 1.6k at 33.6k; same-style source says rush Unstoppable. Restored Unstoppable first. |
| Witchmail removed | consequence; restored | Witchmail (T4: 14 spirit, 22% spirit resist, 7% CDR) is the pricier version of Enchanter's Emblem, which is back. |
| box moves | LEGIT/no effect | box boundary only. |
| order 3311 -> 1331 | LEGIT intent, wrong result | same as seven: under the game-data model ball T1 stays at 900; 1133 gives 200 (under old model B 1331 is right). |
| desc "Gun Seven" | UNKNOWN | wording only; no rule decides between "Gun Seven" and "Gun-spirit Seven". Kept current. |

## Pre-existing problems fixed (clean base had them too)
- Health 4.8k after the spirit spike (spirit 11.2k, health 14.4k) against Kieran's priority (damage spike, then health spike) for a hero with no escape and no kit sustain. Proposed: Duration Extender, then Spirit Lifesteal, Sprint Boots, Enduring Speed (health 4.8k at 12.0k), then Surge of Power (spirit 4.8k at 14.4k). Vs clean: HP +12/+28/+14% at 10.4k/12.0k/12.8k, damage +2% at 10.4k, -13/-14% at 12.0k/12.8k, identical from 14.4k. Hypothesis seven_gun_N3. V9 (greens before Duration Extender) loses 19% damage at 8.8-10.4k: rejected.
- Superior Duration (T3) in the rich box: moved into Late as the Duration Extender upgrade (+1.6k; same-style official late core). Power Surge window 24.4 -> 25.6 s, global duration, 8% bullet resist.
- Mystic Vulnerability fresh at 20.8k: moved before Tesla Bullets (17.6k).

## Corrected progression (council/work/seven_gun.js)
Early: Monster Rounds, High-Velocity Rounds, Opening Rounds, Extra Spirit, Cultist Sacrifice, Enchanter's Emblem, Duration Extender (Power Surge), Spirit Lifesteal. Mid: Sprint Boots, Enduring Speed, Surge of Power (Power Surge), Improved Spirit, Mystic Vulnerability, Tesla Bullets, Toxic Bullets, Escalating Exposure. Late: Unstoppable, Superior Duration, Spiritual Overflow, Boundless Spirit. Rich: Spirit Burn, Ricochet, Witchmail, Lightning Scroll, Divine Barrier. Counters / Slot locked / Losing lane unchanged. Order 1133234324141224.
walk1: gun 4.8k @5.6k, health @12.0k, spirit @14.4k, 46.4k, 12 slots, FLAGS none.

## Gate (node council/tools/gate.js check council/proposals/seven_gun.json)
Fixed 8: Swift Striker and Duration Extender not upgraded, Spiritual Overflow threshold line (supplied by the reason), Mystic Vulnerability fresh T2 late, Superior Duration T3 in rich, gun/spirit overshoot before health, health 4.8k after 16k.
WAIVED: MAIN_4.8K_LATE (checker treats spirit as main by late T4 cost; gun is main and lands at 5.6k; spirit delayed on purpose, comparison in seven_gun_N_compare.txt). No order of these items gets gun and spirit both under 8k with health near 12k.
UNRESOLVED (pre-existing, can't fix without breaking rules): CORE_NOTE_NONEMPTY Unstoppable (allowed tip: only a stun ends the storm); T1T2_NOT_UPGRADED_OR_SOLD Enduring Speed (false positive, Juggernaut is its Slot locked upgrade).

## Open questions and dependencies
- Order string model A vs B: flips the order verdict only (A: 1133, B: 1331). Queue strictness: no effect.
- 1-charge counting: no charge item; no effect.
- Spiritual Overflow proc: build-up 1.08 per shot, decay after 2 s (reload 2.35 s), one-and-done; whether "shot" is a bullet or a burst is unverified: 8-24 s of hero hits to charge. Kept (same-style build, passive stats are Spirit Lifesteal's).
- Power Surge ChainTickRate cap at high fire rate: unverified; matters only for the fire-rate rival.
- Numbers that would move the verdicts: Swift Striker 20%, Enchanter's 15 spirit/18% spirit resist, Superior Duration 28%, vitality and weapon invest tables, Power Surge scaling. 6819 changed none.
- Model-only: continuous hits on one target, no movement, bounces not counted, HP ignores Cultist's +4/boon.

## Scenarios
seven_gun_N2_fire_rate_vs_emblem, seven_gun_N3_health_before_spirit, seven_N0_order_ball_first (council/sandbox/scenarios/). Pending.
