# Final audit (round 14) — zero mistakes allowed

SP = /tmp/claude-0/-home-claude/47606c1f-aee7-5b4e-b80d-df074bbfb70f/scratchpad. Run from SP. Touch ONLY files for your assigned build ids: read a14/in/<id>.js, write a14/out/<id>.js (always, even if unchanged) and a14/log/<id>.md. Never write anywhere else, never loop over other files.

Kieran (Oct 20, 00:26): "One final audit. If there is a single problem, I will be very, very mad." He has repeatedly found mistakes after we said builds were audited. Your job: find EVERY problem in your builds, as a new-player-facing expert who has checked every claim against the game files and same-style public builds. Take as long as needed. Decide and fix yourself; never leave a question.

## Sources of truth
- Game files (current, build 6795, Oct 17): items `python3 -I audit_D_q.py "<Item>"` (stats, components, desc), abilities `python3 -I ab.py <class>` (classes in audit/hero_<id>.txt or new/hero_hero_<codename>.txt; charges, cooldowns, scaling, tier upgrades), hero stats in gt/repo/game/citadel/pak01_dir/scripts/heroes.vdata.
- Tools: `node a3/walk1.js <f>` (buy walk; must be FLAGS: none), `node a12/check.js <f>` (CHECK12: none, except colour-change swap lines you have walked and justify in the log), `node a7/sp.js <f> <orderString>` (spirit power and ability tiers at every buy).
- Same-style public builds only (post-patch, see a8/PATCH.md for dates): lockbuilds.com builds of that style, deadlocklabs, mobalytics filtered by the ability maxed first, tracklock pro matches only where the item set matches the style. A hero-wide pick rate is NOT evidence (Melee Charge 74% on Apollo comes from melee Apollo players).
- Kieran's rules: a14/RULES_KIERAN.md (his stated rules, oldest first) and a5/RULES.md. When rules conflict, the LATER one wins. The latest rules (Oct 19–20) override older ones:
  - separate builds per style replace pivots; his older "playstyle per hero" list now describes the MAIN build, the variants are the other styles;
  - item notes ONLY when needed (niche tip/interaction, item changes how you play, situational condition, what to sell once past 12 slots, what a swap replaces, Slot locked "Upgrade of X."); otherwise the note is EMPTY "";
  - build desc = short style label only ("Speedy AoE Paige", "Tanky Abrams"), or "" if it's how the hero is always played; never spikes, item explanations, how-to, or false claims;
  - names "Rizuhble's <style-describing name>"; the style must be obvious; ≤32 chars.

## Check EVERY one of these for EVERY item, note, box, desc, name and the ability order
A. Kit fit: the item's effect actually applies to how THIS build does damage/survives (read item desc + ability data). No range items on close-range heroes, no Duration Extender on infinite/channelled effects, no charge items on abilities without charges (AbilityCharges in ab.py), no proc items whose trigger the damage source can't meet (e.g. Lucky Shot needs bullets — Violet's Living Ink isn't bullets), no melee items on a flying hero, no token investments (one lone item of a damage type).
B. Same-style evidence: every item is used by builds of THIS style or justified by kit numbers you state in the log. Hero-wide rates don't count. Check the obvious better item for each job (Wraith anti-heal = Inhibitor, not Toxic Bullets; Drifter gets souls from picks → Trophy Collector, not Monster Rounds farming).
C. Imbues on the right ability: the one cast most often / whose number the item actually raises (Haze Surge of Power on dagger, never ult; Calico Compress on bombs). State cooldowns/scaling in the log.
D. Thresholds met at the buy point (a7/THRESH.md + ADDITIONS): Mystic Burst >80, Tankbuster >165, Spirit Burn 500 in 5s, Mystic Reverb 100, Recharging Rush 200 in 3.5s, Witchmail late, Tankbuster not rushed; use sp.js with this build's order.
E. Spikes: race to 4.8k in the main colour; health spike timing per hero (fighty heroes ~11–12k, sustain/escape heroes later), no big overshoot before the next spike; recount upgrades as the difference.
F. No long run (3+) of 6.4k buys before ~30k souls; no fresh T2s late; core fills 12 slots by itself; ≤8 items per box; every T1/T2 is upgraded later or has a named sell; sell-later dead-end items (Restorative Shot) bought first.
G. No item twice in one build. Rich box = T4 only and only pricier versions of things the build has. Slot locked = only tiny-gain expensive upgrades, notes "Upgrade of X.". Counters on every build with the required desc format ("Get after X if you need it. Ahead? Skip it until you feel like you're dying. Sell Y for it."), and the X and Y named must be in the build. If Dispel Magic is in, Divine Barrier is its rich upgrade. Losing-lane box = survival items only.
H. Swaps / situational boxes: concrete trigger a new player can check ("2+ of Shiv, Lash, Infernus, Vindicta"), each note says what it replaces, same job; walk the swapped build and confirm spikes. "Lost lane?" empty reorder boxes only if the reorder genuinely helps (verify mechanics: Lifestrike procs on light melee too and on troopers).
I. Every note and counter note is TRUE: verify each mechanic it claims in the game files (Dispel Magic doesn't answer damage like Geist's bomb; Unstoppable blocks stun/silence/sleep/root/disarm, not knockbacks; Spirit Resilience lists only heroes with real ticking spirit damage; spell Vyper). Hero names in counters must actually do what the note says. Empty every note that isn't one of the allowed kinds. No AI phrasing, no proc/threshold explanations, "your gun" not shotgun/beam/laser.
J. Ability order: copies what same-style popular builds actually do (state the source), and it must support the build's thresholds/imbues.
K. Name/desc/box captions per the latest rules above. Desc never explains. Box captions short.
L. Playstyle: the build is genuinely its named style (spirit Apollo has no melee items; support builds help the team; tank builds are tanky), and the variant pair is clearly different builds.

## Output
- a14/out/<id>.js: the corrected build (same JSON shape; keep id, hero, hk, abil, tg if present). Add one "Round 14:" line to `changes` summarising fixes.
- a14/log/<id>.md: for EVERY item in the build, one line: `<Item> (<box>): OK — <evidence: same-style source or kit number>` or `FIXED — <what and why>`. Then lines for: ability order (source), desc/name, each box caption, each note kept (why it's allowed + where verified), walk1/check.js/sp.js results. A reviewer will re-check your log line by line against the game files, so every claim must be verifiable.
- Final message: per build id, the list of fixes (or "no fixes") — nothing else.

## Specific known points
- Kelvin main build must be "tank damage-dealer Kelvin" (Kieran's words): damage but genuinely tanky; the existing one ends at only 11.2k health.
- Imbue items may keep a short "On <ability>." note.
- Existing builds' items may still rest on hero-wide rates from round 12: re-source every item from same-style builds.
- Builds with no published same-style ability order: find one (mobalytics filtered by max-first ability, lockbuilds builds that show orders); kit-based orders must be justified in the log.
- Rem's health 4.8k now lands at 17.6k after Echo Shard moved to 14.4k: check that's acceptable for a support (who must survive), fix if not.

## Standing checks added Oct 22 (every build, every agent; reviewer FAILS the build if any is missed)
M. Item relevance: each item raises a stat this build's damage sources actually scale with (abilities.vdata scaling), not just "gun" or "spirit" by colour.
N. Swap / "sell X for Y" / Counters boxes re-walked with the change applied: no colour that reached 4.8k in the base may drop below it.
O. Counters box: menu premise (buy only when dying, by killer, cheapest first); no T3 items in the rich box; Glass Cannon never on a health/tank build.
P. Buy timing: each item sits after the items that make it pay off (cost-efficiency agent output attached).
