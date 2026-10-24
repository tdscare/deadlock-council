// Build identity evidence: composition (what the purchases do), kit (what the hero's abilities do, from the effects extractor, read-only),
// classification, claim extraction (name/description/tags) and claim-vs-evidence lint. Evidence level is ALWAYS stated:
//   composition-only  = from the build's own items + ability order (no sandbox/behaviour data) -> role claims can be CONTRADICTED but rarely fully CONFIRMED
//   +sandbox          = at least one VALID build-context sandbox result for the build exists (stronger, still partial)
const C=require('./common');const {R,ROLES}=require('./roles');const {fs,path,SP}=C;
let EFF=null;function effects(){if(EFF)return EFF;try{EFF=JSON.parse(fs.readFileSync(path.join(SP,'council/evidence/interactions/effects/heroes.json'),'utf8')).heroes}catch(e){EFF={}}return EFF}
function composition(b,ctx){const sp={},spOpt={},who={};ROLES.forEach(r=>{sp[r]=0;spOpt[r]=0;who[r]=[]});let tot=0,totOpt=0;const unknown=[];
 for(const it of C.items(b)){const w=R[it.name];if(!w){unknown.push(it.name);continue}const t=ctx.ITEMS[it.name]?ctx.ITEMS[it.name].t:2,cost=C.COST[t];
  if(it.core&&!it.opt){tot+=cost;for(const r in w){sp[r]+=cost*w[r];if(w[r]>=.5)who[r].push(it.name)}}
  else if(!/^(Counters|Losing|Lost)/i.test(it.title)){totOpt+=cost;for(const r in w)spOpt[r]+=cost*w[r]}}
 const f={};for(const r of ROLES)f[r]=tot?sp[r]/tot:0;return {spend:sp,total:tot,frac:f,who,unknown,optionalSpend:totOpt}}
function kit(b){const H=effects()[b.hk];const out={available:!!H,abilities:[]};if(!H)return out;
 const slots={};for(const a of H.abilities){const e=a.effects||[];const p=e[0]&&e[0].producer;const slot=p&&p.slot;if(!/^[1-4]$/.test(String(slot||'')))continue;
  const txt=JSON.stringify(a.desc||{}).toLowerCase();
  slots[slot]={name:p.name,cc:e.some(x=>x.op==='apply_cc'&&/hard_cc|slow|silence|disarm|root|stun/.test(x.subtype)),heal:e.some(x=>x.op==='heal'),shield:e.some(x=>x.op==='absorb'),
   debuff:e.some(x=>x.op==='amplify'&&/vulnerab/.test(x.subtype)),dmg:/damage/.test(txt)||(a.behaviors||[]).includes('DISPLAYS_DAMAGE_IMPACT')}}
 out.abilities=[1,2,3,4].map(i=>slots[i]||null);
 // ability-point focus: weight earlier points more (point k of 16 weighs 1-(k/20))
 const ord=b.order||[];const w=[0,0,0,0,0];ord.forEach((a,k)=>{if(a)w[a]+=1-k/20});const tw=w.reduce((x,y)=>x+y,0)||1;
 let util=0,dmg=0;out.abilities.forEach((a,i)=>{if(!a)return;const x=w[i+1]/tw,u=a.cc||a.debuff||a.heal||a.shield;if(u&&a.dmg){util+=x/2;dmg+=x/2}else if(u)util+=x;else if(a.dmg)dmg+=x});
 out.focus=w.slice(1).map(x=>+(x/tw).toFixed(2));out.utilFocus=+util.toFixed(2);out.dmgFocus=+dmg.toFixed(2);return out}
function classify(b,ctx,hasSandbox){const c=composition(b,ctx),k=kit(b),f=c.frac;
 // ability-amplifier items (cooldown/duration/range/charges) are neutral: split by what the build's ability points actually go into (kit flags, point-weighted)
 const ks=k.available&&(k.utilFocus+k.dmgFocus)>0?k.utilFocus/(k.utilFocus+k.dmgFocus):.35,eU=f.enabler*ks,eD=f.enabler*(1-ks);
 const D=f.gun+f.spirit+f.melee+eD,U=f.cc+f.debuff+f.ally+eU,S=f.sustain+f.defense;
 const norm=D+U+S||1;const d=D/norm,u=U/norm,s=S/norm;
 const utilItems=new Set([...c.who.cc,...c.who.debuff,...c.who.ally]);
 const classes=[],why=[];
 if(u>=.40&&u>=d&&utilItems.size>=3){classes.push('support');why.push(`utility share ${pc(u)} >= damage ${pc(d)} with ${utilItems.size} utility items (${[...utilItems].join(', ')})`)}
 else if(u>=.22&&utilItems.size>=2){classes.push('damage-support hybrid');why.push(`utility share ${pc(u)} with ${utilItems.size} utility items (${[...utilItems].join(', ')}) beside damage ${pc(d)}`)}
 if(s>=.40){classes.push('sustain/tank fighter');why.push(`survival share ${pc(s)} (sustain ${pc(f.sustain)}, defence ${pc(f.defense)})`)}
 const gD=f.gun,sD=f.spirit+eD,mD=f.melee,dsum=gD+sD+mD||1;
 if(d>=.30){if(mD/dsum>=.30&&f.melee>=.15)classes.push('melee damage');
  if(gD/dsum>=.55)classes.push('gun damage');else if(sD/dsum>=.55)classes.push('spirit damage');else if(!classes.some(x=>/damage$/.test(x)))classes.push('gun-spirit hybrid damage');
  why.push(`damage share ${pc(d)}: gun ${pc(gD)}, spirit ${pc(f.spirit)} (+ability amplifiers on damage abilities ${pc(eD)}), melee ${pc(mD)}`)}
 if(!classes.length)classes.push('unclear');
 return {classes,why,comp:c,kit:k,share:{damage:d,utility:u,survival:s,enablerU:eU,enablerD:eD},level:hasSandbox?'composition+sandbox':'composition-only'}}
const pc=x=>Math.round(x*100)+'%';
// ---- claims in name / description / tags -------------------------------------------------------------
const LEX=[
 ['support',/\b(support|wingman|protect|guardian|bodyguard|concierge|babysit\w*)\b/i],['healer',/\b(healer|medic|nurse|healing|heals?)\b/i],
 ['tank',/\b(tank\w*|unkillable|iron|human shield|fortress|bulwark)\b/i],['gun',/\b(gun|guns|bullet|bullets|hose|shooter|glock|rifle|shoot\w*)\b/i],
 ['spirit',/\b(spirit|mage|caster|sorcer\w*)\b/i],['melee',/\b(melee|brawl\w*|punch\w*|fist\w*|stab\w*|slap\w*|knife|rabbit punch|curb stomp)\b/i],
 ['damage',/\b(dps|damage|carry)\b/i],['assassin',/\b(assassin|sniper|dive|diver|burst|pick|night night|ambush)\b/i],['bomb/ult',/\b(bomb|bomber|ult|nuke|grenade)\b/i]];
// STRONG = explicit role word; SOFT = flavour words that humorous names use ("Stabby", "Gun To Knife Fight"): soft hits are never allowed to FAIL a name
const SOFT=/\b(knife|stab\w*|brawl\w*|punch\w*|fist\w*|slap\w*|curb stomp|rabbit punch|hose|glock|shoot\w*|rifle|iron|dive|diver|pick|burst|ambush|bomb|bomber|grenade|nuke|night night)\b/ig;
function claims(text,strongOnly){let t=text;if(strongOnly)t=t.replace(SOFT,' ');const o=[];for(const [k,re] of LEX)if(re.test(t))o.push(k);return o}
function judge(claim,r){const f=r.comp.frac,sh=r.share,cl=r.classes;const D=f.gun+f.spirit+f.melee;
 const R_=(v,why)=>({claim,verdict:v,why});
 switch(claim){
 case 'support':if(cl.includes('support'))return R_('supported','utility-dominant composition');if(cl.includes('damage-support hybrid'))return R_('partial','composition is a damage/utility hybrid, not a pure support: label "support" overstates it');
   return sh.utility<.15&&sh.damage>.5?R_('contradicted',`only ${pc(sh.utility)} of core spend is utility for others vs ${pc(sh.damage)} damage`):R_('weak',`utility share ${pc(sh.utility)}`);
 case 'healer':{const h=f.ally+f.sustain;return h>=.2?R_('supported','heal/sustain share '+pc(h)):h<.1?R_('contradicted','heal/sustain share only '+pc(h)):R_('weak','heal/sustain share '+pc(h))}
 case 'tank':return sh.survival>=.35?R_('supported','survival share '+pc(sh.survival)):sh.survival<.2?R_('contradicted','survival share only '+pc(sh.survival)):R_('weak','survival share '+pc(sh.survival));
 case 'gun':return f.gun/(D||1)>=.5&&f.gun>=.2?R_('supported','gun is '+pc(f.gun)+' of core spend'):(f.gun<.1?R_('contradicted','gun items only '+pc(f.gun)+' of core spend'):R_('weak','gun '+pc(f.gun)));
 case 'spirit':{const sp=f.spirit+sh.enablerD;return sp>=.25?R_('supported','spirit/ability-amp '+pc(sp)):sp<.1?R_('contradicted','spirit/ability items only '+pc(sp)):R_('weak','spirit '+pc(sp))}
 case 'melee':return f.melee>=.15?R_('supported','melee items '+pc(f.melee)):f.melee<.05?R_('contradicted','melee items only '+pc(f.melee)):R_('weak','melee '+pc(f.melee));
 case 'damage':return sh.damage>=.5?R_('supported','damage share '+pc(sh.damage)):sh.damage<.3?R_('contradicted','damage share only '+pc(sh.damage)):R_('weak','damage '+pc(sh.damage));
 default:return R_('unverifiable','behavioural claim (positioning/burst/combo): composition cannot confirm it; needs sandbox behaviour evidence')}}
// tag -> evidence requirement
function judgeTag(tag,r,b){const f=r.comp.frac,w=r.comp.who,sh=r.share;const R_=(v,why)=>({tag,verdict:v,why});
 const need=(x,hi,lo,label)=>x>=hi?R_('supported',label+' '+pc(x)):x<lo?R_('contradicted',label+' only '+pc(x)):R_('weak',label+' '+pc(x));
 switch(tag){case 'weapon':return need(f.gun,.25,.10,'gun share of core spend');case 'spirit':return need(f.spirit+sh.enablerD,.25,.10,'spirit/ability share');
  case 'melee':return need(f.melee,.12,.04,'melee share');case 'damage':return need(sh.damage,.4,.25,'damage share');case 'vitality':return need(sh.survival,.25,.12,'survival share');
  case 'healing':return need(f.ally+f.sustain,.2,.1,'heal/sustain share');case 'mobility':{const j=need(f.mobility,.12,.04,'mobility share from items (ability mobility is not visible to this check)');return j.verdict==='contradicted'?R_('weak',j.why):j}
  case 'utility':return need(sh.utility,.2,.08,'utility-for-others share');
  case 'debuff':return w.debuff.length>=2?R_('supported','debuff items: '+w.debuff.join(', ')):w.debuff.length===1?R_('weak','only one debuff item: '+w.debuff[0]):R_('contradicted','no debuff item in core');
  case 'crowd_control':return w.cc.length>=2?R_('supported','cc items: '+w.cc.join(', ')):w.cc.length===1?R_('weak','only one cc item: '+w.cc[0]):R_('contradicted','no cc item in core');
  default:return R_('unverifiable','complexity tags are a judgement call, not derivable from composition')}}
module.exports={composition,kit,classify,claims,judge,judgeTag,pc};
