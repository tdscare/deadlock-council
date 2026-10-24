# solomon_support (Chessmaster) sandbox plan
Abilities: Setup Bishop, Kingside Knight, Rook Battery, Develop Queen  order [1, 1, 2, 2, 3, 2, 4, 4, 3, 2, 4, 1, 3, 4, 3, 1]
Core 12 used in scenarios (first 12 final items in build order): Opening Rounds, Superior Cooldown, Healing Nova, Healing Booster, Trophy Collector, Heroic Aura, Enchanter's Emblem, Cursed Relic, Warp Stone, Boundless Spirit, Stamina Mastery, Divine Barrier

## Uncertain slots and substitutes (each swap run vs 'none' too)
- Healing Nova -> Rescue Beam, none: ally survives same burst: score outcome not hps
- Cursed Relic -> Echo Shard, Escalating Exposure, none: late utility slot
- Heroic Aura -> Hunter's Aura, none: only good if allies are gun carries (needs allies op)

## Economy
Rooks/Queen AoE clear waves; no farm problem, Cultist not needed.
Early ladder (items owned at each soul total, built from build order with component credit):
- 8k (8000 spent): Healing Rite, Opening Rounds, Grit, Extra Stamina, Improved Spirit, Compress Cooldown, Sprint Boots
- 12k (12000 spent): Opening Rounds, Grit, Extra Stamina, Improved Spirit, Superior Cooldown, Healing Nova, Sprint Boots
- 20k (20000 spent): Opening Rounds, Extra Stamina, Improved Spirit, Superior Cooldown, Healing Nova, Healing Booster, Trophy Collector, Guardian Ward, Heroic Aura, Enchanter's Emblem
- 30k (29600 spent): Opening Rounds, Extra Stamina, Improved Spirit, Superior Cooldown, Healing Nova, Healing Booster, Trophy Collector, Guardian Ward, Heroic Aura, Enchanter's Emblem, Cursed Relic, Warp Stone
- full (41600 spent): Opening Rounds, Superior Cooldown, Healing Nova, Healing Booster, Trophy Collector, Heroic Aura, Enchanter's Emblem, Cursed Relic, Warp Stone, Boundless Spirit, Stamina Mastery, Divine Barrier
Check at each: cooldowns back before next fight, health, damage, ammo (mag/reload), health spike present, damage taken. Compare p8k/p12k blocks for lane survival.

## Healing sources (game data) - never read raw hps as an item effect
Kit: none (Knight self-cast gives combat barrier, not healing)
- Item Healing Nova: TotalHealthRegen=325 (+6x spirit), RegenDuration=2
- Item Healing Booster: HealAmpCastPercent=20, HealAmpRegenPercent=20, BonusHealthRegen=3
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
- solomon_support_early.txt
- solomon_support_swap1.txt
- solomon_support_swap1_rev.txt
- solomon_support_swap2.txt
- solomon_support_swap2_rev.txt
- solomon_support_swap3.txt
- solomon_support_swap3_rev.txt
- solomon_support_heal.txt
- solomon_support_heal_rev.txt
