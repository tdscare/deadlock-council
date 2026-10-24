# Victor gun-only lifesteal, first real in-game data (2026-10-23, build 6819)
Setup: Victor (Frank) level-max, 50k souls, shooting an enemy Haze bot 350u away on dl_midtown, 8 s of continuous fire per item, hurt to ~80% first. Raw: damage_20261023_132455.csv / samples_victor_lifesteal_132502.csv.

| item | dmg/s | heal/s (incl ~4.5 regen) | heal as % of damage dealt |
|---|---|---|---|
| none | 128.6 | 4.5 | 4% (regen only) |
| Bullet Lifesteal (upgrade_vampire) | 138.7 | 22.4 | 16% (13% item + regen) |
| Leech (upgrade_damage_recycler) | 145.4 | 45.4 | 31% (28% item + regen) |
| Vampiric Burst (upgrade_surging_power), activated | 155.1 | 57.9 | 37% |
| Infuser | 113.5 | 5.1 | none - spirit lifesteal only, needs ability damage |
| Spirit Lifesteal | 124.9 | 5.1 | none - same |

Validation: measured lifesteal matches item stats (13%, 28%). Not yet tested: spirit-damage items with Victor's abilities, a mixed gun+ability rotation, the 5 s active window uptime over a long fight.
Caveats: single enemy, constant 350u range (no falloff), heal includes regen, aim offset calibrated by hand (yaw +5.5, pitch +3).
