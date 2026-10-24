# P7 verified: Calico Gloom Bombs melee resist shred with a melee partner

Sources: gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata (ability_nano_clustergrenade, line 85646), heroes.vdata, audit/items_full.json, data.js (current builds), localization citadel_heroes_english.txt line 1838. Helper scripts: council/evidence/duo/_p7_dump.js, _p7_melee.js.

## 1. Gloom Bombs (ability_nano_clustergrenade), verified

| Stat | Base | T1 | T2 | T3 |
|---|---|---|---|---|
| Cooldown (AbilityCooldown) | 14s | 11s (-3) | 11s | 11s |
| Melee resist reduction (MeleeResistReduction) | 0 | 0 | -6% per bomb touch | -6% |
| Debuff duration (MeleeResistReductionDuration) | 0 | 0 | 6s | 6s |
| Bomb count (GrenadeCount) | 4 | 4 | 4 | 7 (+3) |
| Damage (Damage) | 45 +0.644x ETechPower | same | same | same |
| Radius | 3.0m (ETechRadius) | | | |
| Fuse (Lifetime) / spacing | 0.75s / 0.05s between bombs, cast delay 0.15s | | | |
| MultiHitPenaltyPercentage | 65 (same target hit by several bombs takes reduced damage) | | | |

- Upgrade order in the vdata: T1 cooldown, T2 melee resist, T3 +3 bombs. The tier-2 text is "Per Bomb Touch: X% Melee Resist for Ys".
- Property type is MODIFIER_VALUE_MELEE_RESIST_REDUCTION (melee only). It is NOT MODIFIER_VALUE_BULLET_AND_MELEE_RESIST_REDUCTION, which is what Stalker/Hunter's Aura-type effects use. The stage A card wording "melee/bullet" is REFUTED: the bombs shred melee resist only, no bullet resist.
- Applied through m_DebuffModifier = modifier_nano_cluster_grenade_debuff (hidden, on the enemy, name key modifier_bullet_armor_reduction). Duration scales with ETechDuration (spirit duration items lengthen it). The reduction value has no spirit scaling. Damage scales with spirit power.
- Compare: Apollo's Riposte (ability_fencer_riposte) has the same property at -25% for 3.0s (T2).
- Current Calico build (data.js `calico`, order [1,1,2,2,3,1,4,3,4,1,4,3,4,3,2,2]): bombs unlock at pick 1, T1 pick 2, T2 at pick 6, T3 (7 bombs) at pick 10. Costs 1/1/2/5, so T2 is paid for at 7 AP total spent.
- Uptime: 6s debuff / 11s cooldown (T1+) = about 55% if rethrown on cooldown with a hit each throw. Before T1 it is 6/14 = 43%.
- Max shred if every bomb touches and stacks additively: 4 x 6 = 24% (T2), 7 x 6 = 42% (T3). Per-touch stacking, not refresh, is UNVERIFIABLE-FROM-FILES (the modifier logic is in compiled code, not the vdata).

## 2. Interaction questions

| Question | Verdict | Detail / Sandbox test |
|---|---|---|
| Exact melee resist value | VERIFIED | -6% per bomb touch, 6s, T2 (needs 2 AP at T2 level; 7 AP cumulative in current order) |
| Bullet resist reduction too | REFUTED | property is MELEE_RESIST_REDUCTION only |
| Stacks per touch (4 bombs = -24%, 7 bombs = -42%) | UNVERIFIABLE | Test: bot at 0 melee resist, Calico T2 throws bombs at its feet, read the target melee resist/debuff stack in the debuff panel, repeat at T3 (7 bombs). Also test whether 65% MultiHitPenalty affects the resist application (it should only affect damage) |
| Refresh vs stack across two throws | UNVERIFIABLE | Same test, second throw inside 6s |
| Applies to ALLY melee damage | UNVERIFIABLE (likely yes) | Debuff sits on the enemy and the property is the enemy-side melee resist reduction, so it should hit all melee taken. Test: Calico bomb a dummy, partner heavy melee it with and without debuff, compare damage numbers |
| Applies to ability damage flagged melee (Billy Bashdown CountsAsLightMelee; heavy at T3 'now deals 50% Heavy Melee Damage') | UNVERIFIABLE | Test: Billy Bashdown on a debuffed dummy vs clean dummy |
| Applies to item procs on melee (Spirit Strike/Snatch SpiritDamage, Lifestrike heal) | REFUTED by type | those are spirit damage/heal, not melee-resist scaled. Resist shred only helps the raw light/heavy melee hit |
| Calico's own Leaping Slash (ImpactDamage 10+0.8x ELightMeleeDamage, +60 at T3) benefits | UNVERIFIABLE | Test same as above, using Leaping Slash |

## 3. Partner melee damage in our current builds (data.js, final item set, all numbers from items_full.json stats)

Base melee (heroes.vdata): light 50, heavy 116 for Abrams (hero_atlas), Billy (hero_punkgoat), Shiv, Sinclair (hero_magician), Victor (hero_frank). Yamato 55/128. Calico 63/116. +1.58 per level (MODIFIER_VALUE_BASE_MELEE_DAMAGE_FROM_LEVEL). Melee reach 5m, half angle 30.

Melee bonus items: Melee Lifesteal +12%, Lifestrike +16%, Spirit Snatch +7%, Melee Charge +10% and +25 heavy bonus (BonusHeavyMeleeDamage), Crushing Fists +22% and +25 heavy bonus, Colossus +30% (ACTIVE: 37s cooldown, 7s duration), Runed Gauntlets +30%, Shadow Weave +25 ambush melee.

| Build id | Melee items in core | Melee % bonus (sum) | Heavy bonus | Note |
|---|---|---|---|---|
| abrams_melee | Lifestrike, Crushing Fists, Spirit Snatch, Colossus | 75% (45% without Colossus) | +25 | strongest, melee is the plan |
| billy_damage | Lifestrike, Spirit Snatch, Crushing Fists, Colossus (+ Berserker) | 75% (45%) | +25 | Bashdown also flagged melee |
| billy (tanky) | Lifestrike, Crushing Fists, Colossus | 68% (38%) | +25 | |
| yamato_brawler | Lifestrike, Crushing Fists, Spirit Snatch, Colossus | 75% (45%) | +25 | plus Crimson Slash buff +30% melee for 4s (BuffMeleeDamage, T2) |
| sinclair (melee) | Melee Charge (swap) / Crushing Fists, Colossus | 52% (22%) | +25 | Melee Charge is in core mid list but Crushing Fists upgrade replaces it |
| yamato (spirit) | Lifestrike, Spirit Snatch, Colossus | 53% (23%) | 0 | melee is secondary to Power Slash |
| abrams (tanky) | Spirit Snatch only | 7% | 0 | die |
| victor, victor_gun | none | 0 | 0 | Victor kit has no melee component |
| shiv, shiv_gun | none | 0 | 0 | Shiv melee only feeds Killing Blow rage (RagePerLightMelee 1.56, RagePerHeavyMelee 2.85); no melee dmg items |
| sinclair_bolt | none | 0 | 0 | |

Arithmetic (assuming additive resist, 0 base melee resist, shred multiplies the hit by (1 + shred)): heavy hit at 116 base x (1 + 0.75) = 203 pre-level; a -24% shred adds roughly 28 per base heavy and 49 on top of 203 at T2 four-touch, about 70-85 at T3 seven-touch if it stacks per touch. A single -6% (no stacking) adds only about 7 per base heavy. Swing rate/animation timing is NOT in the files, so melee share of the partner's DPS is UNVERIFIABLE. Sandbox: let partner melee a dummy for 10s with and without debuff, compare total.

## 4. Pair verdicts on the arithmetic

- Survive: Calico + Abrams (melee build), Calico + Billy (damage or tanky; Billy also reloads from melee via Blasted so melee is his DPS engine), Calico + Yamato brawler (melee % 75, Crimson Slash melee buff), Calico + Sinclair (melee). They all do repeated heavy melee and stack 38-75% melee bonuses.
- Weak: Yamato spirit (Power Slash does the damage, melee shred is secondary), Calico gun.
- Die: Victor (no melee kit, no melee items), Shiv (no melee items; the spirit Shiv's -6% spirit resist on Slice and Dice is a separate stat), Abrams tanky (7%), Sinclair bolt.
- Condition for all survivors: bomb timing. T2 only lands at pick 6 and the debuff is 6s against 11s cooldown, so the partner must commit melee inside the 6s window, and Colossus (7s every 37s) must be popped inside it to reach the 75% number. Cold-ratio checks: Crushing Fists applies a stacking BULLET resist debuff (-5 per stack, 8s, 6 stacks, 0.75s stun at max), which is separate from Calico's melee shred and does not overlap.
