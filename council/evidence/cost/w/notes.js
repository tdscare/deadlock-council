// manual findings per build. sev: HIGH = a 4.8k spike never lands / is lost, MED = spike or big item >4k souls off, or slot/cost break; LOW = small.
module.exports={
danny:{
 sum:{flags:"MED Sharpshooter @16.0k = gun 4.8k lands 4th (his rule: HV>Opening Rounds>Sharpshooter); MED every counter + Mystic Reverb sells Opening Rounds (gun 4.8k>3.2k); LOW Surge of Power @24.0k after Greater Expansion; LOW Stamina Mastery 2400 for 0 hp",
  fix:"Sharpshooter right after Opening Rounds (gun 4.8k @4.8k, spirit 4.8k 8.0k>11.2k, health 12.8k>16.0k); counters/Reverb sell Enchanter's Emblem or Extra Stamina line, not Opening Rounds; Surge of Power before Greater Expansion"},
 items:{
  'Sharpshooter':['MED','Bought 4th-last of the mid items at 16.0k; gun 4.8k only lands here (800 and 1.6k steps idle for 14k souls). Danny rule: keep HV>Opening Rounds>Sharpshooter (in-game build). Fix A (rule order): move right after Opening Rounds = gun 4.8k @4.8k. Fix B (compromise): after Compress Cooldown = gun @11.2k, health @16.0k.'],
  'Opening Rounds':['MED','Counters desc and Mystic Reverb note sell this: gun invest 4800>3200, the 4.8k spike is lost the moment the counter is bought. Sell Enchanter\'s Emblem (health 17.6k>16.0k, no spike crossed) or Reactive Barrier instead.'],
  'Surge of Power':['LOW','24.0k after Tankbuster (18.4k) and Greater Expansion (20.8k, 0 spirit power, TechResist 10). SoP = ImbuedTechPower 28 for 3200 = 8.8 SP/1k plus 20% fire rate; Greater Expansion gives none. Move SoP before Greater Expansion: no spike moves (tested).'],
  'Stamina Mastery':['LOW','2400 souls for 0 hp (Stamina 2, air move 23%). It is what pushes health to 4.8k @12.8k. Extra Health (800, 210 hp) then Fortitude would give 585 hp for 3200. Rich Focus Lens also sells it: health 17.6k>14.4k (loses the 16k step); sell Reactive Barrier line instead. Judgement call otherwise.'],
 },
 swaps:[],
 fixes:[
  {t:'Fix A (rule order): Sharpshooter after Opening Rounds',ops:['mv:Sharpshooter>after:Opening Rounds']},
  {t:'Fix B (compromise) + Surge of Power before Greater Expansion',ops:['mv:Sharpshooter>after:Compress Cooldown','mv:Surge of Power>before:Greater Expansion']},
 ],
 find:['Mystic Burst @4.0k: OK, Chimera explosion 70+1.5xSP = 125 at SP 36.8 (>80). Tankbuster @18.4k: Chimera 70+1.5x110 = 235 (>165). Thresholds were already checked in a7; only these two re-derived.']
},
danny_gun:{
 sum:{flags:"LOW Spirit Shielding = T2 with no further upgrade and no named sell; otherwise OK (gun 4.8k @4.8k, health 10.4k, spirit 17.6k)",
  fix:"Name a sell for Spirit Shielding (e.g. Counters desc sells it) or swap for a pure upgrade of Grit that is in the build; no timing change needed"},
 items:{
  'Spirit Shielding':['LOW','T2 upgrade of Grit (800 paid). Nothing upgrades it (no components use it) and no box says to sell it. Rule: every T1/T2 needs an upgrade later or a named replacement.'],
  'Extra Spirit':['LOW','Stepping stone: 800 at 6.4k, only consumed by Surge of Power at 17.6k (11k souls later). 10 SP for 800 = 12.5 SP/1k meanwhile; acceptable.'],
  'Express Shot':['OK','4.0k, 2400 paid (HV consumed). Gun 4.8k lands at 4.8k with Swift Striker: fastest in my set. Earlier than other builds (median 15.2k) but it is the 4.8k race.'],
 },
 swaps:[],fixes:[],find:['Counters sell Warp Stone: no spike crossed (all colours stay above their thresholds).','Gun 8.0k reached via Toxic Bullets @15.2k before spirit 4.8k (17.6k): intended (8k is a spike step), not an overshoot.']
},
bebop:{
 sum:{flags:"LOW Fortitude @33.6k bought after two 6.4k items (2400 for 375 hp); LOW rich box sells Bullet Resist Shredder / Spirit Snatch drop spirit 4.8k to 3.2k / 1.6k",
  fix:"Fortitude right after Spirit Snatch (spikes unchanged: gun 7.2k, health 12.8k, spirit 18.4k); rich Lucky Shot/Spellslinger sell Stalker or Enduring Speed-line item instead"},
 items:{
  'Fortitude':['LOW','2400 for 375 hp (+heal out of combat) = 156 hp/1k, best hp/1k in the build, but bought 33.6k after Siphon (24.8k) and Vampiric Burst (31.2k). Other builds buy it median 12.8k (ratio 2.63). Move after Spirit Snatch: no spike changes (tested).'],
  'Bullet Resist Shredder':['LOW','Rich box Lucky Shot sells this: spirit 4.8k>3.2k. Sell Stalker (gun 14.4k>12.8k, nothing crossed) instead.'],
  'Spirit Snatch':['LOW','Rich box Spellslinger sells this: spirit 4.8k>1.6k. Sell Stalker or Siphon-line item instead.'],
  'Headhunter':['OK','7.2k, gun 4.8k lands here (damage first), health 4.8k @12.8k (Veil Walker) before Hunter\'s Aura: matches in-your-face rule.'],
 },
 swaps:[],fixes:[{t:'Fortitude after Spirit Snatch',ops:['mv:Fortitude>after:Spirit Snatch']}],
 find:['Two 6.4k in a row (Siphon 24.8k, Vampiric Burst 31.2k) is allowed (<=3 back to back).']
},
bebop_bomb:{
 sum:{flags:"MED gun 0 (no gun item at all, 4.8k never); LOW Mystic Expansion @16.8k (cheap Sticky Bomb imbue bought late)",
  fix:"No clean fix: gun 4.8k needs two slots (T3 3.2k + T2 1.6k); tested Headhunter + Opening Rounds in place of Trophy Collector + Enduring Speed = gun 4.8k @10.4k but 13 slots and health 4.8k slips to 33.6k. Recommend accept gun 0 for this pure-spirit build; Mystic Expansion next to Compress Cooldown is the only change"},
 items:{
  'Mystic Burst':['OK','First item, 800. Sticky Bomb = 85+1.5x9.2 = 99 at SP 9.2 (>80) so it procs from the start; feeds Tankbuster @16.0k (Sticky Bomb 85+1.5x99 = 234 > 165).'],
  'Mystic Expansion':['LOW','800 at 16.8k, imbue on Sticky Bomb (range/radius), then Greater Expansion @38.4k. Others buy it median 8.8k (ratio 1.9). Bought next to Compress Cooldown it costs nothing in spikes (spirit 4.8k stays @6.4k; health 4.8k 13.6k>14.4k).'],
  'Trophy Collector':['OK','4.0k, early, passive souls payoff starts at once; named sell exists (Magic Carpet).'],
  'Enduring Speed':['OK','Slow hero; upgrade Juggernaut in Slot locked.'],
 },
 swaps:[],fixes:[],find:['No gun item: gun invest 0 for the whole build. Rule "no token investments" means commit or skip, so 0 is consistent; flagged only because Kieran wants 4.8k in every colour on most heroes.','Mercurial Magnum: game slot is Tech (spirit). walk1 and the spirit invest bonus count it as spirit; only Kieran\'s own counting treats it as gun.']
},
bebop_support:{
 sum:{flags:"HIGH swap 'Knockdown instead of Heroic Aura': gun invest 3.2k, 4.8k never lands (base: gun 4.8k @19.2k with Heroic Aura + Hunter's Aura); LOW Veil Walker @24.0k",
  fix:"Swap box gets a gun item with the same job: Spirit Rend (gun T3, team spirit shred; spikes unchanged, gun @19.2k tested). Keep Knockdown only with a 1.6k gun top-up (Opening Rounds) replacing another slot"},
 items:{
  'Heroic Aura':['HIGH','Only gun T3 besides Hunter\'s Aura. Swap Knockdown (Tech, 3200, Health 75) takes gun from 6.4k to 3.2k: 4.8k never. Same walk for the base: gun 4.8k @19.2k, spirit @8.0k, health @10.4k.'],
  'Veil Walker':['LOW','24.0k, 3200 (v3, 125 hp, 6 SP) after Hunter\'s Aura and Slowing Hex. Other Bebop builds buy it 12.8k to 13.6k. It is the item that lets Bebop sneak up for the hook; at 24k that is mid-late.'],
  'Bullet Resist Shredder':['OK','3.2k, spirit 3.2k step; BulletArmorReduction -10 and +9% weapon damage for the team at 1600 = 5.6 WD%/1k.'],
  'Fortitude':['OK','10.4k, 2400 for 375 hp; health 4.8k lands here.'],
 },
 swaps:[{b:'Swap for Heroic Aura (Knockdown)',ops:['swap:Heroic Aura=Knockdown'],v:'FLAG'},
        {b:'Proposed: Spirit Rend instead of Heroic Aura',ops:['swap:Heroic Aura=Spirit Rend'],v:'OK'},
        {b:'Alternative: Knockdown + Opening Rounds (instead of Slowing Hex and Vortex Web)',ops:['swap:Heroic Aura=Knockdown','swap:Slowing Hex=Opening Rounds','swap:Vortex Web=Echo Shard'],v:'FLAG (13 slots, rejected)'}],
 fixes:[],find:['Heroic Aura is a core item conditional on gun heroes; when the condition fails the box is the swap, so the swap must keep colour totals.']
},
dynamo:{
 sum:{flags:"HIGH swap 'Knockdown instead of Heroic Aura': gun 6.4k>3.2k, 4.8k never; MED spirit 4.8k only @18.4k (gun 6.4k first) on a healer; LOW Enchanter's Emblem fresh T2 @20.0k; LOW Warp Stone/Headhunter sells cross 16k/4.8k",
  fix:"Swap box: Spirit Rend (gun T3) instead of Heroic Aura (tested, spikes unchanged); move Heroic Aura after Compress Cooldown (spirit 4.8k 18.4k>15.2k, gun 4.8k 12.8k>18.4k)"},
 items:{
  'Heroic Aura':['HIGH','Gun spike carrier: Headhunter 3.2k + Heroic Aura 3.2k. Knockdown swap leaves 3.2k. Also bought 12.8k before any spirit item: ordering below.'],
  'Rapid Recharge':['MED','Spirit block (Rapid Recharge 16.0k, Mystic Expansion 16.8k, Compress Cooldown 18.4k) starts after two gun T3 + Healing Booster. Healer scales with spirit; spirit 4.8k @18.4k. Move Heroic Aura after Compress Cooldown: spirit @15.2k, gun @18.4k (tested).'],
  "Enchanter's Emblem":['LOW','Fresh T2 at 20.0k (ratio 2.08, others median 9.6k), no upgrade, named sells exist (counter, Witchmail). Rule: late buys are T3/T4 or upgrades. TechPower 15, TechResist 18, 1600 = 9.4 SP/1k.'],
  'Warp Stone':['LOW','Counters Debuff Reducer sells this: health 16.0k>14.4k crosses 16k step.'],
  'Headhunter':['LOW','Rich Refresher sells this: gun 6.4k>3.2k (loses 4.8k and 6.4k). Sell Healing Booster instead.'],
  'Trophy Collector':['LOW','Rich Lightning Scroll sells this: health 16.0k>14.4k (loses the 16k step). Sell Duration Extender-line item instead.'],
  'Rescue Beam':['OK','5.6k, 2400 paid (Healing Rite consumed), health 4.0k, heals ally 20% max hp: pays at once for a support; 0.44 ratio is intended.'],
 },
 swaps:[{b:'Swap for Heroic Aura (Knockdown)',ops:['swap:Heroic Aura=Knockdown'],v:'FLAG'},
        {b:'Proposed: Spirit Rend instead of Heroic Aura',ops:['swap:Heroic Aura=Spirit Rend'],v:'OK'},
        {b:'Alternative: Knockdown + Opening Rounds instead of Enchanter\'s Emblem',ops:['swap:Heroic Aura=Knockdown','swap:Enchanter\'s Emblem=Opening Rounds'],v:'partial: gun 4.8k @20.0k, health 16.0k>14.4k'}],
 fixes:[{t:'Heroic Aura after Compress Cooldown',ops:['mv:Heroic Aura>after:Compress Cooldown']}],find:[]
},
dynamo_damage:{
 sum:{flags:"MED every counter and Witchmail sell Headhunter: gun 4.8k>1.6k; LOW Mystic Reverb/Boundless sell Recharging Rush drops gun to 3.2k",
  fix:"Counters/Witchmail sell Rapid Recharge (or Compress Cooldown line item) instead of Headhunter; Boundless sells Rapid Recharge"},
 items:{
  'Headhunter':['MED','Counters desc and Witchmail note sell this: gun invest 4800>1600, the 4.8k spike is gone as soon as the counter is bought. Sell Rapid Recharge (spirit 35.2k>32.8k, nothing crossed).'],
  'Recharging Rush':['OK','7.2k: Kinetic Pulse at tier 3 = 115+135+1.55x24 = 287 in one hit (>200 in 3.5s); gun 4.8k lands here. Boundless note sells it: gun 4.8k>3.2k, sell Rapid Recharge instead.'],
  'Mystic Burst':['OK','1.6k lane buy, Kinetic Pulse 115+1.55x11.4 = 133 (>80), feeds Tankbuster @13.6k (stomp tier 3: 115+135+1.55x39.9 = 312 > 165).'],
  'Warp Stone':['OK','11.2k, health 4.8k lands (v 4.8k) after gun 4.8k @7.2k; ult-gap closer, early by design.'],
  'Quicksilver Reload':['OK','16.8k, 1600 now and consumed into Mercurial Magnum @25.6k (paid 4800). Ratio 2.1 vs other builds fine.'],
 },
 swaps:[],fixes:[],find:['Spikes: gun @7.2k, health @11.2k, spirit @15.2k: damage first, then health, then spirit: matches priority rule.','Mercurial Magnum is a Tech-slot item (spirit invest). Kieran counts it as gun for his purposes; spikes here follow the game slot.']
},
greytalon:{
 sum:{flags:"LOW rich Refresher sells Sharpshooter: gun 4.8k>1.6k; LOW Superior Cooldown 1600 bought after Indomitable (33.6k->35.2k)",
  fix:"Refresher sells Enchanter's Emblem/Stamina Mastery line; Superior Cooldown before Indomitable (spikes unchanged)"},
 items:{
  'Recharging Rush':['OK','16.8k: Charged Shot 80+54+1.0x102 = 236 in one hit (>200 in 3.5s), refunds the arrow charge (17s cooldown). Slow-firing hero but ability meets the threshold; gun 4.8k lands here (named sell for a counter).'],
  'Tankbuster':['OK','12.8k: Charged Shot (T3) 80+54+1.0x99 = 233 > 165.'],
  "Enchanter's Emblem":['OK','8.0k fresh T2 dead-end but named sells (Tankbuster counter, Witchmail); 9.4 SP/1k.'],
  'Sharpshooter':['LOW','Rich Refresher sells this: gun 4.8k>1.6k. Sell Enchanter\'s Emblem instead.'],
  'High-Velocity Rounds':['OK','2.4k, 800, consumed into Sharpshooter @15.2k (Sharpshooter paid 800 after Long Range).'],
 },
 swaps:[],fixes:[{t:'Superior Cooldown before Indomitable',ops:['mv:Superior Cooldown>before:Indomitable']}],find:['Spikes: spirit @5.6k, health @10.4k, gun @16.8k. Gun items (HV, Long Range, Sharpshooter, Recharging Rush) only pay for bullets; the arrow is an ability, so the gun spike is a Kieran-rule item, not a damage item for this style.']
},
greytalon_gun:{
 sum:{flags:"OK (gun 4.8k @6.4k, health @12.8k, spirit @17.6k); LOW Extra Spirit stepping stone 800 for 10.4k souls",
  fix:"none required"},
 items:{
  'Hollow Point':['OK','6.4k, 3200: BaseAttackDamage 35%, 125 hp, gun 4.8k lands (ratio 0.28 vs median 23.2k: this is the spike race).'],
  'Extra Spirit':['LOW','800 @7.2k, only used by Surge of Power @17.6k; 12.5 SP/1k meanwhile.'],
  'Bullet Lifesteal':['OK','19.2k, 1600, consumed by Vampiric Burst @40.0k (paid 4800).'],
  'Spirit Lifesteal':['OK','20.8k, 1600, consumed by Spiritual Overflow @51.2k (paid 4800).'],
 },
 swaps:[],fixes:[],find:['6.4k items: Lucky Shot 35.2k, Ricochet 46.4k only after 30k: fine.','Mercurial Magnum is Tech slot: counted as spirit by the game.']
},
infernus:{
 sum:{flags:"MED Gun Infernus gets gun 4.8k only third (15.2k) behind spirit @5.6k and health @11.2k; LOW rich Spirit Burn sells Healbane: health 8.0k>6.4k",
  fix:"Toxic Bullets right after Extended Magazine: gun 4.8k @9.6k (was 15.2k), health 4.8k 11.2k>14.4k. Armor Piercer swap is fine (tested, same colour and price)"},
 items:{
  'Toxic Bullets':['MED','15.2k, 3200 (w3), the item that lands gun 4.8k. Build is named gun, yet first 5.6k souls are spirit (Extra Spirit, Duration Extender, Improved Spirit, Mystic Vulnerability). Move after Extended Magazine: gun @9.6k (tested).'],
  'Healbane':['LOW','Rich Spirit Burn sells this: health 8.0k>6.4k crosses the 8k step.'],
  'Swift Striker':['OK','12.0k fresh T2 (800 paid, Rapid Rounds consumed), named sell for a counter.'],
  'Armor Piercer':['OK','Swap instead of Ricochet: both w4 6400 (Armor Piercer\'s HV component not owned): spikes identical (gun @15.2k, spirit @5.6k, health @11.2k).'],
 },
 swaps:[{b:'Swap for Ricochet (Armor Piercer)',ops:['swap:Ricochet=Armor Piercer'],v:'OK'}],
 fixes:[{t:'Toxic Bullets after Extended Magazine',ops:['mv:Toxic Bullets>after:Extended Magazine']}],find:['End health only 8.0k (Bullet Lifesteal, Spirit Lifesteal, Healbane + Leech): lifesteal heavy by design.']
},
infernus_dash:{
 sum:{flags:"MED gun 4.8k only @51.2k (Spiritual Overflow, second to last) with gun 1.6k for 50k souls; LOW every counter + Lightning Scroll sell Swift Striker: gun 8.0k>6.4k",
  fix:"Spiritual Overflow before Escalating Exposure: gun 4.8k @24.0k (tested, spirit @8.8k and health @11.2k unchanged)"},
 items:{
  'Spiritual Overflow':['MED','Gun 4.8k lands here at 51.2k. Moved ahead of Escalating Exposure it lands at 24.0k (tested): gun 4.8k @24.0k, total cost unchanged (Spirit Lifesteal consumed, 4800 paid), spirit @8.8k and health @11.2k unchanged. T4 buys stay below 3 back to back.'],
  'Swift Striker':['LOW','Counters (all) and Lightning Scroll sell this: gun 8.0k>6.4k.'],
  'Sprint Boots':['OK','First item (lane speed for a dash hero), 800, Enduring Speed @11.2k.'],
  'Rapid Recharge':['OK','8.8k (Extra Charge consumed), spirit 4.8k lands here.'],
 },
 swaps:[],fixes:[{t:'Spiritual Overflow before Escalating Exposure',ops:['mv:Spiritual Overflow>before:Escalating Exposure']}],find:[]
},
kelvin:{
 sum:{flags:"INFO gun 0; LOW Infuser (T4) @20.8k earliest in data.js (others median 41.6k)",
  fix:"none required; if gun 4.8k wanted cheapest is 6 T1s or Headhunter + a T2 (needs 2 slots)"},
 items:{
  'Infuser':['LOW','20.8k, 4800 paid (Spirit Lifesteal consumed). Ratio 0.5. Kelvin beam ticks fit it (rule: lots of separate spirit hits); health 4.8k @10.4k is already online, so OK.'],
  'Torment Pulse':['OK','4.8k: 3200 = 100 hp + 18% melee resist + pulse 25+0.23xSP; spirit 4.8k lands here (tanky damage-dealer).'],
  'Healbane':['OK','10.4k fresh T2, named sell (Spirit Burn, counters).'],
 },
 swaps:[],fixes:[],find:['Spikes: spirit @4.8k, health @10.4k; end health 19.2k.','Gun invest 0 for the build.']
},
kelvin_support:{
 sum:{flags:"INFO gun 0; none else",fix:"none required"},
 items:{
  'Healing Booster':['OK','2.4k (Extra Regen consumed), healer: payoff immediate.'],
  "Enchanter's Emblem":['OK','9.6k fresh T2 with named sell for a counter; health 4.8k lands here.'],
  'Healbane':['OK','11.2k named sell for third counter.'],
  'Warp Stone':['OK','20.0k, 3200; roamer.'],
 },
 swaps:[],fixes:[],find:['Spikes: spirit @6.4k, health @9.6k. Gun invest 0.']
},
paige:{
 sum:{flags:"MED swap 'Slowing Hex instead of Mystic Burst' alone = 13 slots and +1600 souls (Tankbuster loses its Mystic Burst component); MED every counter sells Express Shot: gun 4.8k>1.6k; LOW health only 6.4k at end of core; LOW Surge of Power @24.8k",
  fix:"Merge the Slowing Hex and Vortex Web swaps into one (instead of Mystic Burst and Escalating Exposure: 12 slots, same total 40.0k, tested); counters sell Greater Expansion instead of Express Shot; Surge of Power before Guardian Ward"},
 items:{
  'Express Shot':['MED','Counters desc and Mystic Reverb note sell this: gun 4.8k>1.6k. Spirit Burn note sells Opening Rounds: 4.8k>3.2k. Sell Greater Expansion (spirit 28.8k>26.4k, nothing crossed).'],
  'Mystic Burst':['MED','Swap target. Tankbuster (2400 paid) consumes it; taking Slowing Hex instead makes Tankbuster 3200 and leaves 13 slots. Buy Slowing Hex + Vortex Web together as one swap (Hex is Vortex\'s component).'],
  'Surge of Power':['LOW','24.8k (ratio 1.94, others median 12.8k); ImbuedTechPower 28 for 3200 = 8.8 SP/1k and imbue on the dragon. Before Guardian Ward (21.6k) no spike moves.'],
  'Extra Health':['LOW','12.8k, then Fortitude 15.2k: health 4.8k only @15.2k and ends 6.4k at 40k souls: thinnest health of my 21 builds. Mobile hero, so allowed by the health-delay rule.'],
  'Trophy Collector':['LOW','9.6k with Sprint Boots 8.8k, passive souls early enough. Rich Lightning Scroll sells it: health 6.4k>4.8k loses the 6.4k step; sell Greater Expansion instead.'],
 },
 swaps:[{b:'Lots of dashers: Slowing Hex instead of Mystic Burst',ops:['swap:Mystic Burst=Slowing Hex'],v:'FLAG (13 slots, +1600)'},
        {b:'Lots of dashers: Vortex Web instead of Escalating Exposure',ops:['swap:Escalating Exposure=Vortex Web'],v:'OK'},
        {b:'Lots of dashers: Knockdown instead of Surge of Power',ops:['swap:Surge of Power=Knockdown'],v:'OK (imbue on dragon lost)'},
        {b:'Proposed merged swap: Slowing Hex+Vortex Web instead of Mystic Burst+Escalating Exposure',ops:['swap:Mystic Burst=Slowing Hex','swap:Escalating Exposure=Vortex Web'],v:'OK'}],
 fixes:[{t:'Surge of Power before Guardian Ward',ops:['mv:Surge of Power>before:Guardian Ward']}],find:[]
},
paige_support:{
 sum:{flags:"INFO gun 1.6k (HV + Opening Rounds), 4.8k never; otherwise OK (spirit @10.4k, health @12.8k)",fix:"none required"},
 items:{
  'Opening Rounds':['LOW','8.0k fresh T2 (800 paid, HV consumed), dead-end with named sells (Echo Shard, counters); gun stays 1.6k.'],
  'Rescue Beam':['OK','12.8k, 2400 paid (Healing Rite consumed), 20% heal + pull; health 4.8k lands here.'],
  'Knockdown':['OK','16.0k, 3200; named in notes; sold for Vortex Web.'],
 },
 swaps:[],fixes:[],find:['Gun invest only 1.6k: no gun T3 in the build.']
},
ratking:{
 sum:{flags:"INFO spirit 3.2k never 4.8k (grenade scales off weapon damage by design); LOW Close Quarters 800 @8.0k waits 24k souls for Point Blank",
  fix:"none required; lost-lane reorder box tested harmless"},
 items:{
  'Close Quarters':['LOW','800 @8.0k, consumed by Point Blank @32.0k (ratio 5.0). Close-range hero so +20 weapon power and 20% melee resist work meanwhile.'],
  'Cultist Sacrifice':['OK','7.2k (2400 paid): rule says strong on farm-struggling heroes ~8 min; gun 4.8k lands here.'],
  'Return Fire':['OK','16.0k conditional T2; rule: Return Fire a must for Rat King. Named condition in note.'],
  'Fleetfoot':['OK','12.8k T2 dead-end, named sell for the counter.'],
 },
 swaps:[],fixes:[{t:'Lost-lane reorder: Cultist Sacrifice right after Sprint Boots',ops:['mv:Cultist Sacrifice>after:Sprint Boots']}],find:['Spikes: gun @7.2k, health @11.2k; end gun 14.4k, health 25.6k.']
},
ratking_grenade:{
 sum:{flags:"OK; swap 'Bullet Resist Shredder instead of Battle Vest' passes (health 4.8k stays @12.8k)",fix:"none required"},
 items:{
  'Battle Vest':['OK','8.0k, v2 1600; 18% bullet resist + 18% weapon damage above 65% hp. Swap box replaces it with Bullet Resist Shredder (s2, same price): tested, gun @5.6k, health @12.8k unchanged, spirit 22.4k>19.2k.'],
  'Long Range':['OK','5.6k, 1600; consumed by Sharpshooter @6.4k (800 paid); gun 6.4k early is the point (grenade scales with weapon damage).'],
  'Cultist Sacrifice':['OK','4.0k (2400 paid).'],
 },
 swaps:[{b:'Swap for Battle Vest (Bullet Resist Shredder)',ops:['swap:Battle Vest=Bullet Resist Shredder'],v:'OK'}],fixes:[],find:['Spirit 4.8k only @22.4k, ends 12.8k: secondary colour, acceptable for a grenade-weapon build.']
},
haze:{
 sum:{flags:"INFO spirit 3.2k never 4.8k; all four swaps pass (Surge of Power for Burst Fire moves spirit 4.8k to 36.8k, others unchanged); LOW Extra Charge @28.0k fresh T1 8.8k before Rapid Recharge",
  fix:"none required"},
 items:{
  'Ricochet':['OK','14.4k, 6400 (earliest T4 in my set). Kieran-agreed in-game base (farm until Siphon). Overrides the no-6400-before-20-min guideline.'],
  'Extra Charge':['LOW','800 @28.0k (ratio 11.7), upgraded to Rapid Recharge @36.8k. Could be bought with it (same total 3200) or earlier for the charge; no spike effect (spirit 3.2k).'],
  'Healing Booster':['OK','16.0k (4.8k health spike) 1600; healer base item.'],
  'Active Reload':['OK','2.4k fresh T2 for lane, named sell for a counter; gun 4.8k @4.8k with 4 cheap gun items.'],
 },
 swaps:[{b:'Surge of Power instead of Burst Fire',ops:['swap:Burst Fire=Surge of Power'],v:'OK'},
        {b:'Leech instead of Vampiric Burst',ops:['swap:Vampiric Burst=Leech'],v:'OK'},
        {b:'Blood Tribute instead of Burst Fire',ops:['swap:Burst Fire=Blood Tribute'],v:'OK'},
        {b:'Phantom Strike instead of Silencer',ops:['swap:Silencer=Phantom Strike'],v:'OK (gun 27.2k>20.8k, still above 16k)'}],
 fixes:[],find:['Lost-lane reorder (Ricochet before Fortitude) does not move any spike (tested).']
},
haze_assassin:{
 sum:{flags:"LOW rich Crippling Headshot sells Bullet Resist Shredder: spirit 4.8k>3.2k; 5 T2 dead-ends (7.2k souls) all with named sells",fix:"Crippling Headshot sells Swift Striker/Active Reload line instead"},
 items:{
  'Bullet Resist Shredder':['LOW','14.4k lands spirit 4.8k; rich Crippling Headshot sells it: spirit 3.2k.'],
  'Recharging Rush':['OK','16.0k, fast-firing hero easily >200 in 3.5s; named sell for a counter.'],
  'Tesla Bullets':['OK','19.2k (ratio 3.0), consumed by Capacitor @25.6k (paid 3200).'],
  'Fleetfoot':['OK','5.6k, gun 4.8k lands; named sell for Unstoppable.'],
 },
 swaps:[],fixes:[],find:['Spikes: gun @5.6k, health @10.4k, spirit @14.4k.']
},
rem:{
 sum:{flags:"MED Heroic Aura note sells Opening Rounds so gun ends 3.2k, 4.8k never (swap Rescue Beam: 13 slots, gun 1.6k); MED Echo Shard 6.4k @17.6k earliest in data.js (median 36.8k); MED Trophy Collector fresh T2 @19.2k on a passive-souls item",
  fix:"Keep Opening Rounds, drop Superior Duration (last core item, 46.4k): 12 slots, gun 4.8k @34.4k; Echo Shard after Healing Booster (24.0k); Trophy Collector after Compress Cooldown (9.6k); swap box Spirit Rend (gun T3) instead of Rescue Beam"},
 items:{
  'Heroic Aura':['MED','Note sells Opening Rounds for it: gun 1.6k+3.2k-1.6k = 3.2k. Keep Opening Rounds and cut Superior Duration instead: gun 4.8k @34.4k, still 12 slots (tested). Swap Rescue Beam is Armor (v3): gun 1.6k, and 13 slots because the sell note is not on the swap.'],
  'Echo Shard':['MED','17.6k, 6400, first T4. Other builds 24.8k to 56.0k (median 36.8k). Rule: no 6400s before ~20 min. Mystic Burst/Compress Cooldown spirit 4.8k @8.0k and Healing Nova health @11.2k already landed, so nothing waits on it. Move after Healing Booster = 24.0k.'],
  'Trophy Collector':['MED','Fresh T2 at 19.2k (ratio 2.4; bebop builds 4.0k to 5.6k). Passive souls and ability range stack from kills/assists, so late buy loses most payoff. After Compress Cooldown (9.6k): spirit 4.8k stays @8.0k, health 4.8k 11.2k>12.8k.'],
  'Healing Booster':['LOW','24.0k fresh T2 but slot-locked upgrade Healing Tempo named; Extra Regen not bought so full 1600.'],
  'Superior Duration':['LOW','46.4k last core item, 3200 fresh (8 bullet resist). Candidate to cut for the Opening Rounds fix.'],
  'Mystic Burst':['OK','5.6k: Pillow Toss 75+1.6x43 = 144 (>80). Tankbuster 31.2k: Pillow Toss 75+1.6x131 = 285 (>165).'],
 },
 swaps:[{b:'Swap for Heroic Aura (Rescue Beam)',ops:['swap:Heroic Aura=Rescue Beam'],v:'FLAG'},
        {b:'Proposed: keep Opening Rounds, cut Superior Duration',ops:['nonote:Heroic Aura','del:Superior Duration'],v:'OK'},
        {b:'Proposed swap box: Spirit Rend instead of Heroic Aura (with the fix above)',ops:['nonote:Heroic Aura','del:Superior Duration','swap:Heroic Aura=Spirit Rend'],v:'OK'}],
 fixes:[{t:'All Rem fixes',ops:['nonote:Heroic Aura','del:Superior Duration','mv:Trophy Collector>after:Compress Cooldown','mv:Echo Shard>after:Healing Booster']}],
 find:['"3+ gun heroes?" reorder (Heroic Aura right after Healing Nova) tested: gun 3.2k, same missing 4.8k as the base; with the Opening Rounds fix it gives gun 4.8k @14.4k.']
},
seven:{
 sum:{flags:"INFO gun 3.2k (Monster Rounds>Cultist) never 4.8k; LOW Mystic Expansion @18.4k imbue on the ult; reorder box tested harmless",fix:"none required"},
 items:{
  'Mystic Expansion':['LOW','800 @18.4k (ratio 2.1), imbue on the ult, Greater Expansion @40.0k. Ult range could be bought earlier; no spike cost (spirit already 4.8k @5.6k).'],
  'Surge of Power':['OK','5.6k, 2400 paid (Extra Spirit consumed): spirit 4.8k lands here per Seven rule (SoP/Arcane Surge early).'],
  'Cultist Sacrifice':['OK','8.0k (2400 paid), rule: early farm/Cultist.'],
  'Healbane':['OK','12.0k fresh T2 with named sell for a counter.'],
 },
 swaps:[],fixes:[{t:'Lost-lane reorder: Mystic Vulnerability before Cultist Sacrifice',ops:['mv:Mystic Vulnerability>before:Cultist Sacrifice']}],find:['Spirit @5.6k then health @12.8k: fighty-hero rule (~11-12k) met within 1k.']
},
};
