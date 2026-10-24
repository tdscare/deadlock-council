// Curated item -> role weights (sum 1). HEURISTIC composition evidence, hand-assigned from item names/classes/descriptions in audit/items_full_6819.json.
// Every row can be corrected; the classifier prints which items drove each result. Roles:
//  gun spirit melee = personal damage | cc debuff ally = effects on others | sustain defense = personal survival | mobility econ enabler = neutral
const R={
// weapon
'Extended Magazine':{gun:1},'Monster Rounds':{econ:.7,gun:.3},'Cultist Sacrifice':{econ:.8,gun:.2},'Tesla Bullets':{gun:.5,spirit:.5},'Capacitor':{gun:.4,cc:.3,spirit:.3},
'Hollow Point':{gun:.7,debuff:.3},'Opening Rounds':{gun:1},'High-Velocity Rounds':{gun:1},'Weighted Shots':{gun:.5,cc:.5},'Close Quarters':{gun:1},'Long Range':{gun:1},
'Slowing Bullets':{cc:.6,gun:.4},'Spirit Shredder':{debuff:.5,gun:.3,spirit:.2},'Heroic Aura':{ally:.7,gun:.3},'Silencer':{cc:.6,gun:.4},'Berserker':{gun:1},'Frenzy':{gun:1},
'Headshot Booster':{gun:1},'Weakening Headshot':{debuff:.5,gun:.5},'Sharpshooter':{gun:1},'Headhunter':{gun:1},'Spirit Rend':{spirit:.6,gun:.4},'Crippling Headshot':{debuff:.5,gun:.5},
'Mystic Shot':{spirit:.5,gun:.5},'Lucky Shot':{gun:1},'Point Blank':{gun:1},'Toxic Bullets':{debuff:.5,gun:.3,spirit:.2},'Ricochet':{gun:1},'Rapid Rounds':{gun:1},
"Hunter's Aura":{gun:.7,debuff:.3},'Spiritual Overflow':{gun:.5,spirit:.5},'Shadow Weave':{gun:.7,mobility:.3},'Alchemical Fire':{spirit:.5,gun:.5},'Blood Tribute':{gun:.6,sustain:.4},
'Fleetfoot':{mobility:.6,gun:.4},'Kinetic Dash':{mobility:.6,gun:.4},'Glass Cannon':{gun:1},'Melee Charge':{melee:1},'Crushing Fists':{melee:1},'Burst Fire':{gun:1},'Intensifying Magazine':{gun:1},
'Escalating Resilience':{defense:.6,gun:.4},'Swift Striker':{gun:1},'Restorative Shot':{sustain:.5,gun:.5},'Titanic Magazine':{gun:1},'Split Shot':{gun:1},'Active Reload':{gun:1},
'Armor Piercer':{gun:1},'Spellslinger':{spirit:.5,gun:.5},'Stalker':{gun:1},'Express Shot':{gun:1},'Ballistic Enchantment':{spirit:.5,gun:.5},'Recharging Rush':{gun:1},
// vitality
'Melee Lifesteal':{sustain:.7,melee:.3},'Rebuttal':{defense:1},'Counterspell':{defense:1},'Inhibitor':{debuff:.5,defense:.5},'Siphon Bullets':{sustain:.6,debuff:.4},'Extra Health':{defense:1},
'Bullet Lifesteal':{sustain:1},'Debuff Reducer':{defense:1},'Dispel Magic':{defense:1},'Spirit Resilience':{defense:1},'Bullet Resilience':{defense:1},'Metal Skin':{defense:1},
'Healing Booster':{sustain:.7,ally:.3},'Fortitude':{defense:.5,sustain:.5},'Leech':{sustain:1},'Sprint Boots':{mobility:1},'Trophy Collector':{econ:.5,mobility:.5},'Enduring Speed':{mobility:1},
'Stamina Mastery':{mobility:1},'Extra Stamina':{mobility:1},'Grit':{defense:1},'Weapon Shielding':{defense:1},'Spirit Shielding':{defense:1},'Battle Vest':{defense:1},"Enchanter's Emblem":{spirit:.6,defense:.4},
'Return Fire':{defense:1},'Spirit Lifesteal':{sustain:1},'Healbane':{debuff:.6,spirit:.4},'Rescue Beam':{ally:1},'Phantom Strike':{mobility:.5,cc:.5},'Warp Stone':{mobility:1},'Cheat Death':{defense:1},
'Majestic Leap':{mobility:1},'Healing Nova':{ally:.6,sustain:.4},'Restorative Locket':{ally:.7,sustain:.3},'Healing Rite':{sustain:.5,ally:.5},'Infuser':{spirit:.5,enabler:.5},'Guardian Ward':{ally:.6,defense:.4},
'Divine Barrier':{ally:.5,defense:.5},'Unstoppable':{defense:1},'Colossus':{defense:1},'Fury Trance':{gun:.6,sustain:.4},'Vampiric Burst':{sustain:.6,gun:.4},'Lifestrike':{sustain:.6,melee:.4},
"Diviner's Kevlar":{defense:1},'Extra Regen':{sustain:1},'Veil Walker':{mobility:.6,defense:.4},'Reactive Barrier':{defense:1},'Indomitable':{defense:1},'Witchmail':{defense:1},
'Healing Tempo':{sustain:.7,mobility:.3},'Plated Armor':{defense:1},'Spellbreaker':{defense:1},'Juggernaut':{defense:.6,sustain:.4},
// spirit
'Silence Wave':{cc:1},'Extra Spirit':{spirit:1},'Mystic Regeneration':{sustain:.5,spirit:.5},'Improved Spirit':{spirit:1},'Greater Expansion':{enabler:1},'Mystic Expansion':{enabler:1},'Extra Charge':{enabler:1},
'Bullet Resist Shredder':{debuff:1},'Mystic Reverb':{spirit:.5,enabler:.5},'Mystic Burst':{spirit:1},'Tankbuster':{spirit:1},'Mystic Vulnerability':{debuff:.6,spirit:.4},'Mystic Slow':{cc:.6,spirit:.4},
'Escalating Exposure':{debuff:.5,spirit:.5},'Rapid Recharge':{enabler:1},'Compress Cooldown':{enabler:1},'Superior Cooldown':{enabler:1},'Transcendent Cooldown':{enabler:1},'Slowing Hex':{cc:1},
'Spirit Sap':{debuff:.6,spirit:.4},'Focus Lens':{spirit:.6,cc:.4},'Rusted Barrel':{spirit:.6,gun:.4},'Disarming Hex':{cc:1},'Decay':{debuff:.6,spirit:.4},'Scourge':{debuff:.5,spirit:.5},'Knockdown':{cc:1},
'Vortex Web':{cc:1},'Refresher':{enabler:1},'Echo Shard':{enabler:1},'Torment Pulse':{spirit:.7,sustain:.3},'Arcane Surge':{spirit:1},'Cold Front':{cc:.5,spirit:.5},'Arctic Blast':{cc:.5,spirit:.5},
'Ethereal Shift':{mobility:.5,defense:.5},'Cursed Relic':{cc:.6,debuff:.4},'Duration Extender':{enabler:1},'Superior Duration':{enabler:1},'Spirit Strike':{spirit:.5,melee:.5},'Spirit Snatch':{spirit:.6,sustain:.4},
'Radiant Regeneration':{sustain:.8,ally:.2},'Boundless Spirit':{spirit:1},'Surge of Power':{spirit:1},'Suppressor':{debuff:.6,spirit:.4},'Quicksilver Reload':{enabler:.5,gun:.5},'Mercurial Magnum':{gun:1},
'Magic Carpet':{mobility:1},'Spirit Burn':{spirit:.6,debuff:.4},'Lightning Scroll':{spirit:1},'Golden Goose Egg':{econ:1},'Ammo Scavenger':{econ:.5,spirit:.5}};
const ROLES=['gun','spirit','melee','cc','debuff','ally','sustain','defense','mobility','econ','enabler'];
module.exports={R,ROLES};
