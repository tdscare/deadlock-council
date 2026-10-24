# solomon (Chessmaster) sandbox plan
Abilities: Setup Bishop, Kingside Knight, Rook Battery, Develop Queen  order [1, 1, 2, 3, 1, 4, 4, 1, 2, 3, 3, 4, 3, 2, 4, 2]
Core 12 used in scenarios (first 12 final items in build order): Opening Rounds, Superior Cooldown, Warp Stone, Alchemical Fire, Tankbuster, Greater Expansion, Stamina Mastery, Escalating Exposure, Boundless Spirit, Spirit Burn, Mystic Reverb, Divine Barrier

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Alchemical Fire -> Spirit Rend, Decay, none: weapon-tree item on a spirit AoE hero; scales off spirit invest
- Warp Stone -> Majestic Leap, none: getting into range of the AoE
- Guardian Ward -> Spirit Shielding, Debuff Reducer, none: survival slot

## Economy
Rooks/Queen AoE clear waves; no farm problem, Cultist not needed.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Opening Rounds, Grit, Extra Stamina, Improved Spirit, Superior Cooldown
- 12k (12000 spent): Opening Rounds, Grit, Extra Stamina, Improved Spirit, Superior Cooldown, Mystic Expansion, Warp Stone
- 20k (18400 spent): Opening Rounds, Extra Stamina, Improved Spirit, Superior Cooldown, Mystic Expansion, Warp Stone, Alchemical Fire, Guardian Ward, Mystic Vulnerability, Mystic Burst
- 30k (25600 spent): Opening Rounds, Improved Spirit, Superior Cooldown, Warp Stone, Alchemical Fire, Guardian Ward, Mystic Vulnerability, Tankbuster, Greater Expansion, Stamina Mastery
- full (52800 spent): Opening Rounds, Superior Cooldown, Warp Stone, Alchemical Fire, Tankbuster, Greater Expansion, Stamina Mastery, Escalating Exposure, Boundless Spirit, Spirit Burn, Mystic Reverb, Divine Barrier
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none (Knight self-cast gives combat barrier, not healing)
- Item Mystic Reverb: AbilityLifestealPercentHero=8, ImbueAbilityLifesteal=22
- Baseline regen/Healing Booster/other armor regen counted in block A/B (items not matching heal keys: base regen only).
Blocks: A fire-only no heal items (regen floor), B full rotation no heal items (kit heals), C+item for each heal item (marginal = C - B), D full, E/F at mid HP. Start at hurtme 800 and re-hurt each cycle so healing is never HP-capped. Slot swaps (swap files) report marginal vs the 'none' block. Pain-Battery-style/Berserker-style effects: stack states 0/1/max (see rotation).

## Rotation (cycle x2, derived from kit)
cast 2 0.3, cast 1 0.3, cast 3 0.3, cast 4 0.8, cast 1 0.3, fire 3
Order reasons: imbue/proc items loaded on ability index (assumed) {}; active items cast via cast iN in give order (assumed mapping); ult last (long CD), cc/buff abilities before damage.

## Conditions
- Accuracy 100/50/40 with body/head mix (#P accuracy; plugin op planned). Enemies 1 and 4-5 at close range (#P enemies). Incoming gun+spirit damage via hurtme each cycle; low-HP start. Resist 0 vs realistic (#P resist) for shred items.
- CC: apply stun/slow/disarm on player (planned) - answers in build: Warp Stone, Divine Barrier (blank = none).
- Clean state: each block begins mark none, clear, heal; planned `reset` should also clear buffs/cooldowns; first-block warm-up bias -> run forward + _rev, >=3x.

## Scenario files (/mnt/user-data/outputs/dwpkg2/scenarios)
- solomon_early.txt
- solomon_swap1.txt
- solomon_swap1_rev.txt
- solomon_swap2.txt
- solomon_swap2_rev.txt
- (skipped swap Guardian Ward: not a final core item - component of upgrade)
- solomon_heal.txt
- solomon_heal_rev.txt
