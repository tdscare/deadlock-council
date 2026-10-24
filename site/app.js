/* Rizuhble build browser + editor */
const COST={1:800,2:1600,3:3200,4:6400},ROM={1:"I",2:"II",3:"III",4:"IV"},CATN={w:"Weapon",s:"Spirit",v:"Vitality"};
const ICON_LC={};for(const k in ICONS)ICON_LC[k.toLowerCase()]=ICONS[k];
const DESC_LC={};try{for(const k in DESC)DESC_LC[k.toLowerCase()]=DESC[k]}catch(e){}
const PRESET_HERO={danny:"hero_deadpack",bebop:"hero_bebop",dynamo:"hero_dynamo",greytalon:"hero_orion",infernus:"hero_inferno",kelvin:"hero_kelvin",paige:"hero_bookworm",ratking:"hero_ratking",haze:"hero_haze",rem:"hero_familiar",seven:"hero_gigawatt",solomon:"hero_chessmaster",venator:"hero_priest",victor:"hero_frank",violet:"hero_artist",viscous:"hero_viscous",wraith:"hero_wraith",yamato:"hero_yamato",mina:"hero_vampirebat"};
const HERO_BY_KEY={};HEROES.forEach(h=>HERO_BY_KEY[h.key]=h);
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const clone=o=>JSON.parse(JSON.stringify(o));
const store={get(k,d){try{const v=localStorage.getItem(k);return v?JSON.parse(v):d}catch(e){return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};

/* ---------- data ---------- */
function imbIndex(v,b,hero){
  if(v==null||v===""||v===0)return 0;if(typeof v==="number")return v;
  if(/^[1-4]$/.test(v))return +v;if(/^ult$/i.test(v))return 4;
  const t=v.toLowerCase(),names=(hero?hero.ab.map(a=>a.n):[]).concat(b.abil||[]);
  for(let i=0;i<names.length;i++)if(names[i].toLowerCase().includes(t))return i%4+1;return 0}
function normPreset(b){
  const n=clone(b);n.hk=b.hk||PRESET_HERO[b.id];n.preset=true;const hero=HERO_BY_KEY[n.hk];
  n.rows=n.rows.map(r=>r.map(([t,d,o,items])=>[t,d||"",!!o,items.map(([nm,note,imb])=>[nm,note||"",imbIndex(imb,b,hero)])]));
  n.order=b.order?b.order.slice():[];delete n.abil;delete n.changes;return n}
const PRESETS=B.map(normPreset);
let MINE=store.get("rz-mybuilds",[]);
const saveMine=()=>store.set("rz-mybuilds",MINE);
const findBuild=id=>PRESETS.find(b=>b.id===id)||MINE.find(b=>b.id===id);
const DUO_OF={};(typeof DUOS!=="undefined"?DUOS:[]).forEach(d=>{DUO_OF[d.a]={with:d.b,combo:d.combo,status:d.status};DUO_OF[d.b]={with:d.a,combo:d.combo,status:d.status}});

/* ---------- state ---------- */
let cur=null,editing=false,owned=[],spent=0,simMsg="";
const tabs=document.getElementById("tabs"),win=document.getElementById("win"),dock=document.getElementById("dock");
const tip=document.createElement("div");tip.className="tip";tip.hidden=true;document.body.appendChild(tip);
let pinned=false;document.addEventListener("click",()=>{pinned=false;tip.hidden=true});

/* ---------- sidebar ---------- */
function renderTabs(){
  tabs.innerHTML="";
  const grp=(label,list,cls)=>{if(!list.length)return;const h=document.createElement("div");h.className="grp";h.textContent=label;tabs.appendChild(h);
    list.slice().sort((a,b)=>heroName(a).localeCompare(heroName(b))).forEach(b=>{const t=document.createElement("button");t.className="tab";t.setAttribute("role","tab");t.id="tab-"+b.id;
      const multi=!cls&&list.filter(x=>heroName(x)===heroName(b)).length>1;t.innerHTML=`<span>${esc(cls?b.name:heroName(b))}</span>${cls?`<small>${esc(heroName(b))}</small>`:multi?`<small>${esc((b.desc&&b.desc.length<=22?b.desc:b.name.replace(/^Rizuhble's /,'')).replace(/\.$/,''))}</small>`:""}`;t.setAttribute("aria-selected",cur&&cur.id===b.id);t.onclick=()=>show(b.id);tabs.appendChild(t)})};
  grp("Rizuhble's builds",PRESETS.filter(b=>!DUO_OF[b.id]),false);
  const dl=PRESETS.filter(b=>DUO_OF[b.id]);
  if(dl.length){const h=document.createElement("div");h.className="grp";h.textContent="Duo builds";tabs.appendChild(h);
    dl.forEach(b=>{const w=findBuild(DUO_OF[b.id].with),t=document.createElement("button");t.className="tab";t.setAttribute("role","tab");t.id="tab-"+b.id;
      t.innerHTML=`<span>${esc(heroName(b))}</span><small>with ${esc(w?heroName(w):"")}</small>`;t.setAttribute("aria-selected",cur&&cur.id===b.id);t.onclick=()=>show(b.id);tabs.appendChild(t)})}
  grp("My builds",MINE,true);
  const nb=document.createElement("button");nb.className="tab newb";nb.textContent="+ New build";nb.onclick=newBuildDialog;tabs.appendChild(nb);
}
const heroName=b=>(HERO_BY_KEY[b.hk]||{}).name||b.hero||"";

/* ---------- items ---------- */
function initials(n){const w=n.replace(/[^A-Za-z' -]/g,"").split(/[ -]+/).filter(Boolean);return (w.length>1?w[0][0]+w[1][0]:w[0].slice(0,2)).toUpperCase()}
const itemInfo=n=>ITEMS[n]||{t:1,c:"s",u:[],i:0};
function itemTile(n,opts={}){
  const d=itemInfo(n),b=document.createElement("button");b.type="button";b.className=`it ${d.c} t${d.t}`+(opts.note?" hasnote":"");
  const src=ICON_LC[n.toLowerCase()];b.style.backgroundImage=`url(${ICON_LC["card_backer_"+{w:"weapon",s:"spirit",v:"vitality"}[d.c]+"_t"+d.t]})`;
  const small=!n.includes(" ")&&n.length>9||n.length>18;
  b.innerHTML=(src?`<span class="ic"><img src="${src}" alt=""></span>`:`<span class="ic"><span class="gl">${initials(n)}</span></span>`)+`<span class="tr"></span><span class="tn">${ROM[d.t]}</span>`+(opts.imb?`<span class="imb"><span>IMBUE</span></span>`:"")+`<span class="nm${small?" sm":""}">${esc(n)}</span>`;
  b.dataset.name=n;b.onmouseenter=()=>tipShow(b,n,opts.note,opts.imb);b.onmouseleave=()=>{if(!pinned)tip.hidden=true};
  return b}
function tipShow(el,n,note,imb){
  const d=itemInfo(n),ds=DESC_LC[n.toLowerCase()]||"",hero=HERO_BY_KEY[cur&&cur.hk];
  const imbName=imb&&hero?hero.ab[imb-1].n:"";
  tip.className="tip "+d.c;
  tip.innerHTML=`<div class="th"><b>${esc(n)}</b><span>${COST[d.t].toLocaleString("en-GB")}</span></div>${ds?`<div class="ts">${ds.split(", ").map(x=>`<span>${esc(x)}</span>`).join("")}</div>`:""}${imbName?`<div class="tm">Imbue: ${esc(imbName)}</div>`:""}${note?`<div class="tn2">${esc(note)}</div>`:""}`;
  tip.hidden=false;const r=el.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight;
  let x=r.right+8,y=r.top;if(x+tw>innerWidth-8)x=r.left-tw-8;if(x<8)x=8;if(y+th>innerHeight-8)y=innerHeight-th-8;if(y<8)y=8;
  tip.style.left=x+"px";tip.style.top=y+"px"}

/* ---------- buy simulator ---------- */
function chainOf(n){const c=[];(itemInfo(n).u||[]).forEach(x=>c.push(x,...chainOf(x)));return c}
const isOwned=n=>owned.includes(n)||owned.some(o=>chainOf(o).includes(n));
function toggleBuy(n){
  if(!owned.includes(n)&&isOwned(n))return;
  const i=owned.indexOf(n);if(i>=0){owned.splice(i,1);spent-=COST[itemInfo(n).t];renderSim(true);return}
  let c=COST[itemInfo(n).t];const have=(itemInfo(n).u||[]).filter(x=>owned.includes(x));
  if(!have.length&&owned.length>=12){simMsg="All 12 slots are full. Sell something first.";renderSim(true);return}
  if(have.length){owned[owned.indexOf(have[0])]=n;have.slice(1).forEach(x=>owned.splice(owned.indexOf(x),1));have.forEach(x=>c-=COST[itemInfo(x).t])}else owned.push(n);
  spent+=c;renderSim(true)}
function renderSim(pop){
  const inv={w:0,s:0,v:0};owned.forEach(n=>inv[itemInfo(n).c]+=COST[itemInfo(n).t]);
  const bars=["w","s","v"].map(k=>{const pct=Math.min(100,inv[k]/9600*100),hit=inv[k]>=4800;
    return `<div class="ib"><span class="il">${CATN[k]}</span><div class="track ${k}"><div class="fill" style="width:${pct}%"></div><div class="tick"></div></div><span class="iv${hit?" hit":""}">${(inv[k]/1000).toFixed(1)}k${hit?" ✓":""}</span></div>`}).join("");
  const slots=Array.from({length:12},(_,i)=>{const n=owned[i];if(!n)return`<span class="slot"></span>`;const src=ICON_LC[n.toLowerCase()];
    return `<button type="button" class="slot full" data-sell="${esc(n)}" title="Sell ${esc(n)}">${src?`<img src="${src}" alt="${esc(n)}">`:initials(n)}</button>`}).join("");
  dock.innerHTML=`<div class="dk"><div class="spent"><b>${spent.toLocaleString("en-GB")}</b><span>souls spent</span></div><div class="bars">${bars}</div><div class="slots">${slots}</div><button type="button" class="reset">Reset</button></div>${simMsg?`<p class="warn">${simMsg}</p>`:""}`;
  simMsg="";
  dock.querySelector(".reset").onclick=()=>{owned=[];spent=0;renderSim(true)};
  dock.querySelectorAll("[data-sell]").forEach(s=>s.onclick=()=>toggleBuy(s.dataset.sell));
  document.querySelectorAll(".canvas .it").forEach(e=>e.classList.toggle("owned",isOwned(e.dataset.name)));
  if(pop){dock.classList.remove("pop");void dock.offsetWidth;dock.classList.add("pop")}}

/* ---------- main view ---------- */
function save(){if(!cur||cur.preset)return;const i=MINE.findIndex(b=>b.id===cur.id);if(i>=0)MINE[i]=cur;else MINE.push(cur);saveMine()}
function show(id,keepEdit){
  const b=findBuild(id);if(!b)return;cur=b;if(!keepEdit)editing=false;
  store.set("rz-build",id);owned=[];spent=0;render();renderTabs();renderSim()}
function render(){
  const b=cur,hero=HERO_BY_KEY[b.hk];
  win.innerHTML="";win.classList.toggle("editing",editing);
  const bar=document.createElement("div");bar.className="bar";
  bar.innerHTML=`<h2 ${editing?'contenteditable="true" spellcheck="false"':""} class="bname">${esc(b.name)}</h2>`+
    (editing?`${b.preset?"":`<button type="button" class="pill del" id="delbtn">Delete build</button>`}<button type="button" class="pill" id="donebtn">Done</button>`:`<button type="button" class="pill" id="editbtn">Edit</button>`)+
    `<button type="button" class="pill copy" id="copybtn">Copy for game</button><button type="button" class="pill copy" id="descbtn">Copy description</button>`;
  win.appendChild(bar);
  const ds=document.createElement("div");ds.className="desc";ds.innerHTML=`<span class="hero">${esc(hero?hero.name:"")}</span><span ${editing?'contenteditable="true" spellcheck="false"':""} class="bdesc">${esc(b.desc)}</span>`;win.appendChild(ds);
  const du=DUO_OF[b.id];
  if(du&&b.preset){const w=findBuild(du.with),dv=document.createElement("div");dv.className="duo";
    dv.innerHTML=`<span class="dh">Duo with ${esc(w?heroName(w):"")}</span><span class="dc">${esc(du.combo)}</span><span class="dst">${esc(du.status||"Untested")}</span><button type="button" class="pill" id="duobtn">${esc(w?heroName(w):"Partner")} build</button>`;
    win.appendChild(dv);dv.querySelector("#duobtn").onclick=()=>show(du.with)}
  if(editing){bar.querySelector(".bname").oninput=e=>{b.name=e.target.textContent.trim();save();renderTabs()};ds.querySelector(".bdesc").oninput=e=>{b.desc=e.target.textContent.trim();save()};
    bar.querySelector("#donebtn").onclick=()=>{editing=false;render();renderSim()};
    const del=bar.querySelector("#delbtn");if(del)armDelete(del,"Delete build","Sure? Delete",()=>{MINE=MINE.filter(x=>x.id!==b.id);saveMine();show(PRESETS[0].id)});}
  else bar.querySelector("#editbtn").onclick=startEdit;
  const tb=document.createElement("textarea");tb.id="codebox";tb.readOnly=true;tb.hidden=true;win.appendChild(tb);
  bar.querySelector("#copybtn").onclick=async e=>{const btn=e.currentTarget;const code=buildCode(exportBuild(b),hero,ITEMS);let ok=false;
    try{await navigator.clipboard.writeText(code);ok=true}catch(err){}
    if(!ok){tb.hidden=false;tb.value=code;tb.focus();tb.select();try{ok=document.execCommand("copy")}catch(err){}}
    btn.textContent=ok?"Copied":"Copy the code below";setTimeout(()=>btn.textContent="Copy for game",2000)};
  bar.querySelector("#descbtn").onclick=async e=>{const btn=e.currentTarget;const t="Come watch me live: twitch.tv/rizuhble | youtube.com/@rizuhble";let ok=false;
    try{await navigator.clipboard.writeText(t);ok=true}catch(err){}
    if(!ok){tb.hidden=false;tb.value=t;tb.focus();tb.select();try{ok=document.execCommand("copy")}catch(err){}}
    btn.textContent=ok?"Copied":"Copy the text below";setTimeout(()=>btn.textContent="Copy description",2000)};
  const cv=document.createElement("div");cv.className="canvas";
  b.rows.forEach((r,ri)=>{const row=document.createElement("div");row.className="row";r.forEach((box,bi)=>row.appendChild(boxEl(box,ri,bi)));cv.appendChild(row)});
  if(editing){const add=document.createElement("button");add.type="button";add.className="addbox";add.textContent="+ Add box";add.onclick=()=>{b.rows.push([["New box","",true,[]]]);save();render()};cv.appendChild(add)}
  win.appendChild(cv);
  const low=document.createElement("div");low.className="lower";
  const left=document.createElement("div");left.className="card";left.innerHTML=`<h3>Item note</h3><div class="note"><p>Click an item to see its note.</p></div>`;
  const right=document.createElement("div");right.className="card";right.appendChild(orderEl(b,hero));
  low.append(left,right);win.appendChild(low);
}
function startEdit(){
  if(cur.preset){const c=clone(cur);c.id="u"+Date.now().toString(36);delete c.preset;MINE.push(c);saveMine();cur=c}
  editing=true;show(cur.id,true)}
function armDelete(btn,label,confirmLabel,fn){let armed=false,t;btn.textContent=label;
  btn.onclick=e=>{e.stopPropagation();if(armed){clearTimeout(t);fn();return}armed=true;btn.textContent=confirmLabel;t=setTimeout(()=>{armed=false;btn.textContent=label},2500)}}
function exportBuild(b){const m=(typeof META!=="undefined"&&META[b.id])||{};return {bid:m.bid,tags:m.tags,name:b.name+(b.name&&!/\(Fully Annotated\)$/.test(b.name)&&m.bid?" (Fully Annotated)":""),desc:m.bid?"Come watch me live: twitch.tv/rizuhble | youtube.com/@rizuhble":(b.desc||b.hero||"Build"),order:b.order,rows:b.rows.map(r=>r.map(([t,d,o,items])=>[t,d,o,items.map(([n,note,imb])=>[n,note||"",imb||0])]))}}

/* ---------- boxes ---------- */
function boxEl(box,ri,bi){
  const [title,desc,opt,items]=box,b=cur;
  const c=document.createElement("section");c.className="cat"+(opt?" optional":"");
  if(!editing){c.innerHTML=`<div class="hd"><b>${esc(title)}</b>${opt?'<span class="o">OPTIONAL</span>':""}${desc?`<i>${esc(desc)}</i>`:""}</div>`}
  else{
    c.innerHTML=`<div class="hd"><b contenteditable="true" spellcheck="false" class="ed-t">${esc(title)}</b><i contenteditable="true" spellcheck="false" class="ed-d" data-ph="Description">${esc(desc)}</i>
      <div class="boxctl"><label><input type="checkbox" ${opt?"checked":""}> Optional</label><span class="mv"><button type="button" data-m="l" title="Move left">◀</button><button type="button" data-m="r" title="Move right">▶</button><button type="button" data-m="u" title="Move up a row">▲</button><button type="button" data-m="d" title="Move down a row">▼</button></span><button type="button" class="xbox">Delete box</button></div></div>`;
    c.querySelector(".ed-t").oninput=e=>{box[0]=e.target.textContent.trim();save()};
    c.querySelector(".ed-d").oninput=e=>{box[1]=e.target.textContent.trim();save()};
    c.querySelector("input").onchange=e=>{box[2]=e.target.checked;save();render()};
    c.querySelectorAll("[data-m]").forEach(btn=>btn.onclick=()=>moveBox(ri,bi,btn.dataset.m));
    armDelete(c.querySelector(".xbox"),"Delete box","Sure?",()=>{b.rows[ri].splice(bi,1);if(!b.rows[ri].length)b.rows.splice(ri,1);save();render()});
  }
  const its=document.createElement("div");its.className="items";its.dataset.ri=ri;its.dataset.bi=bi;
  items.forEach((it,ii)=>{const [n,note,imb]=it;const el=itemTile(n,{note,imb});
    if(editing){el.draggable=true;el.ondragstart=e=>{e.dataTransfer.setData("text/plain",JSON.stringify([ri,bi,ii]));e.dataTransfer.effectAllowed="move";el.classList.add("dragging")};el.ondragend=()=>el.classList.remove("dragging");
      el.onclick=e=>{e.stopPropagation();tip.hidden=true;itemDialog(box,ii)}}
    else el.onclick=e=>{e.stopPropagation();toggleBuy(n);noteShow(n,note,imb);pinned=true;tipShow(el,n,note,imb)};
    its.appendChild(el)});
  if(editing){const add=document.createElement("button");add.type="button";add.className="it addit";add.innerHTML="<span>+</span>";add.title="Add item";add.onclick=e=>{e.stopPropagation();shopDialog(box)};its.appendChild(add);
    its.ondragover=e=>{e.preventDefault();its.classList.add("over")};its.ondragleave=()=>its.classList.remove("over");
    its.ondrop=e=>{e.preventDefault();its.classList.remove("over");let src;try{src=JSON.parse(e.dataTransfer.getData("text/plain"))}catch(err){return}
      const tiles=[...its.querySelectorAll(".it:not(.addit)")];let at=tiles.length;
      for(let k=0;k<tiles.length;k++){const r=tiles[k].getBoundingClientRect();if(e.clientX<r.left+r.width/2){at=k;break}}
      const from=b.rows[src[0]][src[1]][3],it=from.splice(src[2],1)[0];
      if(from===items&&src[2]<at)at--;items.splice(at,0,it);save();render()}}
  c.appendChild(its);return c}
function moveBox(ri,bi,m){
  const rows=cur.rows,box=rows[ri][bi];
  if(m==="l"&&bi>0){[rows[ri][bi-1],rows[ri][bi]]=[box,rows[ri][bi-1]]}
  else if(m==="r"&&bi<rows[ri].length-1){[rows[ri][bi+1],rows[ri][bi]]=[box,rows[ri][bi+1]]}
  else if(m==="u"||m==="d"){rows[ri].splice(bi,1);let t=m==="u"?ri-1:ri+1;
    if(t<0){rows.unshift([box]);t=-1}else if(t>=rows.length){rows.push([box])}else rows[t].push(box);
    for(let k=rows.length-1;k>=0;k--)if(!rows[k].length)rows.splice(k,1)}
  save();render()}
function noteShow(n,note,imb){
  const box=win.querySelector(".lower .note");if(!box)return;const d=itemInfo(n),hero=HERO_BY_KEY[cur.hk];
  box.innerHTML=`<div class="ttl">${esc(n)}<span class="meta">${CATN[d.c]} · ${COST[d.t]} souls${imb&&hero?" · imbue: "+esc(hero.ab[imb-1].n):""}</span></div><p>${esc(note)||"No note."}</p>`}

/* ---------- ability order ---------- */
function orderEl(b,hero){
  const wrap=document.createElement("div");
  wrap.innerHTML=`<h3>Ability point order${editing?' <button type="button" class="reset clr">Clear</button>':""}</h3>`;
  const g=document.createElement("div");g.className="ao"+(editing?" edit":"");
  g.innerHTML=`<span></span>`+Array.from({length:16},(_,i)=>`<span class="hdr">${i+1}</span>`).join("");
  const order=b.order||[];
  hero.ab.forEach((a,ai)=>{
    g.insertAdjacentHTML("beforeend",`<span class="an" title="${esc(a.n)}">${ai+1} · ${esc(a.n)}</span>`);
    let lvl=0;
    for(let i=0;i<16;i++){const on=order[i]===ai+1;if(on)lvl++;
      const cls=on?(lvl===1?"un":lvl>4?"bad":"on"):"";
      const cell=document.createElement(editing?"button":"span");cell.className="c "+cls;cell.textContent=on?(lvl===1?"◆":lvl-1):"";
      if(editing){cell.type="button";cell.title=`Point ${i+1}: ${a.n}`;cell.onclick=()=>{b.order=b.order||[];while(b.order.length<16)b.order.push(null);b.order[i]=b.order[i]===ai+1?null:ai+1;save();rerenderOrder()}}
      g.appendChild(cell)}});
  wrap.appendChild(g);
  wrap.insertAdjacentHTML("beforeend",`<div class="legend"><span class="l1">Unlock</span><span class="l2">Upgrade tier</span></div>`);
  const clr=wrap.querySelector(".clr");if(clr)clr.onclick=()=>{b.order=[];save();rerenderOrder()};
  return wrap}
function rerenderOrder(){const card=win.querySelector(".lower .card:last-child");card.innerHTML="";card.appendChild(orderEl(cur,HERO_BY_KEY[cur.hk]))}

/* ---------- dialogs ---------- */
const dlg=document.getElementById("dlg");
function openDlg(html,cls){dlg.className=cls||"";dlg.innerHTML=`<button type="button" class="dx" aria-label="Close">✕</button>`+html;dlg.querySelector(".dx").onclick=()=>dlg.close();if(!dlg.open)dlg.showModal();return dlg}
dlg.addEventListener("click",e=>{if(e.target===dlg)dlg.close()});
function shopDialog(box){
  let tab=store.get("rz-shoptab","w");
  const draw=()=>{const list=Object.entries(ITEMS).filter(([n,d])=>d.c===tab);
    openDlg(`<h3>Add item</h3><div class="stabs">${["w","v","s"].map(k=>`<button type="button" class="st ${k}${k===tab?" on":""}" data-k="${k}">${CATN[k]}</button>`).join("")}</div>`+
      [1,2,3,4].map(t=>`<div class="tier"><div class="tl">${ROM[t]} · ${COST[t].toLocaleString("en-GB")}</div><div class="tg" data-t="${t}"></div></div>`).join(""),"shop");
    dlg.querySelectorAll(".st").forEach(s=>s.onclick=()=>{tab=s.dataset.k;store.set("rz-shoptab",tab);draw()});
    list.sort((a,b)=>a[0].localeCompare(b[0])).forEach(([n,d])=>{const el=itemTile(n);el.onclick=()=>{box[3].push([n,"",0]);save();dlg.close();tip.hidden=true;render()};dlg.querySelector(`.tg[data-t="${d.t}"]`).appendChild(el)})};
  draw()}
function itemDialog(box,ii){
  const it=box[3][ii],[n,note,imb]=it,d=itemInfo(n),hero=HERO_BY_KEY[cur.hk];
  openDlg(`<h3>${esc(n)}</h3><p class="meta">${CATN[d.c]} · ${COST[d.t].toLocaleString("en-GB")} souls</p>
    <label class="fl">Note<textarea rows="3" id="fnote">${esc(note)}</textarea></label>
    ${d.i?`<label class="fl">Imbue<select id="fimb"><option value="0">None</option>${hero.ab.map((a,i)=>`<option value="${i+1}" ${imb===i+1?"selected":""}>${i+1} · ${esc(a.n)}</option>`).join("")}</select></label>`:""}
    <div class="frow"><button type="button" class="pill del" id="frm">Remove</button><button type="button" class="pill" id="fok">Done</button></div>`,"itemdlg");
  const fin=()=>{it[1]=dlg.querySelector("#fnote").value.trim();const s=dlg.querySelector("#fimb");if(s)it[2]=+s.value;save();dlg.close();render()};
  dlg.querySelector("#fok").onclick=fin;
  dlg.querySelector("#frm").onclick=()=>{box[3].splice(ii,1);save();dlg.close();render()}}
function newBuildDialog(){
  openDlg(`<h3>New build</h3><div class="heroes">${HEROES.map(h=>`<button type="button" class="hb" data-k="${h.key}">${esc(h.name)}</button>`).join("")}</div>`,"newdlg");
  dlg.querySelectorAll(".hb").forEach(btn=>btn.onclick=()=>{const h=HERO_BY_KEY[btn.dataset.k];
    const b={id:"u"+Date.now().toString(36),hk:h.key,name:`New ${h.name} build`,desc:"",order:[],rows:[
      [["Losing lane? Buy 1","",true,[]],["Early · L-R","",false,[]]],[["Mid · L-R","",false,[]]],[["Late · L-R","",false,[]],["Counters","",true,[]]],[["I'm rich as fuck","",true,[]],["Slot locked?","If the slot is locked, buy it now. Otherwise last buy.",true,[]]]]};
    MINE.push(b);saveMine();dlg.close();editing=true;show(b.id,true)})}

/* ---------- start ---------- */
let start=store.get("rz-build","danny");if(!findBuild(start))start=PRESETS[0].id;
show(start);
try{const ro=new ResizeObserver(()=>document.documentElement.style.setProperty("--dockh",dock.offsetHeight+"px"));ro.observe(dock)}catch(e){}
