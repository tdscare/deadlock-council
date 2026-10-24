# Game data 6801 -> 6819 (verified)

## Build facts
- PC install: F:\SteamLibrary\steamapps\common\Deadlock\game\citadel\steam.inf (read-only stage) = ClientVersion/ServerVersion 6819, SourceRevision 11162696, Oct 22 2026 16:40:35. pak01_dir.vpk is packed (no extracted vdata on PC).
- gt/repo working tree = 6801 (37f9aeb, Oct 20). `git fetch` worked; origin/master 17462b2 = "6819" (Oct 22 23:53). Its steam.inf is byte-identical in version/SourceRevision/date to the PC file, so 17462b2 IS the installed build. Working tree NOT modified; 6819 files exported to gt6819/ (5 files).
- Per scope correction: build number is not evidence of staleness. Only data differences count.

## Full 6801 -> 6819 diff of game data (everything that changed)
heroes.vdata: NO change. citadel_gc_mod_names: NO change. Item/ability data: abilities.vdata, 3 hunks only:
1. Warden "Last Stand" (modifier_warden_riot_protocol + cast_delay): added MODIFIER_STATE_FEAR_IMMUNE. Text: "Immune to fear while Last Stand is active." (ability_warden_riot_protocol_desc).
2. Violet "Living Ink" (ability_artist_pullbrush): new m_flMinStrokeDistance = 15.0 (minimum drawn stroke length; drawing UX/hit detail, no damage/cooldown/scaling change).
3. Item text only: Spiritual Overflow "when shooting enemy heroes" -> "heroes"; Escalating Resilience "hits an enemy hero" -> "hits a hero". No stat/cost/tier/component/disabled change in any item.
Other changes in the commit range: client/server strings, Nurse VO soundevents, one protobuf field removed, schema headers (Doorman_Doorway, Modifier_ItemWalkBack, Artist_PullBrush) - no build impact. No new/removed/disabled items (194 items both builds, 18 disabled both). Dispel Magic, Echo Shard, Vortex Web, Indomitable: unchanged stats and text.

## Affected builds (only these)
- warden: Last Stand fear immunity (text/mechanic bonus; no numbers). Check the build's Last Stand notes/any "fear" claim only; nothing in data.js mentions fear.
- violet, violet_spirit: Living Ink min stroke distance 15 - no stat change; no revisit needed beyond optional note.
- Spiritual Overflow wording (22 builds: danny_gun, greytalon, greytalon_gun, infernus, infernus_dash, haze, seven_gun, victor_gun, violet, violet_spirit, wraith, yamato, vindicta, vindicta_sniper, mcginnis, celeste, celeste_carry, baba, warden, vyper, graves, nurse) and Escalating Resilience wording (mcginnis, graves_tank): text only. "Heroes" vs "enemy heroes" may indicate it also procs on allied heroes (unconfirmed; not a numeric change).
- Tests: none need rerunning. Recommendation: NO replacement of items_full.json / levels.json / hero tables; keep 6801 files as validated.

## Existing live files vs current data
- audit/items_full.json (Oct 18) vs 6801 regen: identical except Majestic Leap has 8 extra sound-only stat keys (VelocityPitch/Vol, etc.) in live; irrelevant. vs 6819: only the two wording changes above.
- audit/heroes_full.json (Oct 18) vs 6801 regen: two ability description wording changes (Living Ink t1 "Max Draw Distance", Viscous Goo Grenade t3 "Bounce"); 6801 regen == 6819 regen exactly. No stat differences.
- a7/levels.json: level/gold table, not in any changed file; unchanged.

## Price evidence
- Game files contain only tier (m_iItemTier = EModTier_1..5; tierN_base), no cost/price field (grep of abilities.vdata/heroes.vdata: no ItemCost/Price; only m_nAbilityPointsCost/m_nAbillityUnlocksCost for ability unlocks). heroes.vdata m_MapModCostBonuses has gold thresholds 800/1600/... but is a per-souls-spent bonus table, not prices. So prices cannot be verified from files.
- Best source: deadlock.wiki/Shop (fetched): "4 tiers based on price: 800, 1,600, 3,200 and 6,400". Evidence level: secondary (community wiki, web), not game data; no price change reported. Treat 800/1600/3200/6400 as confirmed-secondary. Tier 5 (EModTier_5) exists in files; no price source for it.

## New files (6801 files untouched; nothing live overwritten)
- audit/items_full_6819.json (194 items; extra field `text_extra` = active/passive/alt localization keys). 13 of the 29 text-less used items now have text, including Dispel Magic, Echo Shard, Vortex Web, Indomitable (keys: <class>_active, _active_desc, and `upgrade_upgrade_auto_cleanse_desc` typo key). 16 stay without text because the game has no description (pure stat items: Extended Magazine, High-Velocity Rounds, Bullet Lifesteal, Sprint Boots, Rapid Rounds, Extra Stamina, Extra Spirit, Improved Spirit, Spirit Lifesteal, Mystic Reverb, Rapid Recharge, Cheat Death, Boundless Spirit, Extra Regen, Swift Striker, Titanic Magazine).
- audit/heroes_full_6819.json
- audit/gen6819/: extract_6819.py, extract_6801.py (regen), fill_text.py, items_6801_regen.json, heroes_6801_regen.json
- gt6819/game/citadel/... (the 5 source files at 6819)
- a7/levels.json not regenerated (unchanged).

## Switch plan (minimal, only if wanted)
1. Do not replace anything. For the text gap, read `text_extra` from items_full_6819.json additively (`desc || text_extra`) in whatever consumes items_full.json; stats identical.
2. Optional: update 2 wording strings (Spiritual Overflow, Escalating Resilience) and Warden Last Stand fear-immunity note in build notes; no sim/numeric rerun.
