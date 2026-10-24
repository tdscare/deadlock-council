// name / description / tag / caption consistency lint for ONE build record content. Never edits anything.
const C=require('./common');const I=require('./identity');const G=require('./gamefmt');const X=require('./export');const {fs,path,SP,PUB}=C;
const MARKETING=/\b(amazing|insane|incredible|unstoppable|ultimate|godlike|god[- ]tier|broken|overpowered|op|top[- ]tier|best|crazy|massive damage|great survivability|high damage|huge damage|dominat\w+|destroy\w*|annihilat\w+|devastating|unleash\w*|beast mode|perfect for|powerhouse|game[- ]changer|supreme)\b/i;
const PROMO=/(come watch|twitch\.tv|youtube\.com|subscribe|follow me|my channel|watch me)/i;
const AI_NAME=/\b(ultimate|supreme|extreme|unleashed|master(?:y)?|pro|elite|apex|prime|reborn|redefined|rise of|the (?:rise|fall|return) of|of doom|of destiny)\b/i;
const TRADE=/\b(but|however|trade[- ]?off|at the cost|costs?|depends?|needs?|requires?|relies|reliant|weak|struggles?|less|sacrific\w+|without|only works|unless|falls? off|vulnerable|worse|slower|lacks?|gives up|give up)\b/i;
const APPROACH=/\b(fight|fights|engage|poke|dive|skirmish|lane|team|teamfight|pick|picks|roam\w*|farm\w*|front|frontline|back ?line|ult|combo|trade|trades|burst|sustain|brawl\w*|snipe|peel|kite|flank|zone|setup|set up|follow[- ]?up)\b/i;
const SENT=t=>t.split(/(?<=[.!?])\s+/).map(s=>s.trim()).filter(Boolean);
function lintDesc(c,ctx,out){const d=(c.desc||'').trim();const issue=(sev,code,msg)=>out.push({area:'description',sev,code,msg});
 if(!d)return issue('gap','EMPTY','no description');
 const words=d.split(/\s+/).length;
 if(words<=6)issue('gap','LABEL_ONLY',`"${d}" is a style label (${words} words), not a decision-useful description (does not state damage source, approach, trade-off, dependency)`);
 if(MARKETING.test(d))issue('fail','MARKETING','marketing/vague phrase: '+d.match(MARKETING)[0]);
 if(PROMO.test(d))issue('fail','PROMO','channel promo in the description field (branding is added by the exporter from branding.json, never typed into the record)');
 const names=Object.keys(ctx.ITEMS).filter(n=>new RegExp('\\b'+n.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b').test(d));
 if(names.length>=4)issue('fail','ITEM_LIST',`lists ${names.length} items (${names.slice(0,5).join(', ')}): a description is not an item list`);
 const budget=G.LIMITS.description.max-(X.BR.game_line.length+1)-('Rev r00#00000000'.length+1);
 if(d.length>budget)issue('fail','TOO_LONG',`${d.length} chars > ${budget} available in-game after the creator line and revision line (512 limit)`);
 if(words>6){ if(!TRADE.test(d))issue('fail','NO_TRADEOFF','no trade-off / dependency / limitation stated');if(!APPROACH.test(d))issue('warn','NO_APPROACH','no fight/match approach stated (heuristic word check)');
  const basis=c.basis||[];const uncovered=SENT(d).filter(s=>!basis.some(b=>s.startsWith(b.s)||b.s.startsWith(s)));
  if(!basis.length)issue('fail','UNSOURCED','description has no `basis` list: every sentence must cite what the Council established (composition metric, evidence file, kit fact)');
  else if(uncovered.length)issue('fail','UNSOURCED_SENTENCE',`${uncovered.length} sentence(s) without a basis entry: "${uncovered[0].slice(0,60)}"`);
  for(const b of basis){if(!b.ref)issue('fail','BASIS_NO_REF','basis entry without ref');else if(/^(file:|council\/|evidence\/)/.test(b.ref)){const f=b.ref.replace(/^file:/,'');if(!fs.existsSync(path.join(SP,f)))issue('fail','BASIS_MISSING_FILE','basis file does not exist: '+f)}}}
}
function lintName(c,ctx,res,out){const base=c.name.replace(/^Rizuhble's\s+/,'');const issue=(sev,code,msg)=>out.push({area:'name',sev,code,msg});
 if(c.name.length>32)issue('fail','NAME_LEN',c.name.length+' chars > 32 (builds_check NAME_LEN; +suffix must stay <= 50)');
 if(AI_NAME.test(base))issue('fail','GENERIC_NAME','generic/dramatic naming pattern: '+base.match(AI_NAME)[0]);
 const hero=c.hero.toLowerCase();if(base.toLowerCase().replace(hero,'').replace(/[^a-z]/g,'').length<3)issue('fail','NAME_RESTATES_HERO','name is just the hero name');
 const {B}=ctx.data;const dup=B.filter(x=>x.id!==c.id&&x.name===c.name);if(dup.length)issue('fail','NAME_DUP','same name as '+dup.map(x=>x.id).join(', '));
 // name claims vs evidence (name only)
 const soft=new Set(I.claims(base).filter(k=>!I.claims(base,true).includes(k)));for(const k of I.claims(base)){const j=I.judge(k,res);if(soft.has(k)){if(j.verdict==='contradicted')issue('warn','NAME_FLAVOUR_VS_EVIDENCE',`name flavour suggests "${k}" but ${j.why} (humour is allowed; make sure it does not mislead)`);continue}if(j.verdict==='contradicted')issue('fail','NAME_CLAIM_CONTRADICTED',`name implies "${k}": ${j.why}`);else if(j.verdict==='partial')issue('warn','NAME_CLAIM_PARTIAL',`name implies "${k}": ${j.why}`);else if(j.verdict==='unverifiable')issue('info','NAME_CLAIM_UNVERIFIABLE',`name implies "${k}" (${j.why})`)}}
function lintClaims(c,ctx,res,out){const issue=(sev,code,msg)=>out.push({area:'class',sev,code,msg});const seen=new Set();
 for(const k of I.claims(c.desc||'')){const j=I.judge(k,res);if(j.verdict==='contradicted')issue('fail','DESC_CLAIM_CONTRADICTED',`description says "${k}": ${j.why}`);else if(j.verdict==='partial')issue('warn','DESC_CLAIM_PARTIAL',`description says "${k}": ${j.why}`);else if(j.verdict==='weak')issue('warn','DESC_CLAIM_WEAK',`description says "${k}": only weak support (${j.why})`);}}
function lintTags(c,ctx,res,out){const issue=(sev,code,msg)=>out.push({area:'tags',sev,code,msg});const t=X.tagsOf(c);
 if(!t.tg){issue('gap','NO_TAGS','no tags available');return}
 if(t.source==='hero-default')issue('gap','TAGS_HERO_DEFAULT','tags are the per-hero default from mkimport.js T, not chosen for this build ('+t.tg.join(', ')+')');
 for(const tag of t.tg){const isCat=G.TAG_ID[tag];if(!isCat){const inb=C.items(c).some(i=>i.name===tag&&i.core&&!i.opt);const hero=C.heroOf(ctx.HEROES,c);if(!ctx.ITEMS[tag]&&!hero.ab.find(a=>a.n===tag))issue('fail','TAG_UNSUPPORTED','not a game tag, item or ability: '+tag);else if(ctx.ITEMS[tag]&&!inb)issue('warn','TAG_ITEM_NOT_IN_CORE','mod tag '+tag+' is not a core item of this build');continue}
  const j=I.judgeTag(tag,res,c);if(j.verdict==='contradicted')issue('fail','TAG_CONTRADICTED',`tag ${tag}: ${j.why}`);else if(j.verdict==='weak')issue('warn','TAG_WEAK',`tag ${tag}: ${j.why}`)}
 if(new Set(t.tg).size!==t.tg.length)issue('fail','TAG_DUP','duplicate tag');
 // hybrid builds must not be forced into one tag
 if(res.classes.includes('damage-support hybrid')&&!t.tg.some(x=>['utility','debuff','crowd_control','healing'].includes(x)))issue('warn','HYBRID_SINGLE_TAG','evidence says damage/support hybrid but no utility-type tag is set');
 if(res.classes.includes('support')&&!t.tg.some(x=>['utility','debuff','crowd_control','healing'].includes(x)))issue('fail','SUPPORT_NO_UTILITY_TAG','evidence says support but no utility/debuff/crowd_control/healing tag');}
function lintCaptions(c,ctx,out){const issue=(sev,code,msg)=>out.push({area:'captions',sev,code,msg});const its=C.items(c);
 const empty=its.filter(i=>i.core&&!i.opt&&!i.note);if(empty.length)issue('gap','CAPTION_MISSING',`${empty.length}/${its.filter(i=>i.core&&!i.opt).length} core items have no caption (rule: every finished item needs a build-specific caption)`);
 const generic=its.filter(i=>/^(Upgrade of|Sell .* for this\.?$|If you bought)/.test(i.note));if(generic.length)issue('gap','CAPTION_BOILERPLATE',generic.length+' captions are sale/upgrade boilerplate only');
 const boxes=c.rows.flat().filter(b=>C.isCore(b[0]));const nod=boxes.filter(b=>!b[1]);if(nod.length)issue('gap','PHASE_DESC_MISSING',nod.map(b=>b[0]).join(', ')+' have no phase description')}
function lintBuild(c,ctx,hasSandbox){const res=I.classify(c,ctx,hasSandbox);const out=[];lintName(c,ctx,res,out);lintDesc(c,ctx,out);lintClaims(c,ctx,res,out);lintTags(c,ctx,res,out);lintCaptions(c,ctx,out);
 if(res.comp.unknown.length)out.push({area:'class',sev:'warn',code:'ITEM_ROLE_UNKNOWN',msg:'no role row for '+res.comp.unknown.join(', ')});
 const worst=out.some(o=>o.sev==='fail')?'MISMATCH':out.some(o=>o.sev==='warn')?'UNCERTAIN':'OK';return {res,issues:out,verdict:worst,level:res.level}}
module.exports={lintBuild,lintDesc,lintName,MARKETING,AI_NAME};
