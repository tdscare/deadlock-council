"""Hero kit -> OFFERS (what the hero can do for another) and NEEDS (what its own kit wants / what limits it).
Everything is derived from raw abilities.vdata / heroes.vdata / localisation through gamedata.py; no hero or ability name appears in any rule.
Each fact carries: grade  DATA (numeric property in the vdata) | STATE (modifier state mask in the vdata) | TEXT (English description only) | INFER (property NAME only)
and ev = list of 'class.Property=value' / 'class:text' strings so every claim can be traced.  Unknown stays the string 'UNKNOWN'."""
import re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gamedata as G

UNK = 'UNKNOWN'

# ---------------- lexicons (patterns over the game's own vocabulary) ----------------
HARD_CC = [  # (kind, duration-property regex, state)
    ('stun', r'^(Stun[A-Za-z]*Duration|StunDuration[A-Za-z]*|LateCheckoutStun|StompStunDuration|WallStunDuration)$|^StunDuration$', 'MODIFIER_STATE_STUNNED'),
    ('immobilize', r'^(Immobilize[A-Za-z]*|EntangleDuration|HoldInPlaceDuration|RootDuration|WebDuration)$', 'MODIFIER_STATE_IMMOBILIZED'),
    ('sleep', r'^(SleepDuration|MinSleepTime)$', 'MODIFIER_STATE_IS_ASLEEP'),
    ('silence', r'^(SilenceDuration|SilenceDebuff)$', 'MODIFIER_STATE_SILENCED'),
    ('disarm', r'^(DisarmDuration)$', 'MODIFIER_STATE_DISARMED'),
    ('petrify', r'^(PetrifyDuration)$', None),
]
SLOW_PROPS = re.compile(r'^(SlowPercent|EnemySlowPct|EnemySlowPercent|MoveSlowPercent|MovementSlow|MovementSlowPct|MoveSpeedSlowPct|FadingSlowPercent|CoatedSlowPercent|AuraSlowAmount|MaxSlowPercent|SpinSlowPercent|MovementSlowPercent|ClubSlowPercent|SlowPercentPerStack)$')
SLOW_DUR = re.compile(r'^(SlowDuration|EnemySlowDuration|MovementSlowDuration|MoveSlowDuration|CoatedSlowDuration|DebuffDuration|MaxSlowTime)$')
# resist/amp: (type, regex, shared?) -- shared False = caster-only by property name
SHRED = [
    ('bullet', r'^(BulletResistReduction|BulletArmorReduction(?!Duration)|BulletArmorDamageReduction|DiamondResistShred|BulletResistReductionPerStack|ArmorReductionPerBite|ArmorReductionPerStackNonHero)$'),
    ('spirit', r'^(TechArmorDamageReduction|TechResistDebuff|MagicResistReduction|TechArmorDamageReductionPerStack|TechResistReduction)$'),
    ('melee', r'^(MeleeResistReduction)$'),
]
AMP = [  # all-damage amplifiers on the target
    ('all', r'^(DamageAmplificationPerStack|DamageAmpPercentage|AmpPercentPerStack|IncomingDamagePercent|VulnerabilityPerStack|DamageAmplification|AmpDamagePercent|DamageAmp)$'),
]
CASTER_ONLY = re.compile(r'FromCaster|BulletAmp$|^DamageBonus$|^BonusDamagePercent$|^BulletDamageAmp$|^WeaponPowerDebuff')   # raised only by the caster's own hits (by name) -- UNVERIFIED engine rule
ANTIHEAL = re.compile(r'^(HealAmpReceivePenaltyPercent|HealAmpRegenPenaltyPercent|DisableHealing)$')
DEBUFF_DUR = re.compile(r'^(DebuffDuration|BulletResistReductionDuration|MeleeResistReductionDuration|AmpDuration|BulletAmpDuration|BulletArmorReductionDuration|DamageAmpDuration|StackDuration|VictimStackDuration|CoatedDuration|EffectDuration|AuraEffectDuration|BuffDuration)$')
BARRIER = re.compile(r'^(CombatBarrier|AirDropBulletShield|ShieldHealth|TechShield|BulletShield)$')
HEAL = re.compile(r'^(HealAmount|HealingPerSecond|HealthRegen|BonusHealthRegen|ExternalBonusHealthRegen|HealFixedHealth|HealMaxHealth|HealPerSecond|HealPerPickup|TotalHealthRegen|MaxHealthRegenPct|MissingHealthPercentHeal|MissingHPHeal|InfestHeal|HealOnHit|RakeHealPerKill|HealPctVsHeroes)$')
CLEANSE = re.compile(r'^(PurgeDebuffs|PurgeOnCast|DispelOnUse|RemoveDebuffs|ReduceDebuffs|PurgeOnActivate)$')
UNSTOP_STATES = {'MODIFIER_STATE_UNSTOPPABLE', 'MODIFIER_STATE_STATUS_IMMUNE', 'MODIFIER_STATE_INVULNERABLE', 'MODIFIER_STATE_UNIT_STATUS_HEALTH_HIDDEN'}
# displacement parameters (name -> direction class)
DISPLACE_PROPS = [
    ('pull', r'^(PullDistance|PullForceMax|EnemyDragSpeed|FollowDistance|PullInStrength|IcePathPullInStrength|VacuumSpeed|PullDownRange|GrabExtraTargetsRadiusMult)$'),
    ('knock_away', r'^(KnockbackSpeed|PushForce|BonusKnockbackDistance|MaxPushForceHorizontal|EnemyPushForceAway|KnockForce|KnockAwaySpeed|TossBackSpeed|PushBackForce)$'),
    ('lift_toss', r'^(TossDistance|ThrowDistance|LiftHeight|LiftDuration|TossDuration|TossUpSpeed|TossSpeed|EnemyLiftDuration|TossForce|UpForce|KnockupSpeed|EnemyTossVelocity|EnemyHeroTossVelocity|StompBounceHeight)$'),
    ('swap', r'^(SwapTime|MinSwapTime|MultiSwap|TotalSwaps)$'),
    ('teleport_target', r'^(TeleportBackOffsetFromTarget|AllyDistance)$'),
    ('tether', r'^(ChainLength|TetherRadius|TetherDuration|RopeLength|RopeSnapDistance|TetherBreakRange|CaptureRadius|ChainDuration|EscapeRange)$'),
]
# delays that make a payload wait for a target to remain (name -> role)
DELAY_PROPS = re.compile(r'^(ShockDelay|DetonationDelay|ExplodeDelay|ArmTime|ArmingDuration|ArmingTime|StartupDelay|GroundAuraPopDelay|FirstBounceDetonateTimer|TripTime|TimeToEntangle|PreExplosionDuration|SwapEndDelay|ExplodeDelayTime|BarrageStartDelayMax|BuffDelay|LiftInitialDelay|HookImpactDelay|InitialDelay)$')
CHARGE_PROPS = re.compile(r'^(TimeToFullCharge|MaxChargeDuration|HoldDurationMax|TimeToGainLockonStack|PerfectHoldTimeStart)$')
STACK_PROPS = re.compile(r'^(MaxStacks|BuffMaxStacks|MaxStacksPerTarget|FixationStacks)$')
SELFDMG = re.compile(r'^(SelfDamagePct|SelfDamagePercent|SelfDamagePercentage|SelfDamage|HealthToDamage|MaxHealthSelfDamagePercent|CurrentHealthPercentDamage|SelfDPS)$')
CONDITIONS = [  # (state, regex over property name or text, grade)
    ('low_health', r'LowHealth|ExecuteThreshold|CheckmateThreshold|EnemyHealthPercent$|MissingHealth|VenomMaxDamageHealth|HealthThreshold'),
    ('wall', r'Wall(Stun|Hit|Impact|Bonus)|WallImpactRange|WallStunDistance|KnockedOffDamage'),
    ('isolated', r'Isolat'),
    ('close_range', r'RangeForBonusDamage|CloseRange|BonusDamageCloseRange'),
    ('marked_or_revealed', r'IncomingDamagePercentFromCaster|CoatedDamage|MarkDuration|RevealDuration|BurstMarkStacks|ExtraMarkDamage'),
    ('stacks_on_target', r'^(MaxStacks|DamagePerStack|BonusDamagePerStack|DamageBonusFixedPerStack|BuildUpPerShot|VictimStackDuration|StackDuration)$'),
]
# description text patterns for conditions that have no property (TEXT grade)
COND_TEXT = [
    ('isolated', r'\bisolat|\bno (?:other |nearby )(?:enem|allies)|\balone\b'),
    ('wall', r'\bwall\b'),
    ('immobilised_target', r'(?:immobiliz|stunned|slowed|rooted|debuffed|disabled)\w* (?:enem|target|hero)|against (?:immobiliz|stunned|slowed|rooted)'),
    ('low_health', r'below \d+%|less than \d+%|low health|missing health|execut'),
    ('close_range', r'close range|at close range|point.blank|up close|if the enemy is close'),
    ('revealed', r'reveal'),
]

def _f(x):
    return x if isinstance(x, (int, float)) else None

def tiers_of(a, prop):
    return [a.p(prop, t) for t in range(4)]

def tier_first(a, prop):
    """lowest tier (0..3) at which prop > 0 (or != 0 for negative-valued shreds)"""
    for t in range(4):
        v = a.p(prop, t)
        if v not in (None, 0, 0.0): return t
    return None

def val(a, prop, tier=3):
    v = a.p(prop, tier)
    return v if v is not None else UNK

def side_of(a):
    """who the ability's primary effect lands on: enemy / ally / any / self"""
    T = a.targets
    en = any(x for x in T if 'ENEMY' in x and any(k in x for k in ('HERO', 'ALL')))
    fr = any(x for x in T if 'FRIENDLY' in x and any(k in x for k in ('HERO', 'ALL')))
    anyh = 'CITADEL_UNIT_TARGET_HERO' in T or 'CITADEL_UNIT_TARGET_ALL' in T
    if anyh or (en and fr): return 'any'
    if fr: return 'ally'
    if en: return 'enemy'
    return 'self' if not T or T == {'CITADEL_UNIT_TARGET_NONE'} else 'unknown'

def states_by_side(a):
    """modifier states the ability applies, split by the modifier's position in the ability definition (path words). UNKNOWN side kept apart."""
    out = {'self': set(), 'target': set(), 'unknown': set()}
    for path, cls, st in a.modifier_states():
        p = path.lower() + ' ' + str(cls).lower()
        key = 'self' if 'self' in p else ('target' if 'target' in p or 'debuff' in p or 'victim' in p else 'unknown')
        out[key] |= set(st)
    return out

class Offer(dict):
    pass

def mk(kind, a, side, tier, params, grade, ev, **kw):
    d = Offer(kind=kind, ability=a.cls, aname=a.name, tier=tier, side=side, params=params, grade=grade, ev=ev)
    d.update(kw)
    return d

def _ev(a, prop, tier=3):
    v = a.p(prop, tier)
    return '%s.%s=%s' % (a.cls, prop, ('%g' % v) if v is not None else '?')

def ability_offers(a):
    O = []
    side = side_of(a)
    sts = states_by_side(a)
    cd = [a.p('AbilityCooldown', t) for t in range(4)]
    props = list(a.props0)
    txt = a.fulltext().lower()
    cast_delay = a.p('AbilityCastDelay', 0) or 0.0
    dur_t = lambda t: a.p('AbilityDuration', t)
    # ---- hard CC on enemies ----
    for kind, rx, state in HARD_CC:
        for p in props:
            if re.match(rx, p):
                t0 = tier_first(a, p)
                if t0 is None: continue
                d = a.p(p, 3)
                if kind == 'silence' and p == 'SilenceDebuff': continue
                if kind == 'sleep' and p == 'MinSleepTime': continue
                prm = dict(duration=d)
                brk = False
                if kind == 'sleep':
                    prm['wake_delay_after_damage'] = a.p('SleepWakeUpDelay', 3) if a.has('SleepWakeUpDelay') else (UNK)
                    prm['min_sleep'] = a.p('MinimumSleepTime', 3) if a.has('MinimumSleepTime') else (a.p('MinSleepTime', 3) if a.has('MinSleepTime') else UNK)
                    prm['damage_threshold'] = a.p('SleepDamageThreshold', 3) if a.has('SleepDamageThreshold') else None
                    brk = True
                # applies only after a condition (wall/escape failure/late checkout) -> flag
                cond = None
                if re.search(r'Wall', p): cond = 'wall'
                if p.startswith('LateCheckout'): cond = 'failure_to_check_out'
                if re.search(r'Escape', ' '.join(props)) and kind == 'immobilize' and 'EscapeTime' in a.props0: cond = 'target_stays_still_EscapeTime=%g' % a.p('EscapeTime', 3)
                O.append(mk('cc_' + kind, a, 'enemy' if side != 'ally' else side, t0, prm, 'DATA', [_ev(a, p)], breaks_on_damage=brk, condition=cond, pprop=p, dprop=p))
    # state-mask-only CC (no duration property) -> duration UNKNOWN unless AbilityDuration/ChannelTime
    seen = {o['kind'] for o in O}
    for st, kind in (('MODIFIER_STATE_STUNNED', 'cc_stun'), ('MODIFIER_STATE_IS_ASLEEP', 'cc_sleep'), ('MODIFIER_STATE_IMMOBILIZED', 'cc_immobilize'), ('MODIFIER_STATE_SILENCED', 'cc_silence'), ('MODIFIER_STATE_DISARMED', 'cc_disarm')):
        if kind in seen: continue
        if st in sts['target'] or (st in sts['unknown'] and 'CITADEL_UNIT_TARGET_HERO_ENEMY' in a.targets):
            dd = a.p('AbilityDuration', 3) or a.p('AbilityChannelTime', 3) or UNK
            if dd == 0 or (dd != UNK and dd >= 999): dd = UNK
            O.append(mk(kind, a, 'enemy', 0, dict(duration=dd), 'STATE', ['%s modifier_state %s (%s side)' % (a.cls, st, 'target' if st in sts['target'] else 'unknown')],
                        breaks_on_damage=(kind == 'cc_sleep'), condition=None))
    # ---- slows ----
    for p in props:
        if SLOW_PROPS.match(p):
            t0 = tier_first(a, p)
            if t0 is None: continue
            v = abs(a.p(p, 3))
            dprop = next((q for q in props if SLOW_DUR.match(q) and (q.startswith(p[:4]) or q == 'SlowDuration' or q == 'DebuffDuration')), None)
            dur = a.p(dprop, 3) if dprop else UNK
            O.append(mk('slow', a, 'enemy', t0, dict(pct=v, duration=dur if dur else UNK), 'DATA', [_ev(a, p)] + ([_ev(a, dprop)] if dprop else []), pprop=p, dprop=dprop))
            break
    # ---- resist shred / vulnerability ----
    for typ, rx in SHRED:
        for p in props:
            if re.match(rx, p):
                t0 = tier_first(a, p)
                if t0 is None: continue
                v = abs(a.p(p, 3))
                dprop = next((q for q in props if q == p + 'Duration'), None) or next((q for q in props if DEBUFF_DUR.match(q) and (a.p(q, 3) or 0) > 0), None) or next((q for q in props if SLOW_DUR.match(q) and (a.p(q, 3) or 0) > 0), None)
                stack = a.p(next((q for q in props if STACK_PROPS.match(q)), 'zz'), 3)
                O.append(mk('shred_' + typ, a, 'enemy', t0, dict(pct=v, duration=a.p(dprop, 3) if dprop else UNK, per_stack=bool(re.search('Stack|Bite', p)), max_stacks=stack),
                            'DATA', [_ev(a, p)] + ([_ev(a, dprop)] if dprop else []), shared=UNK, pprop=p, dprop=dprop))
    for typ, rx in AMP:
        for p in props:
            if re.match(rx, p):
                t0 = tier_first(a, p)
                if t0 is None: continue
                v = a.p(p, 3)
                dprop = next((q for q in props if DEBUFF_DUR.match(q)), None)
                O.append(mk('amp_' + typ, a, 'enemy', t0, dict(pct=v, duration=a.p(dprop, 3) if dprop else UNK), 'DATA', [_ev(a, p)], shared=(False if CASTER_ONLY.search(p) else UNK)))
    for p in props:
        if CASTER_ONLY.search(p) and tier_first(a, p) is not None and not p.startswith('Weapon'):
            O.append(mk('amp_caster_only', a, 'enemy', tier_first(a, p), dict(pct=a.p(p, 3)), 'INFER', [_ev(a, p)], shared=False))
    for p in props:
        if ANTIHEAL.match(p) and tier_first(a, p) is not None:
            O.append(mk('antiheal', a, 'enemy', tier_first(a, p), dict(pct=abs(a.p(p, 3))), 'DATA', [_ev(a, p)])); break
    # ---- displacement ----
    for cls, rx in DISPLACE_PROPS:
        hits = [p for p in props if re.match(rx, p) and tier_first(a, p) is not None]
        if hits:
            prm = {p: a.p(p, 3) for p in hits}
            t0 = min(tier_first(a, p) for p in hits)
            # does it act on allies / enemies / the caster? text and targeting decide; unknown stays unknown
            tgt_txt = 'ally' if re.search(r'\bally|allies|friendly|teammate', txt) else None
            O.append(mk('displace_' + cls, a, side, t0, prm, 'DATA', [_ev(a, p) for p in hits[:3]], ally_text=bool(tgt_txt)))
    # desc keywords for displacement that have no numeric property
    kw = re.findall(r'\[(Pulls?|Pulling|KnockUp|KnockBack)\]', a.desc() + ' ' + a.fulltext())
    for k in set(kw):
        if not any(o['kind'].startswith('displace_') and o['ability'] == a.cls and (('pull' in o['kind']) == k.lower().startswith('pull')) for o in O):
            O.append(mk('displace_' + ('pull' if k.lower().startswith('pull') else 'knock_up' if k == 'KnockUp' else 'knock_away'), a, side, 0, {}, 'TEXT', ['%s desc [%s]' % (a.cls, k)], ally_text=False))
    # ---- ally-directed mobility / carry (targets friendly heroes AND moves someone) ----
    friendly = side in ('ally', 'any') or 'CITADEL_UNIT_TARGET_ALL_FRIENDLY' in a.targets
    allies_txt = bool(re.search(r'\bally\b|\ballies\b|friendly hero|teammate|\bany hero\b|\ball heroes\b', txt))
    moves = ('CITADEL_ABILITY_BEHAVIOR_MOVEMENT' in a.behaviors) or bool(re.search(r'\bcarry|take flight|grab an ally|bring nearby allies|tag along|jump to an ally|grapple allies|hook.*allies|can be used on allies|friendly heroes? instead|punch.*allies|everyone in the area', txt))
    if friendly and allies_txt and moves:
        mv = {p: a.p(p, 3) for p in props if re.match(r'^(AllyDistance|AllyCastDelay|FlyingItemCastRange|AbilityCastRange|FriendlyHookIgnoreRange|MoveDistance|SelfMoveDistance|TossDurationFriendly|FriendlyImpactDuration)$', p) and a.p(p, 3)}
        carried = sts['self'] | sts['target'] | sts['unknown']
        O.append(mk('ally_move', a, 'ally', 0, dict(duration=a.p('AbilityDuration', 3) or UNK, cast_range=a.p('AbilityCastRange', 3) or UNK, **{k: v for k, v in mv.items() if k != 'AbilityCastRange'}),
                    'TEXT' if not a.has('AllyDistance') else 'DATA', ['%s targets=%s' % (a.cls, sorted(x.replace('CITADEL_UNIT_TARGET_', '') for x in a.targets)), '%s desc: %s' % (a.cls, a.desc()[:140])],
                    states_applied=sorted(carried), own_outgoing_dmg=a.p('AllyOutgoingDamagePercent', 3) if a.has('AllyOutgoingDamagePercent') else None,
                    ally_cooldown_pct=a.p('CooldownReductionPctOnOthers', 3) if a.has('CooldownReductionPctOnOthers') else None))
    # ---- protection of an ally ----
    prot_side = 'ally' if (friendly and allies_txt) else ('ally?' if friendly else 'self')
    for p in props:
        if BARRIER.match(p) and tier_first(a, p) is not None:
            dprop = next((q for q in props if q in ('BarrierDuration', 'BuffDuration', 'AbilityDuration')), None)
            O.append(mk('barrier', a, prot_side, tier_first(a, p), dict(amount=a.p(p, 3), duration=a.p(dprop, 3) if dprop else UNK), 'DATA', [_ev(a, p)])); break
    for p in props:
        if HEAL.match(p) and tier_first(a, p) is not None:
            O.append(mk('heal', a, prot_side, tier_first(a, p), dict(prop=p, amount=a.p(p, 3)), 'DATA', [_ev(a, p)])); break
    for p in props:
        if CLEANSE.match(p) and tier_first(a, p) is not None:
            O.append(mk('cleanse', a, prot_side, tier_first(a, p), {}, 'DATA', [_ev(a, p)])); break
    imm = (sts['self'] | sts['target'] | sts['unknown']) & UNSTOP_STATES
    if imm:
        O.append(mk('immunity', a, 'self' if side != 'ally' else 'ally', 0, dict(states=sorted(s.replace('MODIFIER_STATE_', '') for s in imm), duration=a.p('AbilityDuration', 3) or a.p('ImmunityDuration', 3) or UNK), 'STATE', ['%s states %s' % (a.cls, sorted(imm))]))
    if re.search(r'enter(?:ing)? one door|exit out|portal', a.desc().lower()):
        O.append(mk('displace_portal', a, 'any', 0, {p: a.p(p, 3) for p in props if re.match(r'^(DoorwayDistance|AbilityDuration|AbilityCastRange|DoorwayCloseCooldown)$', p)}, 'TEXT', ['%s desc: %s' % (a.cls, a.desc()[:110])], ally_text=True))
    if re.search(r'out of the world|guest at|removes? (?:the )?target from', a.desc().lower()) or 'MODIFIER_STATE_OUT_OF_GAME' in (sts['self'] | sts['target'] | sts['unknown']):
        O.append(mk('remove_target', a, 'enemy', 0, dict(duration=a.p('AbilityDuration', 3) or UNK), 'STATE', ['%s OUT_OF_GAME state / desc' % a.cls]))
    # ---- terrain / blockers / zones ----
    wallp = [p for p in props if re.search(r'Wall(Length|Height|Width|Depth|Segments)|BlockerScale|TimeWall|ZombieWall|CubeScale', p)]
    if wallp or re.search(r'(?:create|cast|erect|summon|place|deploy|unearth)s?\b[^.]{0,30}\b(?:wall|dome|barrier|pillar)\b|impenetrable', a.desc().lower()):
        O.append(mk('terrain', a, 'area', 0, {p: a.p(p, 3) for p in wallp[:4]}, 'DATA' if wallp else 'TEXT', [_ev(a, p) for p in wallp[:2]] or ['%s desc: %s' % (a.cls, a.desc()[:100])]))
    # ---- ally buffs (damage/fire rate/spirit/lifesteal/speed) given to allies ----
    if (friendly or re.search(r'allies', txt)) and not O and False:
        pass
    for p in props:
        if re.match(r'^(BonusFireRate|AlliedFireRatePercentage|AuraFireRateBonus|BonusSpirit|BonusSpiritPower|TechPowerPercent|BulletLifestealPercent|BonusWeaponDamage|WeaponDamageBonus|FriendlyBulletDamageBonus|MoveSpeedBonus|MovementSpeedBonus|BonusMoveSpeed|AllyDamageReduction|OutgoingDamagePercent)$', p) and tier_first(a, p) is not None:
            if (a.p(p, 3) or 0) > 0 and (allies_txt or (friendly and not a.has('ALLOW_SELF'))) and allies_txt:
                O.append(mk('ally_buff', a, 'ally', tier_first(a, p), dict(prop=p, amount=a.p(p, 3), duration=a.p('AbilityDuration', 3) or a.p('BuffDuration', 3) or UNK), 'DATA' if friendly else 'TEXT', [_ev(a, p)]))
                break
    # ---- cooldown ----
    for p in props:
        if re.match(r'^(CooldownReductionPctOnOthers|CDReduceOnPillowHit|ResetCooldownOnFriendlyHook|CooldownRefundPercent|RestoreHookCooldown)$', p) and tier_first(a, p) is not None:
            O.append(mk('cooldown', a, 'ally' if 'Others' in p or 'Friendly' in p else 'self', tier_first(a, p), dict(prop=p, amount=a.p(p, 3)), 'DATA', [_ev(a, p)]))
    # ---- vision ----
    if a.has('RevealDuration') or re.search(r'\brevealed?\b', a.fulltext().lower()):
        O.append(mk('reveal', a, 'enemy', tier_first(a, 'RevealDuration') or 0, dict(duration=a.p('RevealDuration', 3) or UNK), 'DATA' if a.has('RevealDuration') else 'TEXT', ['%s reveal' % a.cls]))
    # ---- economy ----
    for p in props:
        if re.match(r'^(BonusGoldOnKill|BonusSoulsPct|SkullKillGold)$', p) and tier_first(a, p) is not None:
            O.append(mk('economy', a, 'self', tier_first(a, p), dict(prop=p, amount=a.p(p, 3)), 'DATA', [_ev(a, p)]))
    trig = re.search(r'lethal damage|upon death|when you die|after (?:you )?dying|on death|after taking lethal', txt)
    for o in O:
        o['cd'] = cd
        o['cast_delay'] = cast_delay
        if trig and not o.get('condition'):
            o['condition'] = 'triggers only on the caster\'s own death ("%s") - not a usable coordinated effect' % trig.group(0)
            o['unusable'] = True
    return O

# ---------------- NEEDS ----------------
def ability_needs(a, hk):
    N = []
    props = list(a.props0)
    txt = a.fulltext().lower()
    cdm = a.p('AbilityCooldown', 3) or 0
    ch = a.p('AbilityChannelTime', 3) or 0
    rng = a.p('AbilityCastRange', 3) or 0
    radius = next((a.p(p, 3) for p in ('Radius', 'ShockRadius', 'ExplosionRadius', 'ShotRadius', 'ImpactRadius', 'AuraRadius', 'VacuumRadius', 'GroveRadius', 'ExplodeRadius', 'ChainRadius', 'DragonSearchRadius') if a.has(p) and a.p(p, 3)), None)
    dmg_prop = max([(a.p(p, 3) or 0, p) for p in ('Damage', 'ImpactDamage', 'PulseDamage', 'ExplosionDamage', 'DamagePerRocket', 'FullChargeDamage', 'BigExplosionDamage', 'DelayedDamage', 'CartDamage', 'MaxDamage', 'PerfectDamage', 'BaseDamage', 'ScorchDamage', 'LateCheckoutDamage', 'PetrifyDamage', 'HealthToDamage') if a.has(p)] + [(0, '')], key=lambda x: x[0])
    dmg, dmg_prop = dmg_prop[0], (dmg_prop[1] or None)
    dps_prop = max([(a.p(p, 3) or 0, p) for p in ('DPS', 'PulseDPS', 'BleedDPSPerStack', 'TurretDPS', 'LifeDrainPerSecond', 'MaxDPS') if a.has(p)] + [(0, '')], key=lambda x: x[0])
    dps, dps_prop = dps_prop[0], (dps_prop[1] or None)
    base = dict(ability=a.cls, aname=a.name, hero=hk)
    # delayed payload: a target must remain where the effect lands
    dl = [(p, a.p(p, 3)) for p in props if DELAY_PROPS.match(p) and (a.p(p, 3) or 0) >= 0.5]
    if dl and (dmg or dps):
        p, d = max(dl, key=lambda x: x[1])
        N.append(dict(base, kind='delayed_payload', delay=d, radius=radius, damage=dmg, dmg_prop=dmg_prop, cd=cdm, ev=['%s.%s=%g' % (a.cls, p, d)], grade='DATA',
                      self_applied_hold=any(o['kind'] in ('cc_immobilize', 'cc_stun') for o in ability_offers_cache(a))))
    ct = [(p, a.p(p, 3)) for p in props if CHARGE_PROPS.match(p) and (a.p(p, 3) or 0) >= 0.5]
    if ct:
        p, d = max(ct, key=lambda x: x[1])
        N.append(dict(base, kind='charge_or_lockon', delay=d, damage=dmg, dmg_prop=dmg_prop, cd=cdm, ev=['%s.%s=%g' % (a.cls, p, d)], grade='DATA'))
    cast_d = a.p('AbilityCastDelay', 3) or 0
    chan = 'CITADEL_ABILITY_BEHAVIOR_CHANNELLED' in a.behaviors
    unit_t = (rng > 0 and any('HERO_ENEMY' in t for t in a.targets) and 'CITADEL_ABILITY_BEHAVIOR_PROJECTILE' not in a.behaviors)
    if cast_d >= 0.7 and (dmg or dps) and not chan and not unit_t:   # a cast wind-up only matters for a ground-anchored, non-channelled, non-unit-targeted effect
        N.append(dict(base, kind='delayed_payload', delay=cast_d, radius=radius, damage=dmg, dmg_prop=dmg_prop, cd=cdm, ev=['%s.AbilityCastDelay=%g' % (a.cls, cast_d)], grade='DATA', self_applied_hold=False))
    # exposed channel
    cms = a.p('ChannelMoveSpeed', 3) if a.has('ChannelMoveSpeed') else None
    rooted = (cms is not None and 0 <= cms <= 4.0)      # ChannelMoveSpeed 0 = rooted, small = crawling, -1 = unrestricted (DATA)
    if 'CITADEL_ABILITY_BEHAVIOR_CHANNELLED' in a.behaviors and 1.0 <= ch < 100 and rooted:
        intr = sorted(s.replace('MODIFIER_STATE_', '') for s in a.interrupting)
        unstop = bool(set(['MODIFIER_STATE_UNSTOPPABLE', 'MODIFIER_STATE_STATUS_IMMUNE', 'MODIFIER_STATE_INVULNERABLE']) & set(s for _, _, ss in a.modifier_states() for s in ss))
        if not unstop:
            N.append(dict(base, kind='exposed_channel', rooted=True, channel_move_speed=cms, channel=ch, interrupted_by=intr, radius=radius, damage=dmg, dps=dps, dmg_prop=dmg_prop, dps_prop=dps_prop, cd=cdm, range=rng, ev=['%s.AbilityChannelTime=%g' % (a.cls, ch), '%s interrupting=%s' % (a.cls, intr)], grade='DATA'))
    # area / zone that needs occupants
    dur = a.p('AbilityDuration', 3) or 0
    aura = next((a.p(p, 3) for p in ('AuraRadius', 'GroundAuraRadius', 'ModifierRadius', 'Radius', 'ShockRadius') if a.has(p) and a.p(p, 3)), None)
    if (dps and dur >= 2.0 and aura) or (dps and 'CITADEL_ABILITY_BEHAVIOR_CHANNELLED' in a.behaviors and aura):
        N.append(dict(base, kind='zone_occupancy', radius=aura, duration=dur or ch, dps=dps, dps_prop=dps_prop, cd=cdm, anchored=('CITADEL_ABILITY_BEHAVIOR_CHANNELLED' in a.behaviors or rng == 0), ev=['%s DPS=%g radius=%g dur=%g' % (a.cls, dps, aura, dur or ch)], grade='DATA'))
    # short-range damage (needs the target close)
    if 0 < rng <= 11 and (dmg or dps):
        N.append(dict(base, kind='short_range', range=rng, damage=dmg, dmg_prop=dmg_prop, dps_prop=dps_prop, cd=cdm, ev=['%s.AbilityCastRange=%g' % (a.cls, rng)], grade='DATA'))
    # conditional bonuses
    conds = {}
    for st, rx in CONDITIONS:
        for p in props:
            if re.search(rx, p) and tier_first(a, p) is not None:
                conds.setdefault(st, []).append('%s.%s=%g' % (a.cls, p, a.p(p, 3)))
    for st, rx in COND_TEXT:
        m = re.search(rx, txt)
        if m and st not in conds:
            conds.setdefault(st, []).append('%s text "%s"' % (a.cls, m.group(0)))
    for st, ev in conds.items():
        grade = 'DATA' if '=' in ev[0] else 'TEXT'
        N.append(dict(base, kind='conditional_' + st, state=st, ev=ev[:3], grade=grade, damage=dmg, cd=cdm))
    # self cost
    for p in props:
        if SELFDMG.match(p) and (a.p(p, 3) or 0) > 0:
            N.append(dict(base, kind='self_cost', prop=p, amount=a.p(p, 3), ev=['%s.%s=%g' % (a.cls, p, a.p(p, 3))], grade='DATA')); break
    return N

_off_cache = {}
def ability_offers_cache(a):
    k = (a.cls, a.tier)
    if k not in _off_cache: _off_cache[k] = ability_offers(a)
    return _off_cache[k]

class Kit:
    def __init__(self, hk):
        self.hk = hk
        self.name = G.hero_name(hk)
        self.abilities = G.hero_kit(hk, 3)
        self.stats = G.hero_stats(hk)
        wa = str(G.D().heroes[hk]['m_ShopStatDisplay']['m_eWeaponStatsDisplay'].get('m_eWeaponAttributes', ''))
        self.weapon_attrs = sorted(re.findall(r'EWeaponAttribute_(\w+)', wa))
        self.offers = []
        for a in self.abilities:
            self.offers += ability_offers_cache(a)
        for o in self.offers: o['hero'] = hk; o['hname'] = self.name
        self.needs = []
        for a in self.abilities:
            self.needs += ability_needs(a, hk)
        # weapon-driven needs
        if 'CloseRange' in self.weapon_attrs:
            self.needs.append(dict(kind='close_range_weapon', hero=hk, ability='weapon', aname='primary weapon', ev=['heroes.vdata %s weapon attr CloseRange' % hk], grade='DATA'))
        if 'LongRange' in self.weapon_attrs:
            self.needs.append(dict(kind='long_range_weapon', hero=hk, ability='weapon', aname='primary weapon', ev=['heroes.vdata %s weapon attr LongRange' % hk], grade='DATA'))
        has_move = any('CITADEL_ABILITY_BEHAVIOR_MOVEMENT' in a.behaviors for a in self.abilities)
        if not has_move:
            self.needs.append(dict(kind='no_signature_mobility', hero=hk, ability='kit', aname='kit', ev=['no signature ability with BEHAVIOR_MOVEMENT'], grade='DATA'))
        self.hp = self.stats.get('EMaxHealth')
        self.dmg_profile = {}

    def _damage_profile(self):
        """share of ability damage that scales with spirit vs weapon vs melee (from scale functions of damage-like props); coarse, used only to say which resist type matters."""
        sp = wp = ml = 0.0
        for a in self.abilities:
            for p, e in a.props0.items():
                if not re.search(r'Damage|DPS', p): continue
                sc = e.get('scale')
                s = str(sc)
                v = abs(a.p(p, 3) or 0)
                if not v: continue
                if 'ETechPower' in s: sp += v
                elif 'EBaseWeaponDamageIncrease' in s or 'EWeaponPower' in s: wp += v
                elif 'Melee' in s: ml += v
                else: sp += 0.0
        t = sp + wp + ml
        return dict(spirit=sp / t if t else None, weapon=wp / t if t else None, melee=ml / t if t else None)

    def has_offer(self, kind):
        return [o for o in self.offers if o['kind'] == kind]

def all_kits():
    return {hk: Kit(hk) for hk in G.hero_ids()}

if __name__ == '__main__':
    import collections
    K = all_kits()
    c = collections.Counter()
    nn = collections.Counter()
    for k in K.values():
        for o in k.offers: c[o['kind']] += 1
        for n in k.needs: nn[n['kind']] += 1
    print(sorted(c.items(), key=lambda x: -x[1]))
    print(sorted(nn.items(), key=lambda x: -x[1]))
