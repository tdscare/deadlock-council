# Cost-efficiency audit: greytalon_gun (Rizuhble's Bow Spam Grey Talon)
Core buy order walked left to right (Early, Mid, Late), upgrades counted as the difference, sells applied only where a core note says "Sell X for this". Colour = item slot in game files (Tech = spirit, Armor = health, WeaponMod = gun). 4.8k spikes before: gun@6400, spirit@17600, health@12800. End of core: 51200 souls, gun 30400 / spirit 9600 / health 11200, 12 slots.

Result: OK (gun 4.8k @6.4k, health @12.8k, spirit @17.6k); LOW Extra Spirit stepping stone 800 for 10.4k souls
Minimal fix: none required

## Per item (buy order)
Columns: souls spent when bought, souls paid for this purchase, colour+tier, stat per 1000 of full tier cost (SP spirit power incl. imbue, HP, WD% weapon damage, FR% fire rate, BR%/TR% resists), invest after buying, verdict.

| # | souls | item | paid | col | stat/1k | gun/spirit/health | verdict |
|---|---|---|---|---|---|---|---|
| 1 | 800 | High-Velocity Rounds | 800 | w1 | WD% 10.0 | 800/0/0 | OK |
| 2 | 1600 | Rapid Rounds | 800 | w1 | FR% 11.3 | 1600/0/0 | OK |
| 3 | 2400 | Extra Stamina | 800 | v1 | utility | 1600/0/800 | OK (info: bought 2400 vs median 5600 in 20 other builds, no action) |
| 4 | 3200 | Swift Striker | 800 | w2 | FR% 12.5 | 2400/0/800 | OK |
| 5 | 6400 | Hollow Point | 3200 | w3 | HP 39 WD% 10.9 | 5600/0/800 | OK: 6.4k, 3200: BaseAttackDamage 35%, 125 hp, gun 4.8k lands (ratio 0.28 vs median 23.2k: this is the spike race). [vs 5 other builds: median 23200, min 16000 venator_grenade, max 27200 sinclair] |
| 6 | 7200 | Extra Spirit | 800 | s1 | SP 12.5 | 5600/800/800 | FLAG LOW: 800 @7.2k, only used by Surge of Power @17.6k; 12.5 SP/1k meanwhile. [vs 42 other builds: median 1600, min 800 infernus, max 19200 baba_tank] |
| 7 | 8800 | Quicksilver Reload | 1600 | s2 | FR% 6.3 | 5600/2400/800 | OK |
| 8 | 9600 | Sprint Boots | 800 | v1 | utility | 5600/2400/1600 | OK |
| 9 | 10400 | Enduring Speed | 800 | v2 | utility | 5600/2400/2400 | OK |
| 10 | 12800 | Stamina Mastery | 2400 | v3 | utility | 5600/2400/4800 | OK |
| 11 | 14400 | Long Range | 1600 | w2 | utility | 7200/2400/4800 | OK (info: bought 14400 vs median 5600 in 5 other builds, no action) |
| 12 | 15200 | Sharpshooter | 800 | w3 | WD% 3.1 | 8000/2400/4800 | OK |
| 13 | 17600 | Surge of Power | 2400 | s3 | SP 8.8 | 8000/4800/4800 | OK |
| 14 | 19200 | Bullet Lifesteal | 1600 | v2 | HP 56 WD% 3.8 | 8000/4800/6400 | OK: 19.2k, 1600, consumed by Vampiric Burst @40.0k (paid 4800). [vs 13 other builds: median 9600, min 7200 vindicta, max 27200 haze] |
| 15 | 20800 | Spirit Lifesteal | 1600 | v2 | SP 3.8 HP 56 | 8000/4800/8000 | OK: 20.8k, 1600, consumed by Spiritual Overflow @51.2k (paid 4800). [vs 31 other builds: median 12800, min 4800 paradox_bomb, max 24000 celeste_carry] |
| 16 | 24000 | Burst Fire | 3200 | w3 | FR% 3.1 | 11200/4800/8000 | OK |
| 17 | 28800 | Mercurial Magnum | 4800 | s4 | SP 1.1 FR% 3.4 | 11200/9600/8000 | OK |
| 18 | 35200 | Lucky Shot | 6400 | w4 | utility | 17600/9600/8000 | OK |
| 19 | 40000 | Vampiric Burst | 4800 | v4 | HP 16 WD% 0.9 BR% 1.6 | 17600/9600/12800 | OK |
| 20 | 46400 | Ricochet | 6400 | w4 | FR% 2.8 | 24000/9600/12800 | OK |
| 21 | 51200 | Spiritual Overflow | 4800 | w4 | SP 5.6 HP 14 FR% 3.9 | 30400/9600/11200 | OK |

## Swap / "Instead of" boxes re-walked
No swap or "instead of" box in this build besides notes already covered above (a lost-lane reorder box, if present, is walked under Reorders).

## Sells in counters / rich / slot-locked boxes (effect on spike totals)
End-of-core invest: gun 30400, spirit 9600, health 11200. Only sells that cross 4.8k/6.4k/8k/16k downward are listed.
- none cross a threshold

## Other findings
- 6.4k items: Lucky Shot 35.2k, Ricochet 46.4k only after 30k: fine.
- Mercurial Magnum is Tech slot: counted as spirit by the game.
- Gun / spirit / health 4.8k: gun @6400, spirit @17600, health @12800.
- walk1.js FLAGS: none (checked on the base build). Public same-style builds were not re-fetched in this pass; comparison is against the other 80 data.js builds (core buy-souls).
