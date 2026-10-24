{
 "id": "infernus_dash",
 "hk": "hero_inferno",
 "hero": "Infernus",
 "tag": "Fix",
 "name": "Rizuhble's Dine And Dash Infernus",
 "desc": "Dash Infernus",
 "tg": [
  "mobility",
  "vitality",
  "Echo Shard"
 ],
 "abil": [
  "Napalm",
  "Flame Dash",
  "Afterburn",
  "Concussive Combustion"
 ],
 "order": [
  3,
  3,
  2,
  2,
  1,
  2,
  4,
  2,
  1,
  4,
  4,
  4,
  1,
  1,
  3,
  3
 ],
 "rows": [
  [
   [
    "Losing lane? Buy 1",
    "",
    true,
    [
     [
      "Extra Regen",
      "Sell it once you're out of slots."
     ]
    ]
   ],
   [
    "Early · L-R",
    "",
    false,
    [
     [
      "Sprint Boots",
      ""
     ],
     [
      "Rapid Rounds",
      ""
     ],
     [
      "Mystic Vulnerability",
      ""
     ],
     [
      "Extra Charge",
      ""
     ],
     [
      "Swift Striker",
      ""
     ],
     [
      "Spirit Lifesteal",
      ""
     ],
     [
      "Rapid Recharge",
      ""
     ],
     [
      "Reactive Barrier",
      ""
     ]
    ]
   ]
  ],
  [
   [
    "Mid · L-R",
    "",
    false,
    [
     [
      "Enduring Speed",
      ""
     ],
     [
      "Duration Extender",
      "On Flame Dash.",
      "2"
     ],
     [
      "Dispel Magic",
      ""
     ],
     [
      "Debuff Reducer",
      ""
     ],
     [
      "Superior Duration",
      ""
     ],
     [
      "Spiritual Overflow",
      ""
     ],
     [
      "Escalating Exposure",
      ""
     ]
    ]
   ]
  ],
  [
   [
    "Late · L-R",
    "",
    false,
    [
     [
      "Unstoppable",
      ""
     ],
     [
      "Echo Shard",
      "On Flame Dash.",
      "2"
     ],
     [
      "Spirit Burn",
      ""
     ],
     [
      "Indomitable",
      ""
     ],
     [
      "Cheat Death",
      "Dash into the middle of them, ult, and live through it."
     ]
    ]
   ],
   [
    "Counters",
    "Get after Enduring Speed if needed. Ahead? Skip it until you're dying. Sell Swift Striker for it.",
    true,
    [
     [
      "Metal Skin",
      "One gun hero is deleting you: Haze, Wraith, Vindicta."
     ],
     [
      "Plated Armor",
      "Most of their damage is gun and Metal Skin isn't enough."
     ],
     [
      "Counterspell",
      "A big ability you can see coming at you, like Lash's ult."
     ],
     [
      "Spirit Resilience",
      "Most of their damage is spirit: Seven, Kelvin, Geist, Vyper."
     ],
     [
      "Healbane",
      "Their healer keeps your burn target alive."
     ]
    ]
   ]
  ],
  [
   [
    "I'm rich as fuck",
    "Most important first.",
    true,
    [
     [
      "Divine Barrier",
      "Sell Dispel Magic for this."
     ],
     [
      "Lightning Scroll",
      "Sell Swift Striker for this."
     ],
     [
      "Boundless Spirit",
      "Sell Rapid Recharge for this."
     ]
    ]
   ],
   [
    "Slot locked",
    "",
    true,
    [
     [
      "Juggernaut",
      "Upgrade of Enduring Speed."
     ]
    ]
   ]
  ]
 ],
 "changes": [
  "Round 13: new dash build (Kieran: lots of greens, Bruber's dash Infernus as reference) — sources (dash-style only): lockbuilds 'Ignornus BrooberGaming.ttv (City Never Sleeps Edit)' (Oct 6, 'the build on my main account'): lane Sprint Boots, Rapid Rounds, Mystic Vulnerability, Extra Charge, Swift Striker, Spirit Lifesteal ('4.8k spike'); mid Rapid Recharge, Shadow Weave (he says he's testing it; Enduring Speed instead, which he also lists, keeps it green and leaves Juggernaut as the slot-locked upgrade), Reactive Barrier, Dispel Magic, Duration Extender; then Superior Duration, Escalating Exposure, Debuff Reducer; 'Infernus' Trinity' Cheat Death, Unstoppable, Echo Shard; capstones Indomitable, Juggernaut, Spiritual Overflow, Divine Barrier. lockbuilds Omuk 'Hybrid (Afterburn and Dash)' (Oct 1) for Spirit Burn. Kit: Flame Dash 38s to 26s at T1, +20 DPS at T2, 2 charges at T3; Extra Charge adds a Napalm charge in lane (Napalm has 1 charge) and a dash charge once Flame Dash is T3. Duration Extender on Afterburn: BurnDuration uses the game's duration scaling (the dash trail's GroundFlameDuration doesn't). Order: seemeta's highest-WR Infernus order (58.0% WR, 1,823 games), the one that maxes Flame Dash by point 8. Spirit Burn at 41.6k: afterburn (30 + 0.66x) plus trail (50 + 0.7x) at ~120 spirit is ~240 a second, well over 500 in 5s.",
  "Round 14: Duration Extender moved from Afterburn to Flame Dash. The old reason was wrong: the dash trail's GroundFlameDuration does scale with duration items (ETechDuration in abilities.vdata), so Duration Extender makes the dash 3s to 3.66s and the trail 5s to 6.1s (T2), on the ability this build casts most (3 charges); Afterburn only burns after weapon hits, and this build has little gun. Counterspell example is Lash's ult only.",
  "Round 15: Counters desc was 118 characters (game limit 112). Reactive Barrier (10.4k) and Enduring Speed (11.2k) swapped so Enduring Speed lands the 4.8k health spike; desc now 'Get after Enduring Speed if needed ... Sell Swift Striker for it.' (111). Same items, same totals.",
  "Round 17: Divine Barrier note uses the standard wording (Dispel Magic is core). Empty Dispel Magic/Debuff Reducer/Unstoppable notes stay empty (site defaults fixed globally).",
  "Round 19: checked against current public builds of this style; it is a real style, no changes.",
  "Round 20: late list to 75.2k: Juggernaut moved in from Slot locked, Boundless Spirit added (Broober 844812 luxury box).",
  "Round 23 (kit): Concussive Combustion stuns 1.25s (+0.9 T3 = 2.15s) and can't be interrupted once cast. Lightning Scroll's stun lands 3s after your ult first damages them (DelayBeforeStun 3, 0.75s stun, 64% slow, 150 damage), so after the ult stun ends they get stunned a second time while you're still in the middle of them. Added 3rd in the late list (worth testing; sells Swift Striker); Boundless Spirit now sells Rapid Recharge.",
  "Round 25: ability order 3214322214441133 -> 3322124214441133 (playstyle-based; see a25/log/infernus_dash.md).",
  "Slot locked: Juggernaut moved out of the rich box (Kieran rule: tiny-gain expensive upgrades are Slot locked).",
  "Cost pass: renamed Dine And Dash Infernus; Spiritual Overflow before Escalating Exposure so gun 4.8k lands at 24.0k instead of 51.2k."
 ]
}