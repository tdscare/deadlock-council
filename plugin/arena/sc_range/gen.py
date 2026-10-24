import os
PRO = """raw citadel_unlock_flex_slots
aimoff 0 0
setgold 0
wait 0.4
lvlhold 18
wait 1.2
egod
eresist gun 0
eresist spirit 0
aimpt -33 -30
accoff
wait 0.8
heal
"""
def head(kind, title, q, purpose, mech, items, excl, pt, pw, pwhy, ps, pe, extra=""):
    return f"""meta hero Haze
meta kind {kind}
meta checkpoint Level 18 stat floor, 0 souls spent, items given per block
meta build none (mechanic discovery)
meta items {items}
meta question {q}
meta purpose {purpose}
meta mechanics {mech}
meta excluded {excl}
meta assumed none
meta levels_mode isolated
meta expectedstate items=none at start of every block
meta accmode body-only
meta accwhy hit counts are verified per block
meta abilities gun only
meta runs 1/1
meta cond_start_stacks fresh pawn every block
meta player_title {pt}
meta player_what {pw}
meta player_why {pwhy}
meta player_short {ps}
meta player_expect {pe}
{extra}setup Haze Haze
basemods
mark none
"""
def block(tag, give, place, secs, rep, minhit=0):
    s = "hardreset\n" + PRO
    for g in give: s += f"give {g}\n"
    s += place + "wait 0.5\nhealreset\nrngreset\n" + f"mark {tag}\nfire {secs}\nmark none\n"
    if give: s += "moddump me\n"
    s += f"rngreport {rep}" + (f" minhit={minhit}" if minhit else "") + "\nwait 0.5\n"
    return s

# S1 Close Quarters sweep
D = [60,150,300,450,500,540,580,620,700,900,1300]
t = head("ISOLATED ITEM","","Does Close Quarters add damage inside its range and nothing outside, and where is the edge?","measure the item activation edge in game units with verified distances; not a build verdict","range-gated gun damage; Haze gun only, no abilities","upgrade_close_range","all abilities and all other items; says nothing about a full build","Haze: Close Quarters range","Damage at 11 distances","Finding where the bonus stops","Close Quarters range","Bonus near, none far")
arms = []
for d in D:
    p = f"rng {d} 20\n"
    arms.append(("A_none",[],d)); arms.append(("B_cq",["upgrade_close_range"],d))
for tag,give,d in arms:
    t += block(f"RNG|{tag}|{d}u|body", give, f"rng {d} 20\n", 2.0, f"{tag} {d}u", 85)
# A-B-A repeats
for d in (150,580):
    t += block(f"RNG|A_none_rep|{d}u|body", [], f"rng {d} 20\n", 2.0, f"A_none_rep {d}u", 85)
t += "rngsummary\nmark none\nend\n"
open("rng_cq_haze.txt","w").write(t)

# S2 multi-target Ricochet
L = [("1_target",1,350,0),("3_tight",3,350,150),("3_medium",3,350,400),("5_tight",5,350,150),("5_medium",5,350,400),("5_wide",5,350,800)]
t = head("ISOLATED ITEM","","Does Ricochet reach more enemies when they stand closer together, and what does that add?","measure real bounce hits per target for different enemy counts and spacings; not a build verdict","bullet bounce to nearby enemies; per-target damage, no double counting","upgrade_ricochet","all abilities and all other items; says nothing about a full build","Haze: Ricochet and spacing","Targets hit by layout","Does spacing change its value?","Ricochet vs enemy spacing","Fewer hits when spread")
for name,n,d,sp in L:
    for tag,give in (("A_none",[]),("B_rico",["upgrade_ricochet"]),("A_none_rep",[])):
        t += block(f"MT|{tag}|{name}|body", give, f"layout {n} {d} {sp}\n", 4.0, f"{tag} {name}")
t += "rngsummary\nmark none\nend\n"
open("rng_multi_ricochet_haze.txt","w").write(t)

# S3 moving target
S = [("static",None),("strafe150_2s",(150,2)),("strafe250_1.5s",(250,1.5)),("static_rep",None)]
t = head("ISOLATED ITEM","","How much of Haze's gun fire still hits a target that strafes left and right?","measure hit rate and useful damage against stationary and strafing targets; misses are not damage","teleport-driven strafing of the dummy; camera tracks the target","none","all items and abilities; strafing is a teleport sequence, not a real player's movement","Haze: gun vs moving target","Hit rate when strafing","Misses are not damage","Moving target hit rate","Lower hit rate")
for name,sp in S:
    place = "layout 1 350 0\n" + (f"strafe {sp[0]} {sp[1]}\n" if sp else "strafe off\n")
    t += block(f"MV|{name}|body", [], place, 4.0, f"{name}")
t += "strafe off\nrngsummary\nmark none\nend\n"
open("rng_strafe_haze.txt","w").write(t)

# S4 persistent stack contamination demo (Haze Fixation stacks)
t = head("ISOLATED ITEM","","Do Haze's built-up Fixation stacks survive without a reset, and does the reset really clear them?","prove with log evidence that the next measurement starts from a clean state; not a build verdict","stacking_damage stacks read from the first damage row of each block","none","all items; harness state-contamination check","Tester check: leftover stacks","Stacks with and without reset","Checking the tester, not a build","Harness: stack reset proof","Stacks 1 after reset")
t += "hardreset\n"+PRO+"layout 1 350 0\nwait 0.5\nhealreset\nhzarm\nmark ST|build_stacks|body\nfire 8\nmark none\n"
t += "hzarm\nmark ST|control_no_reset|body\nfire 0.8\nmark none\n"
t += "hardreset\n"+PRO+"layout 1 350 0\nwait 0.5\nhealreset\nstatecheck items=none mods=none cdready=1 charges=1\nmark ST|after_reset|body\nfire 0.8\nmark none\nwait 0.5\nend\n"
open("state_stacks_haze.txt","w").write(t)
