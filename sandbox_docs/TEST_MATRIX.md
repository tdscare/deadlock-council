# Sandbox test standard (Kieran, Oct 23-24). Agents work all of this out themselves; Kieran should never have to say "go test X".
Agents continuously audit and test EVERY build (all heroes), pick uncertain items and substitutes on their own, and report what is best.

## What to test, decided by the agent (not asked)
1. Every uncertain item or slot: list all similar substitutes (same job, same tier) and test them (Leech vs Infuser vs Vampiric Burst vs Bullet Lifesteal; Recharging Rush vs Extra Charge vs neither on Grey Talon arrows; etc.). Also test "none".
2. Hero economy: how does this hero make souls? (Billy cannot farm well -> Cultist Sacrifice, ~8:00; check every hero.) Time purchases to real clock (~7k souls at 8:00).
3. Early game feel at low price points: ~8k, 10-12k (laning), then 20k, 30k, full 12. Check: cooldowns back fast enough, enough health, enough damage, enough ammo (Haze Assassin: Tesla Bullets for farm but no mag -> constantly reloading; fix with spirit or ammo item), health spike present, damage taken when shot. Early-support heroes (Dynamo, Solomon) must still do damage early (Dynamo stomps); don't rush Rescue Beam in lane.
4. Support/utility: score outcomes not raw numbers (does the ally survive the same burst: Healing Nova vs Rescue Beam; ult range/coverage).

## Realism rules
- Accuracy: players hit ~40-50% of shots. Run 100%, 50% and 40% hit rates, and a body/head mix (not only headshots). Report whether the winner changes.
- Enemies: not one dummy. Surround with 4-5 bots at close range for aura/AoE items (Infuser, Healing Aura, Nova...), shoot one. Also single-target. Report both; a 5-bot aura test alone is not realistic.
- Incoming damage: spirit AND gun damage on the player, at realistic rates; test low HP states (Pain Battery, Berserker self-damage, lifesteal/heal only matter when below max HP: start low and keep damaged).
- Stacking mechanics: test at 0, 1 and max stacks (Berserker). Report each.
- CC: hard CC and soft CC against the build. What answers do we have (Unstoppable, Reactive Barrier, Dispel, Rapid Recharge cleanse, Warp Stone)? Seven needs Unstoppable (knockdown/outrange/stuns); Haze may not care about disarm (Rapid Recharge on 2); Wraith values Dispel (slowing hex stops TP). Decide per hero, test with CC applied.
- Range-limited items (Infuser etc.): how does the hero get in range and stay there (speed, Warp Stone, Phantom Strike, Mystic Expansion)? Test with enemies that run away.
- Enemy never dies: infinite/regenerating health or resist items; re-fetch before every burst. Enemies also buy resists: run vs 0 and vs realistic bullet/spirit resist; resist-shred items (Bullet Resist Shredder, Escalating Exposure, Mystic Vulnerability, Tankbuster) judged only in resist runs.

## Clean state between blocks
Full reset every block: remove ALL items, respawn/refresh player (new pawn if needed), reset cooldowns, clear buffs (Mercurial Magnum and other long actives persist otherwise), wait out cooldowns, heal. Randomize/counterbalance block order and repeat >=3 times (first block runs low: warm-up effect observed: first variant 773/797 dps in both orders).

## Optimal rotations per hero (agent derives from the kit, never a flat key-mash)
Ability order and timing matter: e.g. Haze needs knife before ult for Surge of Power; Danny flies up, 2, then ult when enemy < half HP (bonus damage); Seven Lightning Ball charges; Grey Talon arrow charges; Victor Berserker stacks. Keep imbue/proc conditions satisfied in the script. Verify each rotation against the kit data before using.

## Coverage
Every hero/build, including Deadman Danny and all alt builds, then re-run on each patch (new items/heroes) automatically.

## Findings so far
- Victor gun, Leech/Infuser/Vampiric Burst swap, full build, both orders (Oct 24): damage VB > Infuser ~ none > Leech; healing no separable difference (regen/other heals dominate); first-block warm-up bias. Inconclusive on healing: needs low-HP start, bullet-only, accuracy runs.

## Healing attribution (Kieran, Oct 24): the "nothing in the slot" block still healed ~107 hps (vs 88-114 with Leech/Infuser/VB), so other sources dominate
Victor's own healing: Pain Battery (heals 15% of MISSING health, scales with spirit), Jumpstart (15% of max HP), Spiritual Overflow (built-in spirit lifesteal), Healing Tempo (more healing), Frenzy (bullet lifesteal), plus regen. Any build has kit lifesteal + other items; list every heal source of the hero/build from game data first.
- Measure a baseline block with the slot empty AND with each other heal source isolated, then report the marginal healing of the slot item (item minus baseline), at several HP levels (start low and stay low so healing is not capped by max HP).
- Log healing by source where possible (or isolate via item removal); never read a raw hps total as the item's effect.
- Pain Battery-type effects only matter when low: test at low HP; Berserker-type stacks at 0/1/max.

## Hero-aware testing (Kieran, Oct 24 night) - understand how each hero's abilities interact with the thing being tested
- Read the kit before designing the test. Examples: Abrams gets regen while actively taking damage (Healing Booster) and Witchmail gives cooldown: lifesteal items tested only by shooting at low HP will wrongly look worse. Rend does 134+137 from range but +55% heavy melee damage and silence up close: measure at the range the hero actually uses it. Shiv's knives multiply damage per knife in and by rage: test with and without building rage and decide if building rage is viable. Victor Berserker stacks.
- Support/utility: measure downtime. Rem's build is built on Healing Nova + Echo Shard + her 2: what can she do (damage? heal? anything for the team) while all are on cooldown? Fewer idle seconds = better. Report idle time per hero.
- Engage/catch/escape: how does the hero catch targets, slow them, debuff late when enemies have lots of resistance; how does it deal with fast/escape heroes (Mina, Vindicta flying)? Danny needs to reach Vindicta in the sky while she shoots him; how? Test with mobile/ranged enemies, not just a standing bot.
- Ults and sustain are tested too, not only gun/ability damage.

## Test hygiene (hard requirement)
- Enemy bots get god mode (never die). Before EVERY block wipe both sides: remove all items from player AND enemies, clear debuffs/buffs, reset cooldowns/charges, reload/respawn, then give the new build.
- Do this for every item, every hero, every build; run overnight autonomously; report in the morning what is optimal vs not, with changes proposed to data.js (never auto-apply removals without verification).

## Price points and buy order (Kieran, Oct 24 01:43)
- Test at 10k, 18k, 24k, 30k souls (and full 12), not at spikes only. At each: damage, fire rate, ammo, health, cooldowns, feel.
- Buy the build LEFT TO RIGHT exactly as in data.js (Early, Mid, Late box order, components then upgrades as a player would). Never cherry-pick "good" items or random pairs; people follow the order, so the tested loadout at N souls = the items bought in order up to N.

## Order and hero-specific play (Kieran, Oct 24 01:49)
- Test heroes alphabetically: Abrams, Apollo, Baba, Bebop, Billy, Calico, Celeste, then on through the roster and Deadman Danny.
- Every plan must model how the hero is actually played, not stand-still-and-press. Per hero, the planner reads the kit and writes the positioning/rotation, including what a real player can't do (e.g. stand in a whole dash trail).
- Miss shots by aiming slightly above or to the side of the target. No big mouse flicks.
- Actives (Alchemical Fire, Paradox Focus Lens etc.): use them first in the rotation, at the right moment (Focus Lens pays 30% of damage dealt on expire). Every item's interaction is checked, not just passives.
- Souls: for each hero decide whether the build needs souls and how it gets them (Trophy, Cultist, farming ability). Weak farmers (Deadman Danny) need an explicit answer, as does an assassin build that doesn't need souls.
- Range/economy questions per hero (e.g. Lash): does the ult reach, does it need earlier points, Greater/Mystic Expansion earlier, Trophy for range.

Per hero notes:
- Abrams: melee build, must be in punching range. Test tanky Abrams vs several enemies, some gun, some spirit.
- Apollo: 3 lunges forward (can miss a target straight ahead, aim/steer); 1 lunges him backwards, so position shifts.
- Baba: 2 gives a unique melee; steals spirit power, so test against spirit heroes.
- Calico: invulnerable AoE around herself, must be next to an enemy. Gloom Bombs and dash are easy to miss.
- Celeste: build stacks on 3 before ult.
- Drifter: no isolated damage unless he ults the target; starts with no isolated stack, so early numbers read low (note it).
- Grey Talon: damage grows per owl kill.
- Infernus: dash leaves afterburn; nobody stands in it the whole duration, so don't credit full-duration damage.
- Kelvin: extra damage while riding the ice path, but the path moves him off his aim.
- Lash: damage scales with height; see range questions above.
- Deadman Danny: poor farm; assassin pattern is 2 slam then ult.

## Additions (Kieran, Oct 24 02:24)
- Price points: add a lane checkpoint at ~5k souls (very early game) and a full-build (12 items) checkpoint, besides 10k/18k/24k/30k.
- Stack mechanics are everywhere, not just Berserker/Celeste. Model every one the build uses:
  - Hit-based amps: Celeste 3 (damage amp per hit), Pocket Barrage, Ballistic Enhancement imbued on an ability (+20% per target hit, scales with multiple targets: 40/60/80), Celeste Radiant Daggers (+7% spirit per hit, max 6 stacks), Glass Cannon, Fiery, etc. Read each item/ability for its stack rule; hit one vs several targets accordingly.
  - Berserker: weapon damage up as you take damage; 120 damage taken = 1 stack, max 10, 10 s window. Taking damage while stacked refreshes the window; if the window lapses all stacks reset to 0. Self-damage keeps them (Geist Daggers, Vampiric Burst, maybe others; towers and troopers may also give stacks).
  - Weapon quirks: Danny's charging gun, McGinnis ramping Fiery. Read every hero's gun.
  - Drive stacks with real play (hit with the ability, take incoming damage) or lowhp/hurtme/incoming; test 0 / partial / max.
- Accuracy: mix headshots and body shots using a realistic high-rank average (Eternus-level; best guess if no source, state the figure). Not body-only.
- Healing by source: the game's end-of-match stats screen has graphs for healing by type, regen by type, damage by type, souls by source. Try to read it (or the equivalent data in-game); otherwise subtract with/without runs.
- Read every hero and every ability/item in the game (parallel sub-agents) before planning, then keep testing.

## Confounds: kit first, Occam's razor (Kieran, Oct 24 03:59)
- Before crediting a damage difference to an item, a headshot, or a build, check the hero's own kit for the simple explanation: gun that ramps per hit (stacking damage per bullet landed, charge-up, spin-up, Fiery ramp), ability stacks, passive resets/decays, cooldown state, ammo/reload state.
- Every block must start from the same kit state: wait out stack decay / reset timers (verify stacks are zero via modifiers or a fixed idle period from the kit data), cooldowns ready, full ammo, same distance. Order effects (the first block low, a later block high) are the first suspect, not the item.
- Measure in a way that separates them: report damage per shot by consecutive-hit index (shot 1, 5, 10...) and by head/body, so ramping and headshots are visible separately. Compare items at the same stack count, not the same elapsed time.
- Write the likely kit explanation for every result next to the number, and only credit an item/build when the kit explanation is ruled out (counterbalanced order, equal stacks).
- Figure out each hero individually; none is generic. Time-in-effect confounds: Victor's aura does more damage the longer it stays up, so an item tested for longer looks better only because the target was in the aura longer. Every comparison uses identical durations and identical time-in-effect (aura/DoT/channel/ramp age), and per-second numbers are reported against effect age. The hero in the log was Haze (the enemy bot default); the player's hero is whatever the build is for, never assumed.

## Boons, ability points, distance (Kieran, Oct 24 04:06)
- Test with the boons and ability points a player has at that soul level, not max. At each checkpoint set hero level (boons: HP, damage, etc.) and spend ability points in the build's listed order (data.js ability order, `abil` per slot) so each tier does what it does at that point. Verify with a log of level, max HP and per-ability tier at every checkpoint. Current tester state (unlock 7 = all abilities max everywhere) is wrong for every checkpoint below full build.
- Distance: for close-range abilities and items (melee, Calico, Abrams, shotguns, point-blank effects) the enemy is moved to the ability's effective range (use `fetch <dist>`/enemy placement), not left at 350 units. Take the range from the kit data per ability; range-limited items (Long Range vs Close Quarters) are tested at both ends.
