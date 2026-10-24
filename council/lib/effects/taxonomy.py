"""Effect taxonomy: generic vocabularies that map game-data field names, modifier states and description phrases to
(op, state, subtype). Nothing here names a hero, an ability or an item. Every rule is a pattern over the data's own
vocabulary; each match is recorded with its grade:
  STRUCTURED    = a field/flag whose meaning the data declares (e.g. m_nAttributes flags, m_eProvidedPropertyType, behavior bits)
  NAME-INFERRED = meaning inferred from a property / state NAME (e.g. 'ChannelDamageImmune'); the engine code behind it is not in the data
  TEXT          = matched phrase in the English localisation text (the developers' own description)
STATES (game-state variables an effect reads or writes):
  incoming_damage  health  status  cooldown  charges  ammo  actions  targetability  duration  timescale  position  stats  trigger
OPS: defer delayed_cost grant prevent absorb reduce amplify redirect heal apply_cc remove_cc reset_cd reduce_cd extend_cd
     recast add_charge ammo extend_duration time_scale displace lockout_self lockout_target stat_buff trigger_item
"""
import re

# ---- property-name lexicon: (regex, op, state, subtype). Order = priority; ALL matching entries apply except where 'stop' ----
PROP_LEX = [
 (r'^Invulnerable$|^Invuln', 'grant', 'incoming_damage', 'invulnerable'),
 (r'DamageImmune|ImmuneToDamage', 'grant', 'incoming_damage', 'damage_immune'),
 (r'^StatusImmune', 'grant', 'status', 'status_immune'),
 (r'KnockupImmune|KnockdownImmune|^UnstoppableCastDelay|^Unstoppable', 'grant', 'status', 'knock_or_unstoppable_immune'),
 (r'^ImmunityDuration$|^SkullImmuneDuration$', 'grant', 'status', 'named_immunity'),
 (r'^DeathImmunity', 'prevent', 'health', 'death_prevention'),
 (r'Deferred?Damage|DamagePctDeferred|^DeferClear|StoredDamage(?!.*(Required|Threshold))', 'defer', 'incoming_damage', 'deferred_damage'),
 (r'^ExpireDamage|^DelayedDamage$', 'delayed_cost', 'incoming_damage', 'delayed_penalty'),
 (r'Penalty', 'stat_buff', 'stats', 'penalty'),
 (r'^(Combat)?Barrier(Health|Duration|DamagePercentage)?$|CombatBarrier|TechShield|BulletShield|^ShieldHealth|SpellShield', 'absorb', 'incoming_damage', 'barrier'),
 (r'(Tech|Bullet|Melee|Spirit)Resist(?!.*Reduc)|^DamageResist|ArmorDamageResist|AllDamageTakenReduction|IncomingDamageReduction', 'reduce', 'incoming_damage', 'resist'),
 (r'ResistReduction|Vulnerab|ArmorReduction|^DamageAmplification|^AmpDamage|^BulletAmp|AmpPercentPerStack|DamageTakenIncrease', 'amplify', 'incoming_damage', 'vulnerability'),
 (r'Reflect|ReturnFire|^Redirect', 'redirect', 'incoming_damage', 'reflect_redirect'),
 (r'HealAmp|HealingEffectiveness|HealingAmp|HealingFactor', 'amplify', 'health', 'heal_amp'),
 (r'DisableHealing|HealAmpReceivePenalty|HealAmpRegenPenalty', 'apply_cc', 'health', 'heal_reduction'),
 (r'Lifesteal|LifeSteal|^Heal(OnHit|OnKill|PerSecond|Amount|Regen|Percent|Max|FixedHealth|OnActivate|OnCast|Interval|Radius)|HealPerSecond|^HealingPerSecond|^HealingAura|HealthRegen$|^BonusHealthRegen|^MissingHPHeal|^FlatHealthHealing|^PercentHealthHealing|^HealPerStack', 'heal', 'health', 'heal_or_sustain'),
 (r'^(Slow|MoveSlow|MovementSlow|EnemySlow|EnemyMoveSlow)(Percent|Duration)?$|^SlowPercent|^FireRateSlow$', 'apply_cc', 'status', 'slow'),
 (r'^(Stun|Knockup|Sleep|Silence|Disarm|Root|Immobiliz|Petrify|Hex|Daze|Freeze|Entangle|Web|Fear|Lift|Wall)[A-Za-z]*Duration$', 'apply_cc', 'status', 'hard_cc'),
 (r'^(PurgeDebuffs|DispelDebuffs|RemoveDebuffs|PurgeOnActivate|PurgeOnCast|DispelOnUse|LeechPurgeBuffs|CleanseDebuffs)$', 'remove_cc', 'status', 'cleanse'),
 (r'^(ResetCooldown|RefreshCooldown|RefundCooldowns|CopyCooldown|RefreshOnKill|RefreshOnDeath|CooldownRefresh|AllowResetCooldown|HopRefresh)|CooldownRefund|^CancelCooldownRefund', 'reset_cd', 'cooldown', 'reset_or_refund'),
 (r'^ImbuedCooldownMultiplier$', 'extend_cd', 'cooldown', 'item_cooldown_scales_with_imbued_ability'),
 (r'CooldownReduc|ReduceCooldown|^ItemCooldownReduc|CooldownBetweenChargeReduction|ImbuedCooldownReduction', 'reduce_cd', 'cooldown', 'cooldown_reduction'),
 (r'^(MaxRecasts|RecastTime|RecastWindow)$', 'recast', 'actions', 'recast'),
 (r'^(BonusAbilityCharges|BonusAbility1Charge|BonusAbilityChargesNonCharge|EnableAbilityCharges|AbilityChargesConditionally|AbilityChargesInitial)$|^AbilityCharges$', 'add_charge', 'charges', 'ability_charges'),
 (r'UnlimitedAmmo|InfiniteClip|^BonusClip|ClipSize|^ActiveReload|AmmoReload|BulletsReloaded|ReloadSpeed|BonusReload', 'ammo', 'ammo', 'ammo_reload'),
 (r'^Invis|Invisibility|Untarget|PhaseOut|ShadowForm', 'grant', 'targetability', 'untargetable_or_invisible'),
 (r'BonusAbilityDurationPercent|BonusItemDurationPercent|^BuffExtend|ExtendByBullet|DurationExtend|^Extend[A-Z]', 'extend_duration', 'duration', 'duration_extension'),
 (r'TimeScale', 'time_scale', 'timescale', 'time_scale'),
 (r'^(Pull|Push|Knockback|KickKnockback|Toss|Launch|Teleport|Blink|Carry|Grab|Hook|Swap|Tether)[A-Za-z]*(Duration|Speed|Distance|Force|Range)?$|^EnemyLiftDuration|^PullDuration', 'displace', 'position', 'displacement'),
]
PROP_LEX = [(re.compile(a), b, c, d) for a, b, c, d in PROP_LEX]

# properties that merely gate/parametrise and must never become an atom on their own
PROP_IGNORE = re.compile(r'^(AbilityCastDelay|AbilityPostCastDuration|AbilityChannelTime|AbilityUnitTargetLimit|AbilityResourceCost|ChannelMoveSpeed|TechPower|WeaponPower|AbilityCastRange|AbilityCooldown|AbilityDuration|AbilityCooldownBetweenCharge)$')

# ---- MODIFIER_STATE_* -> (op, state, subtype, side). side: 'self_or_ally' when granted, 'enemy' when the modifier is a debuff ----
STATE_LEX = {
 'MODIFIER_STATE_INVULNERABLE': ('grant', 'incoming_damage', 'invulnerable'),
 'MODIFIER_STATE_STATUS_IMMUNE': ('grant', 'status', 'status_immune'),
 'MODIFIER_STATE_SLOW_IMMUNE': ('grant', 'status', 'slow_immune'),
 'MODIFIER_STATE_KNOCKDOWN_IMMUNE': ('grant', 'status', 'knockdown_immune'),
 'MODIFIER_STATE_UNSTOPPABLE': ('grant', 'status', 'unstoppable'),
 'MODIFIER_STATE_FEAR_IMMUNE': ('grant', 'status', 'fear_immune'),
 'MODIFIER_STATE_MOD_NO_CLEANSE': ('prevent', 'status', 'cannot_be_cleansed'),
 'MODIFIER_STATE_TECH_UNTARGETABLE': ('grant', 'targetability', 'tech_untargetable'),
 'MODIFIER_STATE_TECH_UNTARGETABLE_BY_ENEMIES': ('grant', 'targetability', 'tech_untargetable_by_enemies'),
 'MODIFIER_STATE_IGNORED_BY_NPC_TARGETING': ('grant', 'targetability', 'ignored_by_npcs'),
 'MODIFIER_STATE_IGNORE_BULLETS': ('grant', 'incoming_damage', 'ignore_bullets'),
 'MODIFIER_STATE_IGNORE_MELEE': ('grant', 'incoming_damage', 'ignore_melee'),
 'MODIFIER_STATE_OUT_OF_GAME': ('grant', 'targetability', 'out_of_game'),
 'MODIFIER_STATE_INFINITE_CLIP': ('ammo', 'ammo', 'infinite_clip'),
 'MODIFIER_STATE_HEALING_DISABLED': ('apply_cc', 'health', 'healing_disabled'),
 'MODIFIER_STATE_STUNNED': ('apply_cc', 'status', 'stun'),
 'MODIFIER_STATE_IS_ASLEEP': ('apply_cc', 'status', 'sleep'),
 'MODIFIER_STATE_IMMOBILIZED': ('apply_cc', 'status', 'root'),
 'MODIFIER_STATE_DISARMED': ('apply_cc', 'status', 'disarm'),
 'MODIFIER_STATE_SILENCED': ('apply_cc', 'status', 'silence'),
 'MODIFIER_STATE_SILENCE_MOVEMENT_ABILITES': ('apply_cc', 'status', 'movement_silence'),
 'MODIFIER_STATE_SHOOTING_DISABLED': ('apply_cc', 'status', 'shooting_disabled'),
 'MODIFIER_STATE_MELEE_DISABLED': ('lockout_target', 'actions', 'melee_disabled'),
 'MODIFIER_STATE_MELEE_DISABLED_DEBUFF': ('apply_cc', 'status', 'melee_disabled'),
 'MODIFIER_STATE_DASH_DISABLED': ('lockout_target', 'actions', 'dash_disabled'),
 'MODIFIER_STATE_DASH_DISABLED_DEBUFF': ('apply_cc', 'status', 'dash_disabled'),
 'MODIFIER_STATE_PARRY_DISABLED': ('lockout_target', 'actions', 'parry_disabled'),
 'MODIFIER_STATE_ITEMS_DISABLED': ('lockout_target', 'actions', 'items_disabled'),
 'MODIFIER_STATE_COMBAT_ABILITIES_DISABLED': ('lockout_target', 'actions', 'combat_abilities_disabled'),
 'MODIFIER_STATE_COMMAND_RESTRICTED': ('lockout_target', 'actions', 'command_restricted'),
 'MODIFIER_STATE_MOVEMENT_INPUT_DISABLED': ('lockout_target', 'actions', 'movement_input_disabled'),
 'MODIFIER_STATE_MOVEMENT_ABILITY_ACTIVATION_RESTRICTED': ('lockout_target', 'actions', 'movement_abilities_restricted'),
 'MODIFIER_STATE_JUMP_DISABLED': ('lockout_target', 'actions', 'jump_disabled'),
 'MODIFIER_STATE_MUTED': ('apply_cc', 'status', 'muted'),
 'MODIFIER_STATE_ABILITY_MOVEMENT': ('displace', 'position', 'ability_movement'),
 'MODIFIER_STATE_FLYING': ('displace', 'position', 'flying'),
 'MODIFIER_STATE_CHAINED': ('apply_cc', 'status', 'chained'),
 'MODIFIER_STATE_PULLDOWN_TO_GROUND': ('displace', 'position', 'pulldown'),
}
# states present in every cast phase mask that carry no interaction meaning
STATE_TRIVIAL = {'MODIFIER_STATE_BUSY_WITH_ACTION', 'MODIFIER_STATE_IN_ABILITY_ALLOW_ZOOM', 'MODIFIER_STATE_HIDE_CROSSHAIR', 'MODIFIER_STATE_HIDE_AMMO'}

# ---- modifier attribute flags (STRUCTURED) ----
ATTR_MEANING = {
 'MODIFIER_ATTRIBUTE_IGNORE_INVULNERABLE': 'modifier is applied/ticks even through invulnerability (as named; exact engine rule not in data)',
 'MODIFIER_ATTRIBUTE_CANNOT_BE_PURGED': 'modifier cannot be removed by purge/dispel (as named)',
 'MODIFIER_ATTRIBUTE_MULTIPLE': 'multiple instances may coexist (as named)',
 'MODIFIER_ATTRIBUTE_PERMANENT': 'no expiry (as named)',
}

# ---- description phrase patterns (TEXT grade). (regex, op, state, subtype) ----
TEXT_LEX = [
 (r'(?:delay|defer|store|numb|postpone)\w*\b.{0,40}\bdamage|delayed damage|stored damage', 'defer', 'incoming_damage', 'deferred_damage'),
 (r'(?:wear|wears|ends?|expires?) .{0,40}(?:deal|extra|additional|penalty|slower)|plus (?:\w+ )?extra damage|act slower', 'delayed_cost', 'incoming_damage', 'delayed_penalty'),
 (r'immune to (?:all )?damage|damage immun|takes? no damage|cannot (?:take|receive) damage', 'grant', 'incoming_damage', 'damage_immune'),
 (r'invulnerab', 'grant', 'incoming_damage', 'invulnerable'),
 (r'protects? (?:\w+ )?from damage|protect(?:s|ion) from (?:all )?damage', 'grant', 'incoming_damage', 'protected_from_damage'),
 (r'unstoppable', 'grant', 'status', 'unstoppable'),
 (r'untargetable|cannot be targeted', 'grant', 'targetability', 'untargetable'),
 (r'reset(?:s)? (?:the )?cooldown|refresh(?:es)? (?:the )?cooldown|cooldown (?:is )?(?:reset|refreshed)', 'reset_cd', 'cooldown', 'reset'),
 (r'cooldown (?:of|is) increased by|item.s cooldown is increased', 'extend_cd', 'cooldown', 'item_cooldown_scales_with_imbued_ability'),
 (r'unable to (?:take|use|cast)|cannot (?:use|cast|act|take any)|can.t (?:use|cast)', 'lockout_target', 'actions', 'cannot_act'),
 (r'removes? (?:all )?(?:non-ult )?(?:\w+ )?debuffs|dispels?|cleanses?|purges?', 'remove_cc', 'status', 'cleanse'),
 (r'incoming healing', 'heal', 'health', 'interacts_with_incoming_heal'),
 (r'attached|latches?|carr(?:y|ies)|pulls? (?:you|them|the target)|drags?|swap(?:s)? places|teleports? (?:an )?(?:ally|enem)', 'displace', 'position', 'displacement_or_attach'),
 (r'on (?:ability )?cast|when you (?:use|cast) an ability|after (?:using|casting) an ability', 'trigger_item', 'trigger', 'on_ability_use'),
 (r'light melee|heavy melee|when you melee|on melee', 'trigger_item', 'trigger', 'on_melee'),
 (r'when you heal|healing an ally|heals? (?:an )?ally', 'trigger_item', 'trigger', 'on_heal'),
]
TEXT_LEX = [(re.compile(a, re.I), b, c, d) for a, b, c, d in TEXT_LEX]

def clean_text(s):
    s = re.sub(r'<[^>]*>', ' ', s or '')
    s = re.sub(r'\{[gs]:[^}]*\}', '#', s)
    return re.sub(r'\s+', ' ', s).strip()

def classify_prop(name):
    return [(op, st, sub) for rx, op, st, sub in PROP_LEX if rx.search(name)] if not PROP_IGNORE.match(name) else []

def classify_text(text):
    out = []
    for rx, op, st, sub in TEXT_LEX:
        m = rx.search(text)
        if m:
            out.append((op, st, sub, m.group(0)))
    return out
