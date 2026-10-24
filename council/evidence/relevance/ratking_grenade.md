# ratking_grenade (Trash Lobber Rat King) — item relevance to the damage source

Damage sources (abilities.vdata, `python3 -I ab.py ability_ratking_scrap_grenade`):
- Scrap Grenade: DamagePerShrapnel 70 (+0.6x EBaseWeaponDamageIncrease), +70 at T2, T3 +1 detonation and a 300 (+1.0x) big blast; 26s cooldown, -8s at T1. Deals BulletDamage (localization).
- Rule, Ratannia!: 200 (+1.2x EBaseWeaponDamageIncrease).
- Rat Swarm: 8 (+0.08x spirit) per bite (minor, spirit).
- EBaseWeaponDamageIncrease = MODIFIER_VALUE_WEAPON_DAMAGE_INCREASE (item stat BaseAttackDamagePercent, "Weapon Damage %") + weapon soul-investment bonus (heroes.vdata: 4.8k 46, 6.4k 54, 8k 62, 11.2k 74, 16k 86, 22.4k 100).
- Range bonuses are different modifier values: Long Range/Sharpshooter `LongRangeBonusWeaponPower` → MODIFIER_VALUE_LONG_RANGE_BULLET_DAMAGE_INCREASE; Close Quarters/Point Blank `CloseRangeBonusWeaponPower` → MODIFIER_VALUE_CLOSE_RANGE_WEAPON_DAMAGE_INCREASE. Neither is in the grenade formula.

Per-item verdict (old build), grenade effect = 0.6 x Weapon Damage % per detonation:
| Item | Grenade-relevant stat | Per detonation | Verdict |
|---|---|---|---|
| High-Velocity Rounds | 8% WD (bullet speed irrelevant: grenade has its own 1300/1500 projectile) | +4.8 | OUT (Extended Magazine gives the same 8% with a better upgrade) |
| Monster Rounds → Cultist Sacrifice | Cultist 10% (+0.8/boon) WD, farm | +6 | KEEP |
| Long Range | none (40 conditional long-range bullet bonus) | +0 | OUT |
| Sharpshooter | 10% WD (+60 conditional) for 3.2k | +6 | OUT |
| Battle Vest | 18% WD above 65% hp | +10.8 | KEEP |
| Sprint Boots → Enduring Speed | movement | — | KEEP (mobility) |
| Extra Health → Fortitude | health; cape barrier scales with max health | — | KEEP |
| Mystic Expansion → Ballistic Enchantment (grenade) | radius; +20% WD per hero hit (WEAPON_DAMAGE_INCREASE) | +12 per hero hit | KEEP |
| Compress → Superior Cooldown | grenade cooldown | — | KEEP |
| Greater Expansion | +30% radius | — | KEEP |
| Hollow Point | 35% WD above 65% hp | +21 | KEEP, moved earlier |
| Echo Shard (grenade) | second grenade | — | KEEP |
| Witchmail | spirit resist, cooldowns | — | KEEP |
| Colossus | 15% WD, +25% base health | +9 | KEEP |
| Glass Cannon (rich) | 80% WD | +48 | KEEP |
| Mystic Reverb (rich, grenade) | repeats 50% of 100+ hits | — | KEEP |
| Bullet Resist Shredder (swap) | 9% WD, rats' spirit hits cut bullet resist for the bullet-damage grenade | +5.4 | KEEP |

Kieran's suggestion (Close Quarters → Point Blank): CQ BaseAttackDamagePercent 0, PB 0. Both give +0 in the grenade formula, same as Long Range. Rejected on the numbers. Whether ANY range bonus applies to grenade hits at hit time is untested: scenario council/sandbox/scenarios/ratking_grenade_range_bonus.json; no council/evidence/ratking.json results exist → INCONCLUSIVE, so no range item goes in either way.

New: Extended Magazine (8%) → Titanic Magazine (14%, +8.4/detonation) for 1.6k total, vs Sharpshooter path 10% for 3.2k total. Hollow Point moved to right after Fortitude.
- Gun 4.8k at 4.8k souls (was 5.6k), health 4.8k at 11.2k (was 12.8k), gun 8k exactly at 14.4k, core 43.2k (was 44.8k), 12 slots.
- Weapon Damage % at 6.4k souls: 88 (Ti 14 + Cultist 10 + BV 18 + inv 46) vs 74 old (SS 10 + Cultist 10 + inv 54). At 14.4k: 139 vs 92. Late (25.6k): 139 vs 147 old (old has 1.6k more souls in gun).

Tools: walk1 FLAGS none; check.js only the pre-existing Bullet Resist Shredder colour-swap line (BV 1.6k health → 1.6k spirit; health still reaches 4.8k on Fortitude at 11.2k: SB 800 + ES 800 + EH 800 + Fortitude 2400). sp.js 1131234133444222: no threshold items in core; Mystic Reverb (rich) unchanged.
