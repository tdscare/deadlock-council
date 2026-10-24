# holliday: Rizuhble's Yeehaw Headshots (Gun Holliday)

Cost-efficiency audit. Verdict: **3 flags**

walk1 flags: none. 4.8k invest crossings (souls spent): gun @5600, spirit @18400, health @12000. Core ends 46400 souls, 12 slots.

## Swap / Instead-of / sell-for boxes (re-walked)
- Swap for Bullet Resist Shredder -> Ballistic Enchantment (WeaponMod T3, 3200, no Mystic Expansion owned so full price). Walked: Shredder 1600 spirit out, 3200 gun in. Spirit invest tops out at 3200, so spirit 4.8k (@18.4k in the base) is never hit; gun unchanged (4.8k @5.6k, 8k @15.2k); health 4.8k @12.0k; core ends 48000 (+1600). FLAG.
- Counters box sells Rapid Recharge: spirit 4800 -> 1600. FLAG.
- Rich Crippling Headshot<-Bullet Resist Shredder: spirit 4800 -> 3200. FLAG. Other rich sells fine (Siphon Bullets<-Stamina Mastery, Inhibitor<-Fortitude, Spellslinger<-Swift Striker, Mercurial Magnum<-Titanic Magazine).

## Flags
- FLAG swap breaks the spirit 4.8k and costs 1600 more.
- FLAG counters desc sells Rapid Recharge (the item that makes spirit 4.8k).
- FLAG rich Crippling Headshot sells Bullet Resist Shredder (spirit 4.8k breaks).
- WATCH Sharpshooter is 3 separate buys (Long Range 15.2k, High-Velocity Rounds 19.2k, Sharpshooter 20.0k) for 10% weapon damage on 3200 (3.1 per 1000, lowest damage per soul in the build); others buy it at 3.2k-16.0k.

## Proposed fix
- Swap box: "Ballistic Enchantment instead of Sharpshooter" (skip Long Range and High-Velocity Rounds, 1600+800+800 = 3200 = Ballistic). Walked: spirit 4.8k @16.8k (was 18.4k), gun 4.8k @5.6k, gun 8k @20.0k (was 15.2k), health 4.8k @12.0k, core ends 46400 (equal), FLAGS none. Replaces three buys, so the box description must say so.
- Counters: sell Stamina Mastery (vitality to vitality, health stays 12800); use Sharpshooter as the "get after" item.
- Rich Crippling Headshot: sell Sharpshooter (gun item, gun invest stays 25600) instead of Bullet Resist Shredder; Swift Striker and Titanic Magazine are already taken by Spellslinger and Mercurial Magnum.

## Items in buy order
Invest column = gun/spirit/health souls spent after the buy. Stats are per 1000 souls of the item's full price. "Other builds" = same item elsewhere in data.js (souls at purchase from the walk).

| # | Item (box) | Price | Souls after | Invest g/s/h | Stats per 1000 | Other builds | Verdict |
|---|---|---|---|---|---|---|---|
| 1 | Headshot Booster (Early) | 800 | 800 | 800/0/0 | HP 37.5 | 9 builds, 800-15200, med 1600 | OK |
| 2 | Extra Charge (Early) | 800 | 1600 | 800/800/0 | effect only | 31 builds, 800-28000, med 2400 | OK - idle 16.8k souls until Rapid Recharge (18.4k); Powder Keg has 2 charges |
| 3 | Extended Magazine (Early) | 800 | 2400 | 1600/800/0 | weapon dmg % 10.0, clip % 37.5 | 10 builds, 800-18400, med 3200 | OK |
| 4 | Titanic Magazine (Early) | 1600 (net 800) | 3200 | 2400/800/0 | weapon dmg % 8.8, clip % 62.5 | 10 builds, 2400-25600, med 4800 | OK - upgrade; named sell for Mercurial Magnum (rich) |
| 5 | Headhunter (Early) | 3200 (net 2400) | 5600 | 4800/800/0 | HP 15.6, weapon dmg % 1.6, move m/s 0.5 | 8 builds, 4800-23200, med 8000 | OK - upgrade of Headshot Booster |
| 6 | Extra Health (Early) | 800 | 6400 | 4800/800/800 | HP 262.5 | 20 builds, 1600-35200, med 8800 | OK |
| 7 | Rapid Rounds (Early) | 800 | 7200 | 5600/800/800 | fire rate % 11.3 | 19 builds, 800-16000, med 2400 | OK |
| 8 | Swift Striker (Early) | 1600 (net 800) | 8000 | 6400/800/800 | fire rate % 12.5, sprint m/s 0.5 | 15 builds, 3200-16800, med 4800 | OK - upgrade; named sell for Spellslinger (rich) |
| 9 | Fortitude (Mid) | 3200 (net 2400) | 10400 | 6400/800/3200 | HP 117.2, move m/s 0.5 | 20 builds, 8000-43200, med 12800 | OK - Holliday is on Kieran's roamer list; health 4.8k @12.0k |
| 10 | Bullet Lifesteal (Mid) | 1600 | 12000 | 6400/800/4800 | HP 56.3, weapon dmg % 3.8, bullet LS % 8.1 | 13 builds, 7200-27200, med 9600 | OK |
| 11 | Bullet Resist Shredder (Mid) | 1600 | 13600 | 6400/2400/4800 | weapon dmg % 5.6, bullet resist 5.6 | 10 builds, 3200-19200, med 14400 | OK - holds spirit at 1600 of the 4.8k; neither the swap nor the rich sell may remove it without a spirit replacement |
| 12 | Long Range (Mid) | 1600 | 15200 | 8000/2400/4800 | sprint m/s 0.5 | 5 builds, 2400-14400, med 5600 | WATCH - 15.2k, 4.8k souls before Sharpshooter |
| 13 | Extra Stamina (Mid) | 800 | 16000 | 8000/2400/5600 | stamina 1.3 | 20 builds, 800-20000, med 4800 | OK |
| 14 | Rapid Recharge (Mid) | 3200 (net 2400) | 18400 | 8000/4800/5600 | effect only | 30 builds, 5600-49600, med 18400 | OK - upgrade of Extra Charge; it is what puts spirit at 4.8k (@18.4k). Counters must not sell it |
| 15 | High-Velocity Rounds (Mid) | 800 | 19200 | 8800/4800/5600 | weapon dmg % 10.0 | 24 builds, 800-17600, med 800 | WATCH - T1 at 19.2k, only as Sharpshooter component (others 0.8k-17.6k) |
| 16 | Sharpshooter (Mid) | 3200 (net 800) | 20000 | 9600/4800/5600 | weapon dmg % 3.1, sprint m/s 0.3 | 6 builds, 3200-16000, med 15200 | WATCH - 3.1 weapon dmg %/1000 (lowest in build); 20.0k vs 3.2k-16.0k elsewhere (n=6) |
| 17 | Stamina Mastery (Mid) | 3200 (net 2400) | 22400 | 9600/4800/8000 | stamina 0.6 | 16 builds, 8800-36800, med 12800 | OK - upgrade of Extra Stamina |
| 18 | Lucky Shot (Late) | 6400 | 28800 | 16000/4800/8000 | clip % 4.7 | 10 builds, 30400-54400, med 37600 | OK |
| 19 | Glass Cannon (Late) | 6400 | 35200 | 22400/4800/8000 | weapon dmg % 12.5 | 2 builds, 31200-44800, med 44800 | OK - 35.2k, after Swift Striker/magazines |
| 20 | Vampiric Burst (Late) | 6400 (net 4800) | 40000 | 22400/4800/12800 | HP 15.6, weapon dmg % 0.9, bullet resist 1.6, bullet LS % 2.0 | 11 builds, 24800-41600, med 31200 | OK - upgrade of Bullet Lifesteal |
| 21 | Ricochet (Late) | 6400 | 46400 | 28800/4800/12800 | fire rate % 2.8 | 13 builds, 14400-56000, med 44800 | OK |
