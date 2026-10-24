# bebop_bomb (Bebop) sandbox plan
Final 12: Trophy Collector, Enduring Speed, Spirit Snatch, Veil Walker, Tankbuster, Superior Cooldown, Echo Shard, Witchmail, Boundless Spirit, Greater Expansion, Mystic Reverb, Spirit Burn

## Uncertain slots (substitutes; every slot also tested with none)
- Veil Walker -> Warp Stone, Majestic Leap, none: bomb needs a 3.5s fuse; gap closing item guess
- Trophy Collector -> Enchanter's Emblem, Healing Booster, none: passive souls/speed; spirit build has no farm item
- Tankbuster -> Silence Wave, Rapid Recharge, none: bomb is a single big hit: current-health damage helps only if it procs
- Greater Expansion -> Superior Duration, Superior Cooldown, none: bomb radius 8m; hits are not range limited
- Echo Shard -> Refresher, Mystic Vulnerability, none: second bomb vs better ult cycle

## Economy / early game
- Spirit scaling bomb: bomb kills/hits give permanent bonus damage, so farm with bomb on camps. Mystic Burst > Spirit Strike gets 4.8k spirit ~8k; no Cultist (bomb farms), Trophy Collector for passive income is the economy item.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- cast 2 0.5 > cast 3 0.6 > A:Mystic Reverb > cast 1 0.6 > fire 2.5 > cast 4 4.0 > fire 1.5
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Bomb self-damage 20% max HP: must be tested at low HP (bomb can kill you). Bomb stacks at 0/1/max. Bomb only if kill within 10s window. Hook cancelled by stun: Unstoppable answer (counters). 5-bot ring valuable (bomb radius 8m).
- Stacks: Bomb stacks 0 / 10 hero hits / max with diminish at 60 hits/7 kills.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Mystic Reverb ability lifesteal 8% (22% on imbued ability); Hyper Beam T3 65% beam lifesteal; Uppercut T3 18% missing HP. No health-spike item beyond Boundless/Improved Spirit/Tankbuster HP; low sustain.
- Heal items in build (auto from item data): Veil Walker, Mystic Reverb. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
bebop_bomb_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), bebop_bomb_heal, bebop_bomb_timeline, bebop_bomb_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.
