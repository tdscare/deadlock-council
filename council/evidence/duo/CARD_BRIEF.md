# Duo synergy cards — brief (stage A)

NOTE: every example below is an off-the-cuff guess from Kieran, not a conclusion and not a target. Decide only from kit numbers; reject pairs that fail on radius/duration/timing.

Goal: Kieran wants DUO builds: two heroes played together whose builds are tuned to each other's kits (e.g. Dynamo's ult stuns in a small radius and Ivy's ult flies people around to extend it; Mo & Krill's ult holds a target so Bebop can hook it, with Hunter's Aura / Bullet Resist Shredder and damage-over-time items like Alchemical Flask on the floor). Everything must come from the kit numbers, not from public duo lists.

Your job (stage A): for EACH hero in your group, read its kit file (path list in your prompt; ability text + raw stats + upgrades; extra data via `python3 -I ab.py <ability_class>` and `python3 -I audit_D_q.py "<item>"` from SP). Write ONE JSON file `council/evidence/duo/cards_g<N>.json`: an object keyed by the file's hero name, each with:

```
{ "hero": "Dynamo", "file": "audit/hero_dynamo.txt",
  "setup": [ {"ability":"3 Quantum Entanglement","effect":"stun|root|slow|pull|lift|knockdown|silence|disarm|sleep|hold|tether|zone|blind|taunt|bullet-resist-shred|debuff","duration_s":N,"radius_m":N,"range_m":N,"cooldown_s":N,"needs_partner_to":"what a partner must do for this to land","notes":"exact text/number evidence"} ],
  "payoff": [ {"ability_or_item":"...","needs":"stationary|cc'd|low bullet resist|clumped|in zone|debuffed|marked|low hp|...","window":"how long the target must stay / how large an area is needed","numbers":"damage/heal numbers that the setup unlocks"} ],
  "ally_effects": [ {"ability":"...","what":"buff|heal|shield|lift|teleport|speed|resource|cooldown","range_m":N,"duration_s":N,"numbers":"..."} ],
  "item_hooks": [ {"item":"...","why":"what partner behaviour makes this item better on THIS hero (e.g. ally auras, DoT zone, stationary target)"} ],
  "extends_or_is_extended_by": "kit pieces whose radius/duration/range a partner could extend or that extend a partner"
}
```

Rules: every number cites the file text/stat. If a claim is uncertain (e.g. whether a lift keeps stun active) write "unverified" with what you'd need. No hero-wide popularity claims. Be compact: this is a lookup table for matching setup↔payoff across heroes, not an essay. Reply with only the output path and a one-line count.
