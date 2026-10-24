# Blind review, duo batch 2 (reviewer, 2026-10-22)

Sources: game files build 6795 (`audit_D_q.py`, `ab.py`, abilities.vdata, citadel_mods_english.txt), RULES_KIERAN.md, CHECKLIST.md, base builds from data.js (diffed with rv2/diff.js), then designs_batch2.json (read last). No sandbox results exist, so every partner claim is untested.
Tools: walk1 FLAGS none on all 6. check.js CHECK12 none on 5; haze_duo_victor shows only the two colour-swap lines it already had in the base (Surge of Power, Spiritual Overflow). sp.js checked on victor, rem, abrams, seven.

## Shared mechanics (verified)
- **Bullet Resist Shredder**: "Reduces Bullet Resist on enemies when you deal [SpiritDamage]". BulletArmorReduction -10 (MODIFIER_VALUE_BULLET_AND_MELEE_RESIST_REDUCTION), AbilityDuration 8 (scales with ETechDuration), no proc cooldown. It is a debuff on the enemy, so ally bullets get it too. -10 resist means **+10%** damage on a target with 0 resist; "+11%" in the changes is only right against a target with about 9% resist. Not player-facing, just imprecise.
- **Spirit Shredder**: "Your bullets apply a debuff that reduces the Spirit Resist of the target and grants you and your allies Spirit Lifesteal against them." -8 spirit resist, 8s, 10% lifesteal for allies too. Ally spirit damage benefits: VERIFIED from the text.
- **Spirit Rend** (upgrade_spellslinger_headshots): base -8, plus -7 per **headshot** stack, up to 4 stacks, ProcCooldown 2, 8s. That is up to -36 = "~36%" (right for 0 resist). Keeping 4 stacks needs a headshot at least every 2s: UNTESTED.
- **Victor's aura shred**: Aura of Suffering does SpiritDPS (loc text). Its own tiers are T1 slow, T2 +6 min / +34 max DPS, T3 +1m radius and **+15% damage taken** (IncomingDamagePercent), which is damage amp, not bullet shred. So the -10% bullet shred comes **only from the Bullet Resist Shredder item**, procced by aura ticks (TickRate 0.25, 8m, 9m at T3, then x1.2 Mystic Expansion and x1.3 Greater Expansion, both imbued on the aura).
- **Tag Along**: "You can use items and all self-casts target your ally instead." VERIFIED (text). AbilityDuration 5.5. T2 (Rem point 6) gives BonusItemDurationPercent 35, BonusItemRangePercent 35, BonusBarrierAmpPercent 35. Scourge has ALLOW_SELF_CAST and targets CITADEL_UNIT_TARGET_HERO_FRIENDLY at 35m, so Rem could also just target Abrams. The nap only adds the +35%.
- **Two Scourges**: modifier_discord_aura with m_bDurationExtendible = true. Whether two casters stack or refresh: UNVERIFIABLE from files (H-B2-2.2).
- **Seven's coverage**: Power Surge chains (ChainCount 4, ChainRadius 10m, cd 50, 32 at T1, 10s, 20s at T3), Lightning Ball (ShockRadius 4.25m, 6m at T3, 2 charges at T1), Static Charge (5m, 7m at T2). **Storm Cloud AbilityCooldown 205** (30m, 7s channel, 14s at T2). Holliday plays beyond 15m (Long Range / Sharpshooter MinRange 15m). Whether Seven's spirit hits cover her targets is UNVERIFIABLE (H-B2-3.1). It is likely in teamfights, not in picks.

---

## Pair B2-1 Victor + Haze: KEEP (sandbox H-B2-1.1–1.4 still owed)

### victor_duo_haze: KEEP
Delta vs `victor`: +Bullet Resist Shredder (12.8k), -Witchmail, Compress Cooldown moved to its own box (buy order unchanged).
- Bullet Resist Shredder (Mid), why not Hunter's Aura (15m, -10%, doubled to -20% vs one hero, -15% fire rate, no proc needed)? Hunter's Aura costs 3200 and is weapon spend. BRS costs 1600, counts as spirit spend (spirit 8k at buy) and gives +9% weapon / +9% bullet resist. The aura keeps it on everyone within 9–12m at 80% uptime (8s on, 2s cd, and the 8s debuff covers the gap, so it never drops). OK.
- Note "For Haze: your aura keeps it on everyone near you.": true. It is a duo interaction, an allowed note kind. OK.
- Witchmail out, why not Torment Pulse or Spirit Burn? Torment Pulse is the early damage (25+0.23 SP to 2 enemies, 9m) plus 18% melee resist. Spirit resist stays covered by Scourge self-cast (TechResist 40) and Spirit Resilience in Counters. Health spike still at 9.6k (walk1). Late health is lower (17.6k) but the fighty-hero rule only asks for the early spike. OK.
- Unchanged core items (Extra Regen→Healing Booster, Extra/Improved Spirit→Boundless, Torment Pulse, Spirit Lifesteal→Infuser, Sprint Boots→Enduring Speed→Juggernaut, Mystic Vulnerability→Escalating Exposure, Mystic Expansion→Greater Expansion on 3, Compress→Superior Cooldown on 2, Warp Stone, Scourge, Spirit Burn): all the same as the live base build. Each was challenged against its stats. Spirit Burn: aura 58+34+0.72×162.5 = 209 DPS at 49.6k, over 500 in 5s. Escalating Exposure: aura ticks 0.25s against ProcCooldown 0.7. OK.
- A Kit fit OK · B same-style: base unchanged, BRS on kit numbers · C imbues 3/2 OK · D Spirit Burn OK · E spirit 4.8k @5.6k, health @9.6k OK · F 12 slots, ≤8/box OK · G counters desc same format as the 81 live builds, Divine Barrier as Dispel Magic upgrade OK · H n/a · I notes true (Refresher resets Shocking Reanimation's 240s cd: "Reset the cooldown of all your abilities") OK · J order 3312341312214424, aura T3 at point 8, same as base OK · K name "Aura Shredder Victor" (31 chars, says the playstyle), desc "Duo Victor for Haze" OK · L spirit aura brawler OK.

### haze_duo_victor: KEEP
Delta vs `haze`: +Spirit Shredder (24k), Silencer→Spirit Rend (upgrade, 44.8k), Phantom Strike swap removed, Inhibitor now sells Lucky Shot.
- Spirit Shredder (Mid), why not Mystic Vulnerability? MV needs Haze's own spirit damage, and she has almost none. Spirit Shredder is applied by bullets, so Victor's aura (about 162 DPS max at 12.8k) does +8% on her target and he gets 10% lifesteal from it. Ricochet carries it to 2 more targets ("applying any bullet procs"). Bought at 24k, so it is not a late T2, and it is upgraded later. OK.
- Spirit Rend (Late), why not keep Silencer (2.5s silence, -25% spirit damage dealt by the target, 12% spirit resist)? Silencer protects both of them, but Rend costs +1600 against Silencer's 6400 and gives up to -36% on her target for Victor. Fixation gives 3 stacks per headshot, so Haze players aim for heads anyway. Whether she keeps up one headshot per 2s, especially in Bullet Dance, is UNTESTED (H-B2-1.2). If it fails, Rend is only Shredder plus 75 HP and Silencer should come back. OK, pending sandbox.
- Note "For Victor: his aura hurts more on whoever you shoot.": true (verified from the text). OK.
- Inhibitor sells Lucky Shot, why not Burst Fire? Burst Fire is already sold for Crippling Headshot. Rich box, 45+ min. Acceptable. OK.
- Unchanged items, lowercase notes and order 3311234222341144: same as Kieran's in-game base. OK.
- A–L: A OK (Shredder/Rend are bullet-applied) · D n/a · E gun @4.8k, health @16k, same as base, Haze is mobile OK · F/G OK · I notes true · J same as base · K "Brawl Buddy Haze" OK · L tanky healer kept OK.

---

## Pair B2-2 Rem + Abrams: DROP as a pair (Rem side KEEP, Abrams side FAIL). Bar (2) "both builds change" fails once the Abrams swap is reverted.

### rem_duo_abrams: KEEP
Delta vs `rem`: Heroic Aura→Scourge (core, 37.6k, sells Opening Rounds), Rescue Beam swap and "3+ gun heroes" box removed.
- Scourge (Late), why not keep Heroic Aura? Heroic Aura is a team item (17% bullet resist, +26% fire rate, 35m), and the changes line "does nothing for a spirit tank" is **false**: Abrams gets the 17% bullet resist. Even so, Scourge relayed through the nap is much bigger. Uptime 13.5/35 = 39% (Rem 10s ×1.35 = 13.5 checked). Damage is (2.3 + 0.0055×190)% = 3.35% of max HP per second to every enemy within 10m of Abrams, about 45% per cast, plus 40% spirit resist and 20% debuff resist on Abrams. OK (the changes line should be corrected).
- Scourge note "Self-cast it while napping on Abrams: it lands on him and lasts longer.": true per the Tag Along text and T2 (+35% item duration). Bought at 37.6k, when Tag Along is already T3 (sp.js). OK.
- Divine Barrier note: true (600 ×1.35 = 810, BonusBarrierAmpPercent 35). OK.
- Unchanged items: same as base. Inherited issue, not caused by the duo change: Transcendent Cooldown and Healing Tempo sit in the rich box, but Kieran's rule lists both as Slot-locked items. Fix in base `rem` too.
- A–L: D Mystic Burst/Tankbuster unchanged from base · E spirit @8k, health @11.2k OK · F 12 slots (needs the Opening Rounds sell, which is named) · G OK · I OK · J 2211324324344311, Tag Along T2 at point 6 OK · K "Tank Rider Rem" OK · L support OK.

### abrams_duo_rem: FAIL, REVISE (revert to base Scourge)
Delta vs `abrams`: Scourge→Spirit Burn (35.2k).
- **FAIL (B/H, the claim is refuted by the numbers)**: "his own copy is a wasted 6400". Abrams owns Superior Duration from 16.8k (+28% ability and item duration), so his own Scourge lasts **12.8s, not 10s** (AbilityDuration scales with ETechDuration). designs_batch2's "~+40% per cast" compares against 10s. Real: Rem 13.5s × 3.35% ≈ 45% against Abrams 12.8s × (2.3 + 0.0055×168 = 3.22)% ≈ 41%, so **about +10%**. Even if two Scourges only refresh, taking turns (his, then Rem's) gives 26.3s of 35s = **75% uptime against 39%** with Rem's alone. If they stack it is better still. Keeping his copy wins either way. The author's "keep it only if they stack" has the logic backwards.
- **FAIL (L, tank)**: removing Scourge also removes his only late spirit resist besides Witchmail (TechResist 40), plus 20% debuff resist and the debuff reduction on a "Tanky Abrams".
- Spirit Burn, why core? -70% healing for 8s on a 20s per-target lockout (40% uptime). Healbane (-35%, kept on by Siphon ticks) already does that job in core. The threshold is met (Siphon T3 40 + 0.72×168 = 161 DPS ×6s = 966 > 500), but it is a second anti-heal in place of a tank item.
- Inherited issue, not caused by the duo change: order 3311214221444332 (base Round 25) maxes Siphon (his 1) at point 10 and the ult at point 13. That goes against Kieran's "Abrams: ult maxed much earlier than last; his 1 low priority". Re-check the live `abrams` build.
- Fix: put Scourge back (same slot) and Spirit Burn back in the rich box. That leaves Abrams with no partner-only change, so the pair fails bar (2). Drop the pair, or find a real Abrams change. Rem's Scourge-in-core can stand alone as a Rem tweak.

---

## Pair B2-3 Seven + Holliday: REVISE (2 FAILs)

### seven_duo_holliday: FAIL, REVISE (note)
Delta vs `seven`: +Bullet Resist Shredder (16k), -Diviner's Kevlar, Mystic Expansion moved to Late (buy order unchanged).
- Bullet Resist Shredder (Mid), why not Hunter's Aura? Seven's damage is AoE spirit at mid range. Power Surge late (cd about 26s after Compress/Superior Cooldown, 20s+ duration) chains to 4 enemies within 10m on every burst. BRS gives near-permanent -10% on his targets at 1600, as spirit spend. OK.
- **FAIL (I, the note is not true)**: "For Holliday: your balls and storm keep it on all of them." Storm Cloud cd is 205s, so the storm almost never keeps anything up. The balls hit only what is in a 4.25–6m path. The reliable source is Power Surge chains, and they hit at most 4 nearby targets, not "all of them". Suggested: "For Holliday: your spirit damage lowers their bullet resist."
- Diviner's Kevlar out, why not Healbane or Cultist? Healbane is part of the health spike (4.8k @12.8k). Cultist is Kieran's farm item. Kevlar's +40 SP for 20s adds only +24 storm DPS on a 205s cd. Losing its 1000 barrier makes Unstoppable the only ult guard, which is acceptable. OK.
- A–L: E spirit @5.6k, health @12.8k OK · F/G OK · J 3311234442431122, same as base, Power Surge T3 OK · K "Shred Storm Seven" OK.

### holliday_duo_seven: FAIL, REVISE (rich note)
Delta vs `holliday`: Bullet Resist Shredder→Spirit Shredder (13.6k), +Spirit Rend (30.4k), Ballistic Enchantment swap removed, Crippling Headshot sells Spirit Rend.
- Spirit Shredder in place of her own BRS, why give up her Keg-procced shred (6m, 3 charges)? The swap only works if Seven's spirit hits cover her targets (H-B2-3.1). Seven's sources reach 10m around his target and she plays beyond 15m. Likely fine in teamfights, not in picks. UNVERIFIABLE until sandbox. It is kept on that condition, not as a FAIL.
- Spirit Rend: a headshot build (Headshot Booster→Headhunter), so -36% on her target is realistic for Seven. OK.
- **FAIL (G/H)**: "Crippling Headshot: Sell Spirit Rend for this", with the changes line claiming "same job, bigger". Crippling is MagicResistReduction **-16**. Spirit Rend gives **up to -36** spirit. Selling Rend undoes the duo payoff, and the rich item is no longer a pricier version of something in the build, because BRS is gone. Fix: sell another item (Swift Striker is already used by Spellslinger; Long Range is gone into Sharpshooter), or remove Crippling Headshot from this variant.
- Spirit spend now 3.2k, so the 4.8k spirit spike is gone. Fine for a gun build. OK.
- A–L: E gun @5.6k, health @12k OK · F/G except the FAIL above · J 3311234312441422, same as base · K "Shred Shot Holliday" OK.
