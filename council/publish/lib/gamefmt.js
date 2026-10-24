// What the game's build format supports, with sources, plus an INDEPENDENT decoder (not the site encoder) and the expected-vs-decoded comparison.
const C=require('./common');const zlib=require('zlib');
const {parse}=require(C.SP+'/cats.js');
const PROTO='gt/repo/Protobufs/citadel_gcmessages_common.proto:859-908 (CMsgHeroBuild, maximum_size_bytes=16000)';
const UI='gt/repo/game/citadel/pak01_dir/panorama/layout/citadel_hud_hero_builds.xml';
const LIMITS={ // UI limits come from the game's own panorama layout; GC limits are enforced server side (k_eNameTooLong/k_eDescriptionTooLong/k_eBuildTooLarge) with values NOT in the files
 name:{max:50,src:UI+':25 BuildNameTextEntry maxchars=50'},
 description:{max:512,src:UI+':27 BuildDescriptionTextEntry maxchars=512 multiline'},
 annotation:{max:200,src:UI+':46 AnnotationTextEntry maxchars=200'},
 sellPriority:{max:99,src:UI+':48 SellPriorityTextEntry maxchars=2'},
 categoryName:{max:null,src:UI+':37 CategoryNameTextEntry has NO maxchars (server limit unknown)'},
 categoryDescription:{max:null,src:UI+':40 CategoryDescriptionTextEntry has NO maxchars (server limit unknown)'},
 totalBytes:{max:16000,src:PROTO+' option maximum_size_bytes=16000; CCitadelClientMsg_HeroBuild max 16384; UI string #Citadel_HeroBuilds_Error_BuildTooLarge'},
 tagSlots:{max:3,src:UI+':31-33 BuildTag1..BuildTag3'}};
// category (non-item) tags the client knows: localisation keys in client_strings.txt lines 36087-36099
const TAG_KEYS=['complexity_1','complexity_2','complexity_3','crowd_control','damage','debuff','healing','melee','mobility','spirit','utility','vitality','weapon'];
const TAG_ID={};TAG_KEYS.forEach(k=>TAG_ID[k]=C.mm2('citadel_build_tag_'+k));
const TAG_BY_ID={};for(const k in TAG_ID)TAG_BY_ID[TAG_ID[k]]=k;
// Support matrix: field -> {game: supported by proto, site: carried by our exporter, paste: whether it survives the in-game clipboard paste, src}
const FIELDS=[
 ['build.hero_build_id',1,'yes','yes','paste:unknown','CMsgHeroBuild.hero_build_id; exporter uses meta.bid (910000+hero idx+100*variant idx) so a re-paste targets the same row'],
 ['build.hero_id',2,'yes','yes','assumed','exporter writes hero.id'],
 ['build.author_account_id',3,'yes (tied to the publishing Steam account)','constant 300559836','game shows the saving account','CMsgHeroBuild.author_account_id; there is NO free-text author/creator/profile-link field'],
 ['build.name',5,'yes','yes (+" (Fully Annotated)" suffix for importer-owned rows)','paste:carried (IMPORT.md verifies name after paste)','UI maxchars=50'],
 ['build.description',6,'yes','yes','paste:NOT carried per IMPORT.md ("paste doesn\'t carry it"): typed/pasted by hand separately','UI maxchars=512; to be re-verified by Kieran\'s optional manual test'],
 ['build.language',7,'yes','0','-','unused'],['build.version',8,'yes','1','server-managed (k_eStaleVersion)','NOT used as our revision number (server owns it)'],
 ['build.origin_build_id',9,'yes','not written','-','copy-lineage field'],
 ['build.tags[3]',11,'yes: 3 slots, ids = hash("citadel_build_tag_<key>") or an item/ability id (mod tag)','yes (record.tg)','paste:not independently verified','hash function confirmed against known ids; slot-3 item/ability convention is from existing exporter, display of an item tag after paste is UNVERIFIED'],
 ['build.development_build / publish_timestamp',12,'yes','13=now','-','publish_timestamp written as now'],
 ['category.name',2,'yes','yes (box title)','carried','no UI limit found'],
 ['category.description',3,'yes','yes (box description)','carried','no UI limit found'],
 ['category.optional',6,'yes','yes','carried','-'],
 ['category.width/height',4,'yes','heuristic layout floats','carried','cosmetic'],
 ['mod.ability_id (item)',1,'yes','yes','carried','missing/unknown items are DROPPED silently by enc.js (round trip catches it)'],
 ['mod.annotation (caption)',2,'yes','yes (item note)','carried','UI maxchars=200'],
 ['mod.required_flex_slots',3,'yes','not written','-','no data in the record; unused'],
 ['mod.sell_priority',4,'yes (UI "Set sell priority", 2 digits)','NOT written by live enc.js; staged enc.js supports optional item[3]','unverified','sale instructions currently live only in captions text'],
 ['mod.imbue_target_ability_id',5,'yes','yes (item imbue)','carried','-'],
 ['ability_order.currency_changes',2,'yes','yes (first=unlock type2, then T1/T2/T3 deltas)','carried','max 4 per ability in exporter'],
 ['currency_change.annotation',4,'yes (per ability-point note)','NOT written','-','no per-point notes in the record'],
 ['(not in game format)','-','NO field for: stage/phase labels beyond category names, build revision, evidence/validation status, creator name/links, tradeoff lists','website only','-','kept on the website; never claimed to import']];
function cats(p){return p.filter(x=>x[0]===1).map(x=>parse(x[2]))}
const g=(a,n)=>a.filter(x=>x[0]===n).map(x=>x[2]);
function decode(code,ctx){ // ctx {ITEMS,HEROES}
 const raw=zlib.zstdDecompressSync(Buffer.from(code.trim(),'base64'));const top=parse(raw);
 const byId={};for(const n in ctx.ITEMS)byId[ctx.ITEMS[n].id]=n;
 const hero=ctx.HEROES.find(h=>h.id===Number(g(top,2)[0]));const abById={};if(hero)hero.ab.forEach((a,i)=>abById[a.id]=i+1);
 const str=b=>b===undefined?'':Buffer.from(b).toString('utf8');
 const out={bytes:raw.length,build_id:Number(g(top,1)[0]),hero_id:Number(g(top,2)[0]),hero:hero&&hero.name,author:Number(g(top,3)[0]),name:str(g(top,5)[0]),desc:str(g(top,6)[0]),version:Number(g(top,8)[0]),
  tags:g(top,11).map(Number).map(t=>TAG_BY_ID[t]||(byId[t]?{item:byId[t]}:(hero&&hero.ab.find(a=>a.id===t)?{ability:hero.ab.find(a=>a.id===t).n}:{unknown:t}))),
  categories:[],order:[]};
 const det=parse(g(top,10)[0]);
 for(const c of g(det,1)){const p=parse(c);out.categories.push({name:str(g(p,2)[0]),desc:str(g(p,3)[0]),optional:!!Number(g(p,6)[0]||0),w:g(p,4)[0],h:g(p,5)[0],
  mods:g(p,1).map(m=>{const q=parse(m);const id=Number(g(q,1)[0]);const im=g(q,5)[0];return {item:byId[id]||('#'+id),note:str(g(q,2)[0]),imbue:im?(abById[Number(im)]||-1):0,sell:Number(g(q,4)[0]||0),flex:Number(g(q,3)[0]||0)}})})}
 const ao=g(det,2)[0];if(ao){for(const c of g(parse(ao),1)){const p=parse(c);const s=x=>{x=BigInt(x);return Number(BigInt.asIntN(32,x))};out.order.push({ab:abById[Number(g(p,1)[0])],type:Number(g(p,2)[0]),delta:s(g(p,3)[0]!==undefined?g(p,3)[0]:0)})}}
 return out}
// the order entries the game format should contain for an ability-point string (independent of enc.js)
function expectedOrder(order){const cnt={},ent=[];for(const i of order){if(!i)continue;const c=cnt[i]=(cnt[i]||0);cnt[i]++;if(c>3)continue;ent.push({ab:i,type:c===0?2:1,delta:c===0?-1:[-1,-2,-5][c-1]})}return ent}
module.exports={LIMITS,TAG_KEYS,TAG_ID,TAG_BY_ID,FIELDS,decode,expectedOrder,PROTO,UI};
