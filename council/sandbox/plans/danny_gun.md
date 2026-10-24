# danny_gun (Danny) sandbox plan
Final 12: Express Shot, Swift Striker, Fortitude, Spirit Shielding, Toxic Bullets, Surge of Power, Superior Duration, Warp Stone, Spiritual Overflow, Escalating Exposure, Lucky Shot, Siphon Bullets

## Uncertain slots (substitutes; every slot also tested with none)
- Toxic Bullets -> Hollow Point, Burst Fire, none: DoT + anti-heal; Danny gun has two multi-hit sources already
- Siphon Bullets -> Leech, Vampiric Burst, none: sustain slot: Siphon alone was flagged as not real sustain
- Spirit Shielding -> Spirit Resilience, none: note says sell for Spirit Resilience; test whether the barrier matters at all
- Warp Stone -> Fortitude, Majestic Leap, none: Danny already flies; Warp Stone mainly an engage

## Economy / early game
- Gun/spirit hybrid; HV>Rapid>Express Shot spike by ~6k, Fortitude as health spike ~14k; no income item, farms with Jettison on waves. Cultist Sacrifice optional, not recommended: Jettison clears camps.
- Price points: 8k/12k/20k/30k/full from build order, file _timeline (unlock 8/10/13/16/18 is an assumption). Check cooldowns back, HP, ammo, health spike, damage taken when shot at each.

## Rotation (from kit; A: = item active/imbue popped only if owned)
- A:Surge of Power > cast 3 2.2 > fire 4 > cast 1 0.8 > fire 2 > cast 2 1.0 > fire 2 > # PLANNED enemyhp 45 > cast 4 1.5
- repeats 1x per block; hurtme 150 between; ability CDs need planned `resetcd`.

## Conditions
- Accuracy 100/50/40%, body/head mix; 1 vs 4-5 enemies (ring at ~6m for AoE/aura, then single); incoming gun+spirit damage from bot; start 800 HP down; report if winner changes.
- Jettison needs backblast hit for the fire-rate buff: keep target inside 22m. Bullet resist shred (15%) then Toxic: test vs resist 0 and a realistic 20% bullet / 15% spirit resist.
- Stacks: Siphon Bullets stacks 0/10/max; Jettison buff on/off; Toxic Bullets DoT stacks.
- Resist: run 0 vs realistic (20% bullet / 15% spirit); judge shred items only in resist runs.

## Healing attribution (TEST_MATRIX)
- Kit heal sources: Chimera T2 heal on hero hit (needs the dive); Jettison none. Items: Spirit Lifesteal/Spiritual Overflow (ability lifesteal 13% + 10% spirit lifesteal), Siphon Bullets (2.5% max HP steal), Fortitude (regen out of combat only), Spirit Shielding barrier.
- Heal items in build (auto from item data): Spiritual Overflow, Siphon Bullets. Out-of-combat-only regen items are zero in a fight and excluded from H0 comparisons.
- Blocks (_heal): H0 = build without heal items; only_X = H0 + one item; full. Marginal effect of slot item = (swap file value) - (H0 + others). Log healing per source (planned `healsrc`), never raw hps. Note heal items also carry BonusHealth: compare % of max HP or hold max HP fixed (planned `lowhp 30`).
- Pain-Battery-type/missing-HP effects: low HP only; stack effects at 0/1/max.

## Files
danny_gun_swap / _swaprev / _swapshuf (3 orders, repeat >=3x), danny_gun_heal, danny_gun_timeline, danny_gun_cond  (in /mnt/user-data/outputs/dwpkg2/scenarios/)
Assumptions unverified from game files: hero enum names, `cast iN` = Nth active in give order, `cast k s` hold seconds for channels/charges, unlock level per price point.
