#!/usr/bin/env python3
"""Lint scenario .txt files for the experiment-metadata contract (mirrors Display.cs MetaLint + consistency).
usage: lint_meta.py file.txt [...]   exit 1 if any fails. Rules:
 - meta kind in BASELINE|ISOLATED ITEM|PURCHASE CHECKPOINT|COMPLETE BUILD; question, purpose, mechanics, expectedstate present
 - ISOLATED ITEM: meta excluded (what is excluded and why)
 - COMPLETE BUILD / PURCHASE CHECKPOINT: meta build + checkpoint; every `give` item must be declared in meta items (and items must all be given)
 - BASELINE: expectedstate has items=none and no `give` lines
 - ISOLATED ITEM: declared items == items given in the scenario
 - SCOPE of tested item(s) must be consistent: undeclared `give` = FAIL
"""
import re, sys
KINDS = {"BASELINE", "ISOLATED ITEM", "PURCHASE CHECKPOINT", "COMPLETE BUILD", "INTERACTION"}   # INTERACTION: item x kit cell test request from abtimeline.py --interactions (build + checkpoint + strategy_source required)
def lint(path):
    meta, gives = {}, set()
    for ln in open(path, errors="replace"):
        l = ln.split('#')[0].strip()
        if l.startswith("meta "):
            r = l[5:].strip(); k, _, v = r.partition(' ')
            meta[k.lower()] = (meta.get(k.lower(), "") + " " + v).strip()
        m = re.match(r"give\s+(\S+)", l)
        if m: gives.add(m.group(1))
    errs = []
    kind = meta.get("kind", "").upper()
    if kind not in KINDS: return ["meta kind missing/invalid"]
    for k in ("question", "purpose", "mechanics", "expectedstate"):
        if len(meta.get(k, "")) < 3: errs.append(f"meta {k} missing")
    decl = set(re.split(r"[,\s]+", meta.get("items", "").replace("none", ""))) - {""}
    decl = {d for d in decl if d.startswith("upgrade_")}
    if kind == "ISOLATED ITEM" and len(meta.get("excluded", "")) < 10: errs.append("ISOLATED ITEM needs meta excluded")
    if kind in ("COMPLETE BUILD", "PURCHASE CHECKPOINT", "INTERACTION"):
        for k in ("build", "checkpoint"):
            if not meta.get(k): errs.append(f"{kind} needs meta {k}")
    if kind == "BASELINE":
        if not re.search(r"items=(0|none)", meta.get("expectedstate", "")): errs.append("BASELINE expectedstate must say items=none")
        if gives: errs.append(f"BASELINE must not give items: {sorted(gives)}")
    if kind != "BASELINE":
        if gives - decl: errs.append(f"gives undeclared in meta items: {sorted(gives - decl)}")
        if decl - gives: errs.append(f"meta items never given: {sorted(decl - gives)}")
    # plain-English display contract (mirrors Display.cs MetaLint)
    pc = "BUILD" if (kind in ("COMPLETE BUILD", "PURCHASE CHECKPOINT", "INTERACTION") or meta.get("feeds")) else "CALIBRATION"
    if kind == "INTERACTION" and len(meta.get("result_says", "")) < 10: errs.append("INTERACTION needs meta result_says (what result means WORKS / DOES NOT WORK)")
    # selection provenance + intended setup conditions + readbacks (Kieran 15:16/15:19): pre-registered, verified by the runner
    if kind == "INTERACTION" or pc == "BUILD":
        sk = meta.get("selection_kind", "").split()[0] if meta.get("selection_kind") else ""
        if kind == "INTERACTION" and sk not in ("build-decision", "discovery", "weakness-remedy", "requested", "calibration"): errs.append("meta selection_kind missing/invalid (build-decision|discovery|weakness-remedy|requested|calibration)")
        if kind == "INTERACTION" and len(meta.get("selection_reason", "")) < 20: errs.append("meta selection_reason missing (why these items/hero were chosen, written before the run)")
        if kind == "INTERACTION":
            for k in ("cond_scope", "cond_targets", "cond_distance", "cond_activations", "readbacks"):
                if len(meta.get(k, "")) < 3: errs.append(f"meta {k} missing (intended condition the runner must verify)")
    for k in ("player_title", "player_what", "player_why", "player_short", "player_expect"):
        v = meta.get(k, "")
        for part in v.split("|"):
            lim = 26 if k == "player_short" else 32
            if len(part.strip()) > lim: errs.append(f"meta {k} part '{part.strip()}' is {len(part.strip())} chars, max {lim}")
        if pc == "BUILD" and k != "player_expect" and len(v) < 5: errs.append(f"paused-needs-design: {k} missing (plain English from planner/theorycrafter)")
        if pc == "CALIBRATION" and k in ("player_title", "player_what", "player_why") and len(v) < 5: errs.append(f"WARN-calibration without {k}: screen will show a plain factual line only")
    if pc == "BUILD" and len(meta.get("strategy_source", "")) < 5: errs.append("paused-needs-design: strategy_source missing (planner/theorycrafter file)")
    if kind == "ISOLATED ITEM" and pc == "BUILD" and len(meta.get("feeds", "")) < 10: errs.append("isolated item inside a build investigation needs meta feeds")
    # planner fields for range / spacing / movement experiments (PLANNER_FIELDS.md): clean-state and A-B-A control are mandatory when any of them is present
    if any(k in meta for k in ("ranges", "layout", "movement")):
        for k in ("required_start_state", "aba", "order_alternation", "invalid_if", "ranges", "layout", "movement"):
            if len(meta.get(k, "")) < 3: errs.append(f"range/layout/movement request needs meta {k}")
        if re.search(r"strafe|moving", meta.get("movement", ""), re.I) and "blocked_by" not in meta: errs.append("moving-target request must carry meta blocked_by (runner has no enemy-movement op) or name the op that exists")
        if "statecheck" not in " ".join(open(path, errors="replace").read().split()) and "hardreset" not in open(path, errors="replace").read(): errs.append("range/layout request has no hardreset/statecheck (clean-state control)")
    return errs
bad = 0
for p in sys.argv[1:]:
    e = lint(p)
    warn = [x for x in e if x.startswith("WARN")]; e = [x for x in e if not x.startswith("WARN")]
    print(("FAIL " if e else "PASS ") + p + ("  " + "; ".join(e) if e else "") + ("  [" + "; ".join(warn) + "]" if warn else ""))
    bad += bool(e)
sys.exit(1 if bad else 0)
