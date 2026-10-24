#!/bin/bash
# crafted pass/fail cases for the STRATEGY and INTERACTION gate rules (gate.js check only; never apply). Run from anywhere.
SP=$(cd "$(dirname "$0")/../../.." && pwd); cd "$SP"; T=council/work/strategy_tests; ST=council/evidence/strategy; IE=council/evidence/interaction
mk(){ # name buildFile evidenceJSON [waiveJSON]
 printf '{"id":"%s","buildFile":"%s","reason":"%s","evidence":%s%s}\n' "$1" "$2" "crafted gate test case for the strategy/interaction rules (not a real proposal)" "$3" "${4:+,\"waive\":$4}" > $T/$5.json; }
D='{"path":"gt/repo/game/citadel/pak01_dir/scripts/abilities.vdata","kind":"data"}'
node $T/path_to_build.js billy_damage $ST/billy_damage_lane_sustain.txt $T/billy_damage_chosen.js >/dev/null
A4=$(grep -E '^- A4 ' -A1 $ST/billy_damage_lane_sustain.txt | grep PATH | sed 's/^ *PATH: //; s/@[0-9]*//g')
node $T/path_to_build.js billy_damage "path:$A4" $T/billy_damage_A4.js >/dev/null
W3=$(grep -E '^- A3 ' -A1 $ST/wraith_greens_vs_ricochet.txt | grep PATH | sed 's/^ *PATH: //; s/@[0-9]*//g')
node $T/path_to_build.js wraith "path:$W3" $T/wraith_A3.js >/dev/null
sed 's/^CONCLUSION: .*/CONCLUSION: CHOSEN: A4/' $ST/billy_damage_lane_sustain.txt > $T/billy_damage_EDITED_strategy.txt
HZ=$(node -e "const fs=require('fs');const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();const b=B.find(x=>x.id==='haze');const m=b.rows.flat().find(x=>/^Mid/.test(x[0]));m[3].splice(1,0,['Close Quarters','']);fs.writeFileSync('$T/haze_plus_cq.js',JSON.stringify(b));")
mk billy_damage $T/billy_damage_chosen.js "[$D,{\"path\":\"$ST/billy_damage_lane_sustain.txt\",\"kind\":\"strategy\"}]" "" G1_pass_chosen_path
mk billy_damage $T/billy_damage_chosen.js "[$D]" "" G2_fail_no_strategy
mk billy_damage $T/billy_damage_A4.js "[$D,{\"path\":\"$ST/billy_damage_lane_sustain.txt\",\"kind\":\"strategy\"}]" "" G3_fail_path_mismatch
mk wraith $T/wraith_A3.js "[$D,{\"path\":\"$ST/wraith_greens_vs_ricochet.txt\",\"kind\":\"strategy\"}]" "" G4_fail_insufficient
mk billy_damage $T/billy_damage_chosen.js "[$D,{\"path\":\"$T/billy_damage_EDITED_strategy.txt\",\"kind\":\"strategy\"}]" "" G5_fail_edited_file
mk billy_damage $T/billy_damage_chosen.js "[$D]" "[{\"rule\":\"STRATEGY\",\"why\":\"crafted waiver test: computed comparison cited as the evidence file\",\"evidence\":\"$ST/billy_damage_lane_sustain.txt\"}]" G6_waived
mk haze $T/haze_plus_cq.js "[$D,{\"path\":\"$IE/haze_close_quarters_12000.txt\",\"kind\":\"interaction\"}]" "" I1_pass_interaction_cited
mk haze $T/haze_plus_cq.js "[$D]" "" I2_fail_no_interaction
for c in G1_pass_chosen_path G2_fail_no_strategy G3_fail_path_mismatch G4_fail_insufficient G5_fail_edited_file G6_waived I1_pass_interaction_cited I2_fail_no_interaction; do
 node council/tools/gate.js check $T/$c.json > $T/$c.out 2>&1
 echo "== $c: $(grep -h '^RESULT' $T/$c.out)"; grep -hE '^(STRATEGY|INTERACTION|BLOCK STRATEGY|BLOCK INTERACTION|WARN WAIVED STRATEGY|WARN INTERACTION)' $T/$c.out | cut -c1-260
 echo "   other blocks: $(grep -c '^BLOCK' $T/$c.out) total BLOCK lines"; done
# weakness rule (15:19): weakness-justified proposals need a remedy set; NO FIX NEEDED blocks the purchase
WK=council/evidence/weakness
node -e "const fs=require('fs');const B=new Function(fs.readFileSync('data.js','utf8')+';return B')();
 const h=B.find(x=>x.id==='haze');h.rows.flat().find(x=>/^Mid/.test(x[0]))[3].splice(0,0,['Weapon Shielding','']);fs.writeFileSync('$T/haze_plus_ws.js',JSON.stringify(h));
 const b=B.find(x=>x.id==='billy_damage');b.rows.flat().find(x=>/^Mid/.test(x[0]))[3].splice(0,0,['Enduring Speed','']);fs.writeFileSync('$T/billy_plus_es.js',JSON.stringify(b));"
printf '{"id":"haze","buildFile":"%s","reason":"Add Weapon Shielding to fix the ammo weakness found by the remedy set (crafted gate test)","weakness":"ammo","evidence":[%s,{"path":"%s","kind":"weakness"}]}\n' "$T/haze_plus_ws.js" "$D" "$WK/haze_ammo_12000.txt" > $T/W1_weakness_cited.json
printf '{"id":"haze","buildFile":"%s","reason":"Add Weapon Shielding to fix the ammo weakness (crafted gate test, no remedy set cited)","weakness":"ammo","evidence":[%s]}\n' "$T/haze_plus_ws.js" "$D" > $T/W2_weakness_no_file.json
printf '{"id":"billy_damage","buildFile":"%s","reason":"Add Enduring Speed to fix the reach problem (crafted gate test; remedy set says no fix needed)","weakness":"reach","evidence":[%s,{"path":"%s","kind":"weakness"}]}\n' "$T/billy_plus_es.js" "$D" "$WK/billy_damage_reach_7200.txt" > $T/W3_weakness_nofix.json
for c in W1_weakness_cited W2_weakness_no_file W3_weakness_nofix; do node council/tools/gate.js check $T/$c.json > $T/$c.out 2>&1
 echo "== $c: $(grep -h '^RESULT' $T/$c.out)"; grep -hE '^(WEAKNESS|BLOCK WEAKNESS)' $T/$c.out | cut -c1-260; done
