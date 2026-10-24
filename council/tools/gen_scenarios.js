// regenerates sandbox/scenarios/*.json  (node council/tools/gen_scenarios.js)
//   node council/tools/gen_scenarios.js --lint [scenario.json ...]   LINT ONLY (no regeneration; default = every scenarios/*.json; exit 1 if any item-comparison fails)
// Item-comparison scenario (arms differ in items/swaps) must test the ITEM INSIDE THE COMPLETE BUILD at a checkpoint (Kieran 12:26), declared as
//   build_context:{build, checkpoint_souls, compared:[item names], owned:[ALL items held at the checkpoint], ability_tiers:{"1":"T3",...}, imbues:{item:slot},
//                  actives_cast:[relevant actives/abilities the procedure casts], actives_not_cast:{name:reason} (optional, explicit)}
// and the lint checks it against the build walk (abtimeline.py --state): owned set, real ability tiers (no `unlock 7`), every owned imbue item imbued,
// every relevant active (same need family as the compared item, or imbue items; hero abilities with the same effect, e.g. Quicksilver Reload, Full Auto) is
// cast in the procedure. Scenarios with empty arms are templates (exempt until filled).
// Experiment kind (Kieran 13:56, SCHEMA.md): kind baseline|isolated|checkpoint|complete-build|strategy. kind isolated must say "ISOLATED: does not justify the overall build".
// kind strategy|complete-build with builds[] (= claims to inform a build decision) must cite strategy_file = an unedited `abtimeline.py --strategy` file for one of its builds,
// GENERATED before any run of the scenario (results files / queue task start), with question, hypothesis, alternatives, tradeoffs, missing_evidence; strategy arms name an
// alternative (arm.alt) and hold exactly that alternative's items at arm.souls (a CHECKPOINT of the strategy file).
const fs=require('fs'),D=__dirname+'/../sandbox/scenarios/';
if(process.argv.includes('--lint')){const cp=require('child_process'),path=require('path'),SPR=path.resolve(__dirname,'../..');
 const files=process.argv.slice(2).filter(x=>x!=='--lint');const list=files.length?files:fs.readdirSync(D).filter(f=>f.endsWith('.json')).map(f=>D+f);
 const IF=JSON.parse(fs.readFileSync(SPR+'/audit/items_full.json','utf8'));const byClass={};for(const[n,g]of Object.entries(IF))byClass[g.class]=n;
 const nm=x=>byClass[x]||x;let fails=0,tmpl=0,ok=0;
 for(const f of list){const s=JSON.parse(fs.readFileSync(f,'utf8')),id=path.basename(f),errs=[];
  const KINDS=['baseline','isolated','checkpoint','complete-build','strategy'];
  if(s.kind!==undefined&&!KINDS.includes(s.kind))errs.push('kind "'+s.kind+'" must be one of '+KINDS.join('|'));
  if(s.kind===undefined)console.log('  NO-KIND (legacy; add kind):',id);
  const blob=JSON.stringify([s.title,s.question,s.hypothesis,s.notes,s.isolated_note]);
  if(s.kind==='isolated'&&!/ISOLATED: does not justify the overall build/.test(blob))errs.push('kind isolated must state "ISOLATED: does not justify the overall build" (title/question/hypothesis/notes)');
  const informs=Array.isArray(s.builds)&&s.builds.length>0;
  if((s.kind==='strategy'||s.kind==='complete-build')&&informs){
   for(const k of ['question','hypothesis'])if(!s[k]||String(s[k]).length<10)errs.push(k+' missing');
   for(const k of ['alternatives','tradeoffs','missing_evidence'])if(!Array.isArray(s[k])||!s[k].length)errs.push(k+' missing (list from the strategy file)');
   const sf=s.strategy_file&&(fs.existsSync(s.strategy_file)?s.strategy_file:fs.existsSync(SPR+'/'+s.strategy_file)?SPR+'/'+s.strategy_file:null);
   if(!s.strategy_file)errs.push('claims to inform a build decision (builds '+s.builds.join(',')+') but cites no strategy_file (abtimeline.py --strategy)');
   else if(!sf)errs.push('strategy_file does not exist: '+s.strategy_file);
   else{const st=fs.readFileSync(sf,'utf8'),h=k=>(st.match(new RegExp('^'+k+':\\s*(.*)$','m'))||[])[1];
    if(h('KIND')!=='strategy')errs.push('strategy_file is not KIND: strategy');
    if(!s.builds.includes(h('BUILD')))errs.push('strategy_file BUILD '+h('BUILD')+' is not in builds '+s.builds.join(','));
    const v=cp.spawnSync('python3',['-I','council/tools/abtimeline.py','--verify-strategy',sf],{cwd:SPR,encoding:'utf8'});if(v.status!==0)errs.push('strategy_file BODY-SHA mismatch: edited after generation');
    const gen=Date.parse(h('GENERATED')||'');if(!gen)errs.push('strategy_file has no GENERATED time');
    const RD=SPR+'/council/sandbox/results/';const runs=fs.existsSync(RD)?fs.readdirSync(RD).filter(x=>x.includes('_'+s.id+'_')).map(x=>fs.statSync(RD+x).mtimeMs):[];
    try{const Q=JSON.parse(fs.readFileSync(SPR+'/council/sandbox/queue.json','utf8'));for(const tk of Q.tasks)if((tk.exp===s.id||tk.scenario===s.id)&&tk.started)runs.push(Date.parse(tk.started))}catch(x){}
    if(s.run_started)runs.push(Date.parse(s.run_started));
    if(gen&&runs.length&&Math.min(...runs)<gen)errs.push('strategy_file GENERATED '+h('GENERATED')+' AFTER the first run of this scenario ('+new Date(Math.min(...runs)).toISOString()+'): post-hoc, not pre-registered');
    const altNames=(h('ALTERNATIVES')||'').split(';').map(x=>x.trim().split(' ')[0]).filter(Boolean);
    for(const a of s.alternatives||[]){const n=String(a).split(' ')[0];if(!altNames.includes(n))errs.push('alternative "'+a+'" is not in the strategy file ('+altNames.join(',')+')')}
    if(s.kind==='strategy'){const cps=(h('CHECKPOINTS')||'').split(',').map(Number);
     for(const a of (s.arms||[])){if(!a.alt){errs.push('strategy arm "'+a.name+'" names no alt');continue}if(!altNames.includes(a.alt)){errs.push('arm alt '+a.alt+' not in strategy file');continue}
      const sv=+a.souls;if(!cps.includes(sv)){errs.push('arm '+a.name+' souls '+a.souls+' is not a strategy CHECKPOINT ('+cps.join(',')+')');continue}
      const line=st.split('\n').find(l=>l.startsWith('  '+a.alt+' @'+sv+': '));if(!line){errs.push('no owned-items line for '+a.alt+' @'+sv+' in the strategy file');continue}
      const own=line.split(': ').slice(1).join(': ').split(' | ')[0].split(', ').map(x=>x.replace(/\[.*$/,'').trim()).filter(Boolean);
      const got=(a.items||[]).map(nm);const miss=own.filter(x=>!got.includes(x)),extra=got.filter(x=>!own.includes(x));
      if(miss.length||extra.length)errs.push('arm '+a.name+' ('+a.alt+' @'+sv+') is not that path\'s complete state: missing '+(miss.join(', ')||'-')+'; extra '+(extra.join(', ')||'-'))}
     if(/unlock 7|all 3 tiers|all tiers/i.test(JSON.stringify([s.setup,s.controls,s.arms,s.procedure])))errs.push('uses `unlock 7`/all-tiers instead of the real ability tiers at the checkpoint');
     if(errs.length){fails++;console.log('FAIL',id);errs.forEach(e=>console.log('   -',e))}else{ok++;console.log('PASS',id,'(strategy, '+(s.arms||[]).length+' arms checked against '+path.basename(sf)+')')}
     continue}}}
  const arms=s.arms||[];const sets=arms.map(a=>Array.isArray(a.items)?a.items.map(nm):[]);const swaps=arms.flatMap(a=>Object.entries(a.swaps||{}).flat());
  const isBuildRef=arms.some(a=>typeof a.items==='string');
  const differs=swaps.length>0||(sets.length>=2&&JSON.stringify([...sets[0]].sort())!==JSON.stringify([...sets[1]].sort()))||isBuildRef;
  if(arms.length<2||!differs||(sets.every(x=>!x.length)&&!isBuildRef&&!swaps.length)){if(errs.length){fails++;console.log('FAIL',id);errs.forEach(e=>console.log('   -',e));continue}console.log('TEMPLATE/non-item-comparison (exempt):',id);tmpl++;continue}
  const bc=s.build_context;
  if(!bc){errs.push('no build_context: arms must run the complete build state at the checkpoint (owned items, ability tiers, imbues, relevant actives cast)')}
  else{for(const k of ['build','checkpoint_souls','compared','owned','ability_tiers','actives_cast'])if(bc[k]==null)errs.push('build_context.'+k+' missing');
   if(!errs.length){let st;try{st=JSON.parse(cp.execSync('python3 -I council/tools/abtimeline.py --state '+bc.build+' '+bc.checkpoint_souls+' "'+bc.compared.join(',')+'"',{cwd:SPR,stdio:['ignore','pipe','pipe']}).toString())}catch(x){errs.push('cannot compute build state: '+(x.stderr||x.message).toString().slice(0,120))}
    if(st){const exp=new Set(st.owned),got=new Set(bc.owned);const miss=[...exp].filter(x=>!got.has(x)&&!bc.compared.includes(x)),extra=[...got].filter(x=>!exp.has(x)&&!bc.compared.includes(x));
     if(miss.length)errs.push('build_context.owned is not the complete build at '+bc.checkpoint_souls+': missing '+miss.join(', '));if(extra.length)errs.push('build_context.owned has items not held at that checkpoint: '+extra.join(', '));
     for(const[sl,t]of Object.entries(st.tiers))if(t!=='L'&&bc.ability_tiers[sl]!==t)errs.push('ability tier slot '+sl+': build walk says '+t+', scenario says '+bc.ability_tiers[sl]);
     for(const[n,sl]of Object.entries(st.imbues))if(!bc.imbues||String(bc.imbues[n])!==String(sl))errs.push('owned imbue item '+n+' is not imbued to slot '+sl+' in build_context.imbues');
     const text=JSON.stringify([s.procedure,s.controls,s.setup]).toLowerCase();
     for(const a of st.relevant_actives){const has=(bc.actives_cast||[]).includes(a.name),waived=bc.actives_not_cast&&bc.actives_not_cast[a.name]&&bc.actives_not_cast[a.name].length>15;
      if(!has&&!waived)errs.push('relevant '+a.kind+' "'+a.name+'" (same effect family as the compared item) is not in actives_cast (or actives_not_cast with a reason)');
      else if(has&&!new RegExp('(cast|use|press|activate)[^"]{0,40}'+a.name.toLowerCase().replace(/[^a-z ]/g,'')).test(text))errs.push('"'+a.name+'" is listed in actives_cast but the procedure never casts it')}}}}
  if(/unlock 7|all 3 tiers|all tiers/i.test(JSON.stringify([s.setup,s.controls,s.arms,s.procedure])))errs.push('uses `unlock 7`/all-tiers instead of the real ability tiers at the checkpoint');
  if(errs.length){fails++;console.log('FAIL',id);errs.forEach(e=>console.log('   -',e))}else{ok++;console.log('PASS',id)}}
 console.log(`lint: ${ok} pass, ${fails} fail, ${tmpl} templates/non-item exempt, of ${list.length}`);process.exit(fails?1:0)}
const cat=n=>/heal|lifesteal|sustain|net_hp|charge/.test(n)?'healing':/surviv|hp_lost|damage_taken|death/.test(n)?'survivability':/dist|route|move/.test(n)?'mobility':/cast|cooldown|uptime/.test(n)?'cooldowns':/ttk|time_to_kill|first_kill/.test(n)?'burst damage':/clear|souls/.test(n)?'farming':/_30s|_60s|damage_dealt|enemy_hp|shots|kill/.test(n)?'sustained damage':'other';
const M=(name,unit,how,better,primary,g='B')=>({name,unit,how,category:cat(name),grade_target:g,better,primary:!!primary});
const S=[];
const add=o=>S.push(Object.assign({trials:5,controls:[],builds:[]},o));
const std=['Same position and spawn distance','Cooldowns and HP reset between trials','Same boons/souls/ability points in both arms except the item/order under test','Same enemy hero, level, items, behaviour'];
add({id:'victor_vs_three',title:'Victor brawling three enemies',hero:'Victor',playstyle:'Aura Brawler / gun hybrid',builds:['victor','victor_gun'],
 question:'Does Victor survive and win a 1v3 face-to-face fight better on the spirit Aura Brawler core or the gun hybrid core?',
 hypothesis:'Aura Brawler (Torment Pulse, Infuser) out-survives gun hybrid in 1v3 close fights; gun hybrid kills the first target faster.',
 arms:[{name:'aura_brawler',items:'build:victor core 12',ability_order:null,imbues:{},souls:'equal to core cost'},{name:'gun_hybrid',items:'build:victor_gun core 12',ability_order:null,imbues:{},souls:'equal to core cost'}],
 setup:{level_or_boons:'mid-game (~25k souls)',enemies:[{hero:'3 different ranged/melee mix (e.g. Haze, Seven, Abrams)',count:3,behaviour:'attack, no retreat'}],allies:[],start_hp:'full',resets:['hp','cooldowns','enemy positions']},
 conditions:[{name:'vs 3 enemies'}],controls:std,procedure:['Start 30m from enemies, all standing at spawn spots','Engage: Victor walks in and fights with normal rotation (1,2,3 as appropriate, ult when available)','Run until Victor dies, all enemies dead, or 40s','Record metrics at end'],
 metrics:[M('survival_time','s','time until death or 40s cap','higher',true),M('enemies_killed','count','kill count by end','higher',true),M('time_to_first_kill','s','','lower'),M('hp_lost_total','hp','sum of damage taken incl. healed','lower'),M('hp_healed','hp','total healing/lifesteal received','higher'),M('damage_dealt','hp','total damage to enemies','higher')],
 decision:{metric:'enemies_killed then survival_time',min_effect_pct:20,min_trials:5,rule:'arm B beats A on primary metrics with non-overlapping ranges'}});
add({id:'wraith_leech_vs_vampiric',title:'Wraith sustain: Leech vs Vampiric Burst with Ricochet',hero:'Wraith',playstyle:'Early farm then AoE gun',builds:['wraith'],
 question:'When Wraith shoots three targets with Ricochet bouncing, does Leech or Vampiric Burst give more sustain over a real fight window?',
 hypothesis:'Vampiric Burst gives more burst sustain per use (30s cooldown) but Leech gives more over a 30s window with sustained AoE bounces; the answer depends on target count.',
 arms:[{name:'leech',items:['Leech','Ricochet'],souls:'same spend; Vampiric Burst slot replaced with equal-cost filler',notes:'no Vampiric Burst'},{name:'vampiric_burst',items:['Vampiric Burst','Ricochet'],souls:'same spend',notes:'no Leech; use Vampiric Burst on cooldown'}],
 setup:{level_or_boons:'late (~35k souls)',enemies:[{hero:'bot hero w/ guns',count:3,behaviour:'stand in cluster within 12m, fire back'}],allies:[],start_hp:'60% so healing is measurable',resets:['hp to 60%','cooldowns']},
 conditions:[{name:'1 target'},{name:'2 targets'},{name:'3 targets'}],controls:std.concat(['Run every arm at each condition (1, 2, 3 targets in the cluster)']),
 procedure:['Start at 60% HP','Shoot the cluster with normal ability rotation for 30s','Use Vampiric Burst on cooldown in its arm only','Record'],
 metrics:[M('hp_healed_30s','hp','total heal over 30s','higher',true),M('net_hp_change_30s','hp','end HP minus start HP','higher',true),M('damage_dealt_30s','hp','','higher'),M('heal_per_damage','ratio','healed/damage','higher')],
 decision:{metric:'net_hp_change_30s',min_effect_pct:15,min_trials:5,rule:'run at targets=1,2,3 and report the crossover'}});
add({id:'harrow_burst_fire_ally',title:'Harrow: Burst Fire proccing on a teammate',hero:'Harrow',playstyle:'Friendly Fire Harrow',builds:['nurse'],
 question:'Does shooting an ally with Burst Fire raise healing-needle charge/throughput enough to beat Swift Striker?',
 hypothesis:'Burst Fire procs on allies (+32% fire rate for 4.5s, 9s cd) so needle charge from hits rises more than Swift Striker flat +20%.',
 arms:[{name:'burst_fire',items:['Burst Fire'],souls:'equal spend'},{name:'swift_striker',items:['Swift Striker'],souls:'equal spend'}],
 setup:{level_or_boons:'mid (~20k)',enemies:[],allies:[{hero:'any ally bot',count:1,role:'stands still, damaged to 50% HP'}],start_hp:'full',resets:['ally HP','cooldowns']},
 controls:std,procedure:['Ally at 50% HP 10m away','Harrow shoots ally with needles/bullets for 20s to charge Healing Needles; fire needle volley','Record time to full charge and heal delivered'],
 metrics:[M('time_to_full_charge','s','','lower',true),M('heal_delivered_20s','hp','','higher',true),M('shots_fired','count','','higher')],
 decision:{metric:'time_to_full_charge',min_effect_pct:10,min_trials:5,rule:'lower is better'},blockedIfNo:['allies spawnable']});
add({id:'haze_smoke_lifesteal_jumped',title:'Haze: lifesteal from smoke while jumped farming',hero:'Haze',playstyle:'Victor Cosplay Haze (tanky lifesteal)',builds:['haze'],
 question:'With gun items and lifesteal from Smoke Bomb, how much do the point-order choices (max Smoke vs max knife first) change survival when two enemies jump her at a camp?',
 hypothesis:'Smoke-first order survives longer than knife-first because smokes are the only sustain on an all-weapon build.',
 arms:[{name:'smoke_first',items:'build:haze core',ability_order:'Kieran order (Fixation,knife,Fixation,Smoke max,...)'},{name:'knife_first',items:'build:haze core',ability_order:'public order (knife max first)'}],
 setup:{level_or_boons:'mid',enemies:[{hero:'Wraith,Vindicta',count:2,behaviour:'attack Haze while she farms'}],start_hp:'full',resets:['camp respawn','hp','cooldowns']},
 controls:std,procedure:['Haze starts clearing a camp','At t=10s two enemies engage','Haze fights/escapes normally until death or 30s'],
 metrics:[M('survival_time','s','','higher',true),M('hp_healed','hp','','higher'),M('enemy_hp_removed','hp','','higher')],decision:{metric:'survival_time',min_effect_pct:20,min_trials:5,rule:'higher better'}});
add({id:'victor_sustain_three',title:'Victor sustain: Spirit Lifesteal vs Leech',hero:'Victor',playstyle:'Aura Brawler',builds:['victor'],
 question:'In real fights, does Leech out-sustain Spirit Lifesteal on the Aura Brawler core?',
 hypothesis:'Unresolved. Spirit Lifesteal scales with spirit damage dealt; Leech heals on damage dealt in melee/close range. Brawler pressure on 3 enemies decides it.',
 arms:[{name:'spirit_lifesteal',items:'build:victor core',swaps:{}},{name:'leech',items:'build:victor core',swaps:{'Spirit Lifesteal':'Leech'}}],
 setup:{level_or_boons:'mid-late (~30k souls)',enemies:[{hero:'mixed bot heroes',count:3,behaviour:'looped recorded attack; stay in melee range'}],allies:[],start_hp:'full',resets:['hp','cooldowns','enemy positions']},
 conditions:[{name:'1 enemy'},{name:'3 enemies'}],controls:std,procedure:['Victor engages with his normal rotation','Run 30s or until death','Record'],
 metrics:[M('hp_healed_30s','hp','sum of heal/lifesteal numbers or HP sampling','higher',true),M('survival_time','s','','higher'),M('damage_dealt_30s','hp','','higher'),M('hp_lost_total','hp','','lower')],
 decision:{metric:'hp_healed_30s',min_effect_pct:15,min_trials:5,rule:'higher better; report per condition'}});
add({id:'generic_ttk_burst',title:'Generic: time to kill a standard target',hero:'any',playstyle:'any burst/damage build',
 question:'Which item/order variant kills a standard target fastest using the hero\'s real combo?',hypothesis:'defined per use',arms:[{name:'A',items:[],souls:''},{name:'B',items:[],souls:''}],
 setup:{level_or_boons:'set per use',enemies:[{hero:'standard tanky bot',count:1,behaviour:'stationary'}],start_hp:'full',resets:['enemy hp','cooldowns']},controls:std,procedure:['Execute the hero\'s real opener and rotation','Stop at kill'],
 metrics:[M('time_to_kill','s','','lower',true),M('damage_dealt','hp','','higher')],decision:{metric:'time_to_kill',min_effect_pct:10,min_trials:5,rule:'lower better'}});
add({id:'generic_survive_focus',title:'Generic: time to die under focus fire',hero:'any',playstyle:'any',
 question:'How long does the build survive N attackers with and without a defensive item (Metal Skin, Bullet Resilience, Counterspell…)?',hypothesis:'defined per use',arms:[{name:'without',items:[],souls:''},{name:'with',items:[],souls:''}],
 setup:{level_or_boons:'set per use',enemies:[{hero:'3 attackers of the type the item counters',count:3,behaviour:'focus the hero'}],start_hp:'full',resets:['hp','cooldowns']},controls:std,procedure:['Hero uses defensive item/ability at the moment a real player would','Run until death or 30s'],
 metrics:[M('survival_time','s','','higher',true),M('damage_taken','hp','','lower')],decision:{metric:'survival_time',min_effect_pct:15,min_trials:5,rule:'higher better'}});
add({id:'generic_camp_clear',title:'Generic: farming speed',hero:'any',playstyle:'farm builds',
 question:'Does the farm item/order clear a standard camp faster (Ricochet, Mystic Shot, imbues)?',hypothesis:'defined per use',arms:[{name:'A',items:[],souls:''},{name:'B',items:[],souls:''}],
 setup:{level_or_boons:'early/mid',enemies:[{hero:'neutral camp',count:1,behaviour:'camp'}],start_hp:'full',resets:['camp respawn']},controls:std,procedure:['Clear the same camp from the same start point','Stop at last neutral death'],
 metrics:[M('clear_time','s','','lower',true),M('hp_lost','hp','','lower'),M('souls_gained','souls','','higher')],decision:{metric:'clear_time',min_effect_pct:10,min_trials:5,rule:'lower better'}});
add({id:'generic_mobility_course',title:'Generic: movement / escape',hero:'any',playstyle:'mobile / kiting',
 question:'How much do movement items/orders change distance covered or escape success?',hypothesis:'defined per use',arms:[{name:'A',items:[],souls:''},{name:'B',items:[],souls:''}],
 setup:{level_or_boons:'set per use',enemies:[{hero:'chaser bot',count:1,behaviour:'chase'}],start_hp:'full',resets:['positions']},controls:std,procedure:['Run a fixed marked route / flee from the chaser for 15s'],
 metrics:[M('distance','m','','higher',true),M('time_to_route_end','s','','lower'),M('damage_taken','hp','','lower')],decision:{metric:'distance',min_effect_pct:8,min_trials:5,rule:'higher better'}});
add({id:'generic_cooldown_uptime',title:'Generic: ability/imbue uptime',hero:'any',playstyle:'ability/imbue builds',
 question:'Which cooldown item or imbue placement gives more casts/damage over 60s?',hypothesis:'defined per use',arms:[{name:'A',items:[],souls:''},{name:'B',items:[],souls:''}],
 setup:{level_or_boons:'set per use',enemies:[{hero:'durable bot',count:1,behaviour:'stationary'}],start_hp:'full',resets:['cooldowns']},controls:std,procedure:['Cast the target ability on cooldown for 60s'],
 metrics:[M('casts_60s','count','','higher',true),M('damage_60s','hp','','higher',true)],decision:{metric:'damage_60s',min_effect_pct:10,min_trials:5,rule:'higher better'}});
add({id:'generic_dummy_numbers',title:'Generic: single-ability number check (stationary dummy)',hero:'any',playstyle:'any',
 question:'Does the in-game number match the calculated number (damage/heal/duration)?',hypothesis:'matches within 5%',arms:[{name:'calc_check',items:[],souls:''},{name:'observed',items:[],souls:''}],
 setup:{level_or_boons:'set per use',enemies:[{hero:'target dummy',count:1,behaviour:'stationary'}],start_hp:'full',resets:['dummy hp']},controls:std,procedure:['Use the ability once, record the number','Compare with the calculation'],
 metrics:[M('observed_value','number','','higher',true,'A')],decision:{metric:'observed_value',min_effect_pct:5,min_trials:5,rule:'report deviation from calculation'}});
S.forEach(s=>fs.writeFileSync(D+s.id+'.json',JSON.stringify(s,null,1)+'\n'));
console.log(S.length,'scenarios');
