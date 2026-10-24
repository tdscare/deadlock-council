{
 "id": "drifter_spirit",
 "hk": "hero_drifter",
 "hero": "Drifter",
 "tag": "Fix",
 "name": "Rizuhble's Cold Cuts Drifter",
 "desc": "Spirit melee Drifter",
 "tg": [
  "spirit",
  "melee",
  "Spirit Snatch"
 ],
 "abil": [
  "Rend",
  "Stalker's Mark",
  "Bloodscent",
  "Eternal Night"
 ],
 "order": [
  1,
  1,
  2,
  3,
  1,
  2,
  4,
  1,
  2,
  2,
  4,
  4,
  3,
  3,
  3,
  4
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
      "Melee Lifesteal",
      ""
     ],
     [
      "Stalker",
      ""
     ],
     [
      "Spirit Strike",
      ""
     ],
     [
      "Mystic Burst",
      ""
     ],
     [
      "Cold Front",
      ""
     ],
     [
      "Spirit Snatch",
      "Maxed Rend counts as a heavy melee, so it triggers this too."
     ],
     [
      "Sprint Boots",
      ""
     ],
     [
      "Extra Health",
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
      "Trophy Collector",
      ""
     ],
     [
      "Lifestrike",
      ""
     ],
     [
      "Fortitude",
      ""
     ],
     [
      "Mystic Vulnerability",
      ""
     ],
     [
      "Melee Charge",
      ""
     ],
     [
      "Tankbuster",
      ""
     ],
     [
      "Veil Walker",
      ""
     ],
     [
      "Duration Extender",
      "On Stalker's Mark.",
      "2"
     ]
    ]
   ]
  ],
  [
   [
    "Mid · cont.",
    "",
    false,
    [
     [
      "Superior Duration",
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
      "Crushing Fists",
      ""
     ],
     [
      "Escalating Exposure",
      ""
     ],
     [
      "Spirit Burn",
      ""
     ]
    ]
   ],
   [
    "Counters",
    "Get after Lifestrike if needed. Ahead? Skip it until you're dying. Sell Stalker for it.",
    true,
    [
     [
      "Metal Skin",
      "Their gun carry turns and out-shoots you."
     ],
     [
      "Spirit Resilience",
      "Their spirit damage keeps ticking on you, like Infernus burn or Seven's ult."
     ],
     [
      "Counterspell",
      "A big ult or stun you can see coming."
     ],
     [
      "Dispel Magic",
      "Slows and hexes stop you chasing or getting out."
     ],
     [
      "Unstoppable",
      "Stuns keep stopping you before you can finish them."
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
      "Arctic Blast",
      "Upgrade of Cold Front."
     ],
     [
      "Boundless Spirit",
      "Sell Stalker for this, or Trophy Collector if it's gone."
     ],
     [
      "Cursed Relic",
      "Sell Trophy Collector for this, or Veil Walker if it's gone."
     ],
     [
      "Divine Barrier",
      "If you bought Dispel Magic, sell it for this."
     ],
     [
      "Ethereal Shift",
      "Sell Superior Duration for this."
     ]
    ]
   ]
  ]
 ],
 "changes": [
  "Round 13: new spirit build — items from spirit builds only: lockbuilds \"I'm gonna burst\" by Bog (spirit Drifter, Oct 17: Melee Lifesteal, Stalker, Spirit Strike, Extra Health, Cold Front, Spirit Snatch, Hunter's Aura, Sprint Boots; Lifestrike, Fortitude; Melee Charge, Tankbuster, Crushing Fists, Superior Duration, Spirit Burn, Arctic Blast; Enduring Speed/Trophy Collector situational; Silencer late). Ability order by kit (no spirit-only order data): Rend maxed first (T1 +40 close damage, T3 counts as a heavy melee so Spirit Snatch procs on it), then Mark, Bloodscent, ult 13-15.",
  "Round 14: Silencer out, Veil Walker in (Mid, after Tankbuster). Spirit-style evidence: tracklock pro Drifter (148 games, Tankbuster 76%, Spirit Burn 38%) buys Veil Walker 51%, tracklock core lists it, sigma, im da dwifta, cheese bread spirit and BLOODLUST all have it; Silencer is only a late pick in Bog/BLOODLUST and maxed Rend already silences 2s up close. Health now 8k at 23.2k (was 5.6k until 41.6k). Crushing Fists moved to Late (Mid was 9 items). Added the rich box with Divine Barrier (Dispel Magic is in Counters). Ability order now the seemeta most-popular Drifter order (63.1%, 3,974 matches; Rend maxed first, same as the kit order) instead of an unsourced kit order. \"Upgrade.\"/card-restating notes emptied; Spirit Snatch note reworded.",
  "Round 19/20: checked against the real spirit/melee Drifter (Bog 761760 Oct 17, LordNM 787882 Sep 28, Brick Goblin 702822 Oct 12). Renamed Rizuhble's Spirit Melee Drifter (desc Spirit melee Drifter) so the pair reads gun vs spirit/melee. Hunter's Aura (a gun-build item, now only in the gun Drifter) replaced by Mystic Vulnerability, which upgrades to Escalating Exposure in the late list (LordNM, Brick Goblin). Cold Front stays in lane for its damage; its gank-slow note emptied (rule 9). Late list: Escalating Exposure, Boundless Spirit, Cursed Relic, Divine Barrier, Ethereal Shift last (73.6k).",
  "Round 23 (kit): Stalker's Mark bleeds as spirit damage every 0.5s for 8s (T2) (localization: SpiritDPS; ab.py TickRate 0.5, Duration 5 +3), and Escalating Exposure stacks on spirit damage every 0.7s (12 stacks = +54% spirit damage to that target). One Mark fills it by itself, then Rend, Spirit Snatch, Tankbuster and Spirit Burn all hit 54% harder. Escalating Exposure (upgrade of Mystic Vulnerability, +4.8k) moves into Late in Arctic Blast's slot (same 4.8k on top of Cold Front, same colour, spikes unchanged); Arctic Blast moves to the top of the late list as the Cold Front upgrade. Mark's bleed scales with your health regen, not spirit (EHealthRegen x0.015), so spirit items don't raise it.",
  "Round 25: ability order 1122324113234443 -> 1123124122443334 (playstyle-based; see a25/log/drifter_spirit.md).",
  "Round 26 (cost): Fortitude moved right after Lifestrike (Extra Health sat idle until the last buy; health 6.4k/8k now at 15.2k, 4.8k spikes unchanged); renamed Cold Cuts Drifter."
 ]
}