// builds kind:strategy scenario JSONs from a strategy file (fields copied, arms = complete path state at a checkpoint) + crafted lint pass/fail cases
const fs=require('fs'),path=require('path');const SP=path.resolve(__dirname,'../../..');process.chdir(SP);
const h=(t,k)=>(t.match(new RegExp('^'+k+':\\s*(.*)$','m'))||[])[1];
function owned(t,alt,cp){const l=t.split('\n').find(x=>x.startsWith('  '+alt+' @'+cp+': '));return l.split(': ').slice(1).join(': ').split(' | ')[0].split(', ').map(x=>x.replace(/\[.*$/,'').trim()).filter(Boolean)}
function scen(sf,id,cp,altB,extra){const t=fs.readFileSync(sf,'utf8');const b=h(t,'BUILD'),hero=h(t,'HERO');const top=altB||(h(t,'BASIS').match(/^(\S+)/)||[])[1];
 const alts=h(t,'ALTERNATIVES').split(';').map(x=>x.trim());const pick=alts.filter(a=>a.startsWith('A0 ')||a.startsWith(top+' '));
 return Object.assign({id,title:hero+': as-built path vs '+top+' at '+cp+' souls (strategy test, complete path states)',hero,playstyle:'',builds:[b],kind:'strategy',
  question:h(t,'QUESTION'),hypothesis:h(t,'HYPOTHESIS'),alternatives:pick,tradeoffs:h(t,'TRADEOFFS').split(' | ').filter(x=>x.startsWith(top+' ')),
  missing_evidence:h(t,'MISSING_EVIDENCE').split(' | '),strategy_file:path.relative(SP,sf),
  arms:[{name:'A0',alt:'A0',souls:cp,items:owned(t,'A0',cp),ability_order:null,notes:'complete A0 state at the checkpoint (strategy file)'},{name:top,alt:top,souls:cp,items:owned(t,top,cp),ability_order:null,notes:'complete '+top+' state'}],
  setup:{level_or_boons:'abil bits from the strategy file tiers at the checkpoint',souls:cp,position:'shoot-back lane trade (GAPS 6/17 ops needed): enemy Haze bot 350u firing back',enemies:[{hero:'Haze',count:1,items:'reference enemy at the same souls',behaviour:'shoot back',hp:'finite (ehp)'}],allies:[],start_hp:'full',resets:['hardreset']},
  controls:['same enemy and position','arms interleaved A,B,B,A','real ability tiers at the checkpoint (no unlock-all)'],
  procedure:['give the arm items','trade 8 s with the shoot-back enemy, measure damage dealt, damage taken, healing, HP left','rest 22 s, measure HP recovered','repeat 5 cycles'],
  trials:5,metrics:[{name:'trade_ratio',unit:'ratio',how:'time-to-die / time-to-kill from the measured damage rates',grade_target:'B',better:'higher',primary:true},{name:'net_hp_per_cycle',unit:'hp',how:'HP after rest minus HP before trade',grade_target:'B',better:'higher',primary:false}],
  decision:{metric:'trade_ratio',min_effect_pct:5,min_trials:5,rule:'SUPPORTS the strategy file if '+top+' beats A0 by >=5% with non-overlapping ranges; REFUTES if reverse; else INCONCLUSIVE'}},extra||{})}
const ST='council/evidence/strategy/';const O='council/sandbox/scenarios/';const C='council/work/strategy_tests/scen/';fs.mkdirSync(C,{recursive:true});
const w=scen(ST+'wraith_greens_vs_ricochet.txt','wraith_strategy_greens_vs_ricochet',9600,'A3');fs.writeFileSync(O+w.id+'.json',JSON.stringify(w,null,1));
const b=scen(ST+'billy_damage_lane_sustain.txt','billy_damage_strategy_lane_sustain',7200,null);fs.writeFileSync(O+b.id+'.json',JSON.stringify(b,null,1));
// crafted lint cases
const put=(n,o)=>fs.writeFileSync(C+n+'.json',JSON.stringify(o,null,1));
put('L1_pass_strategy',b);
put('L2_fail_no_strategy_file',Object.assign({},b,{id:'L2',strategy_file:undefined}));
put('L3_fail_posthoc',Object.assign({},b,{id:'L3',run_started:'2026-10-24T00:00:00Z'}));
put('L4_fail_edited_file',Object.assign({},b,{id:'L4',strategy_file:'council/work/strategy_tests/billy_damage_EDITED_strategy.txt'}));
const bad=JSON.parse(JSON.stringify(b));bad.id='L5';bad.arms[1].items=bad.arms[1].items.slice(1);put('L5_fail_arm_not_complete_state',bad);
put('L6_pass_isolated',{id:'L6',title:'Rapid Rounds alone on a dummy. ISOLATED: does not justify the overall build',hero:'Haze',builds:['haze'],kind:'isolated',question:'fire rate datum',arms:[]});
put('L7_fail_isolated_unlabelled',{id:'L7',title:'Rapid Rounds alone on a dummy',hero:'Haze',builds:['haze'],kind:'isolated',question:'fire rate datum',arms:[]});
put('L8_fail_complete_build_no_strategy',{id:'L8',title:'complete build test',hero:'Haze',builds:['haze'],kind:'complete-build',question:'does the build work end to end?',hypothesis:'it does',arms:[]});
console.log('ok', w.arms.map(a=>a.items.length), b.arms.map(a=>a.items.length));
