"""FT1 Modul 1 – Kostenvergleichsrechnung & Grenzstückzahl (Skript Folie 31–32, Probeklausur Modul 1 Aufgabe 6)."""
from common import page

BODY = r"""
<style>
.presets{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:720px){.grid{grid-template-columns:1fr}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.card h2{font-size:1rem;margin:0 0 10px;display:flex;align-items:center;gap:8px}
.dot{width:12px;height:12px;border-radius:50%;display:inline-block}
label{display:grid;grid-template-columns:1fr 92px;align-items:center;gap:8px;margin:5px 0;font-size:.92rem;color:var(--muted)}
input[type=number]{width:100%;font:inherit;padding:4px 6px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);text-align:right}
.mslider{margin-top:14px}
.mslider input{width:100%}
.res{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin-top:14px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 12px}
.kpi .l{font-size:.8rem;color:var(--muted)}
.kpi .v{font-size:1.05rem;font-weight:650;font-variant-numeric:tabular-nums}
.note{color:var(--muted);font-size:.88rem;margin-top:12px}
.presets button.on{background:var(--fg);color:var(--panel);border-color:var(--fg)}
.card{min-width:0}
</style>



<div class="presets" id="presets"></div>

<div class="grid">
  <div class="card" id="cardA"></div>
  <div class="card" id="cardB"></div>
</div>

<div class="card mslider">
  <label><span>Fertigungsmenge <i>m</i> [Stück]</span><input type="number" id="mNum" min="1" step="1"></label>
  <input type="range" id="m" min="1" max="3000" step="1" aria-label="Fertigungsmenge">
</div>

<div class="res" id="res"></div>

<div class="card" style="margin-top:14px">
  <svg id="chart" viewBox="0 0 640 330" role="img" aria-label="Kostengeraden beider Alternativen"></svg>
</div>

<p class="note">Formeln wie im Skript: <code>t_r = t_rg + t_rv + t_rer</code>, <code>t_e = t_h + t_n + t_v + t_er</code>, <code>T_a = t_r + m·t_e</code>, <code>K = (Maschinenstundensatz + Fertigungslohn)·T_a</code> (T_a in h). Grenzstückzahl aus K_A(m) = K_B(m), aufgerundet auf ganze Stück.</p>

"""

SCRIPT = r"""

const PRESETS={
  skript:{name:"Skript: Fräs- vs. Walzmaschine",A:{n:"Fräsmaschine",tr:10,te:2.5,M:25,L:35},B:{n:"Walzmaschine",tr:40,te:1.0,M:49,L:35},m:2000},
  probe:{name:"Probeklausur A6: Bohrmaschine vs. BAZ",A:{n:"Säulenbohrmaschine",tr:7,te:3.0,M:18,L:36},B:{n:"Bearbeitungszentrum",tr:75,te:1.2,M:70,L:36},m:1200}
};
let st=JSON.parse(JSON.stringify(PRESETS.probe)), cur="probe";
const fde=(v,d=2)=>v.toLocaleString("de-DE",{minimumFractionDigits:d,maximumFractionDigits:d});
function card(k){
  const c=st[k], col=k==="A"?"var(--x)":"var(--bad)";
  $("card"+k).innerHTML=`<h2><span class="dot" style="background:${col}"></span>${k}: <span>${c.n}</span></h2>
  <label><span>Rüstzeit t<sub>r</sub> [min]</span><input type="number" step="0.1" data-k="${k}" data-f="tr" value="${c.tr}"></label>
  <label><span>Zeit je Einheit t<sub>e</sub> [min/Stück]</span><input type="number" step="0.1" data-k="${k}" data-f="te" value="${c.te}"></label>
  <label><span>Maschinenstundensatz [€/h]</span><input type="number" step="1" data-k="${k}" data-f="M" value="${c.M}"></label>
  <label><span>Fertigungslohn [€/h]</span><input type="number" step="1" data-k="${k}" data-f="L" value="${c.L}"></label>`;
}
function K(c,m){return (c.tr+m*c.te)/60*(c.M+c.L)}
function breakeven(){
  const a=st.A,b=st.B, ra=a.M+a.L, rb=b.M+b.L, den=a.te*ra-b.te*rb;
  if(Math.abs(den)<1e-12) return null;
  const m=(b.tr*rb-a.tr*ra)/den; return m>0?m:null;
}
function render(){
  const m=st.m, KA=K(st.A,m), KB=K(st.B,m), be=breakeven();
  const cheaper=KA<KB?"A":(KB<KA?"B":"–");
  let beTxt="kein Schnittpunkt (m > 0)", beSub="";
  if(be!==null){beTxt=fde(be,1)+" Stück"; const up=Math.ceil(be); const above=K(st.A,up+1)>K(st.B,up+1)?"B":"A"; beSub=`ab ${up.toLocaleString("de-DE")} Stück ist ${above} günstiger`;}
  $("res").innerHTML=`
   <div class="kpi"><div class="l">T<sub>a</sub> A / B</div><div class="v">${fde((st.A.tr+m*st.A.te)/60)} h / ${fde((st.B.tr+m*st.B.te)/60)} h</div></div>
   <div class="kpi"><div class="l">Gesamtkosten A</div><div class="v" style="color:var(--x)">${fde(KA)} €</div><div class="l">${fde(KA/m,3)} €/Stück</div></div>
   <div class="kpi"><div class="l">Gesamtkosten B</div><div class="v" style="color:var(--bad)">${fde(KB)} €</div><div class="l">${fde(KB/m,3)} €/Stück</div></div>
   <div class="kpi"><div class="l">Grenzstückzahl m*</div><div class="v">${beTxt}</div><div class="l">${beSub}</div></div>
   <div class="kpi"><div class="l">Bei m = ${m.toLocaleString("de-DE")} wirtschaftlicher</div><div class="v" style="color:var(--ok)">${cheaper==="–"?"gleich":cheaper}</div><div class="l">${cheaper==="–"?"":st[cheaper].n}</div></div>`;
  draw(be);
}
function draw(be){
  const W=640,H=330,l=72,r=16,t=14,bm=42, mMax=Math.max(st.m*1.25,be?be*2:0,50);
  const kMax=Math.max(K(st.A,mMax),K(st.B,mMax))*1.05;
  const X=m=>l+(W-l-r)*m/mMax, Y=k=>H-bm-(H-t-bm)*k/kMax;
  const ink=css("--fg"),mute=css("--muted"),line=css("--line");
  let s="";
  const nice=v=>{const p=Math.pow(10,Math.floor(Math.log10(v)));const f=v/p;return (f<=2?2:f<=5?5:10)*p/5;};
  const sx=nice(mMax), sy=nice(kMax);
  for(let v=0;v<=mMax;v+=sx){s+=`<line x1="${X(v)}" x2="${X(v)}" y1="${t}" y2="${H-bm}" stroke="${line}"/><text x="${X(v)}" y="${H-bm+16}" fill="${mute}" font-size="11" text-anchor="middle">${v.toLocaleString("de-DE")}</text>`}
  for(let v=0;v<=kMax;v+=sy){s+=`<line x1="${l}" x2="${W-r}" y1="${Y(v)}" y2="${Y(v)}" stroke="${line}"/><text x="${l-6}" y="${Y(v)+4}" fill="${mute}" font-size="11" text-anchor="end">${v.toLocaleString("de-DE")}</text>`}
  s+=`<line x1="${X(0)}" y1="${Y(K(st.A,0))}" x2="${X(mMax)}" y2="${Y(K(st.A,mMax))}" stroke="${css("--x")}" stroke-width="2.5"/>`;
  s+=`<line x1="${X(0)}" y1="${Y(K(st.B,0))}" x2="${X(mMax)}" y2="${Y(K(st.B,mMax))}" stroke="${css("--bad")}" stroke-width="2.5" stroke-dasharray="7 4"/>`;
  if(be!==null&&be<=mMax){s+=`<circle cx="${X(be)}" cy="${Y(K(st.A,be))}" r="5" fill="${ink}"/><text x="${X(be)+8}" y="${Y(K(st.A,be))+18}" style="fill:${ink}" font-size="12">m* ≈ ${fde(be,1)}</text>`}
  s+=`<line x1="${X(st.m)}" x2="${X(st.m)}" y1="${t}" y2="${H-bm}" stroke="${css("--ok")}" stroke-dasharray="3 3"/>`;
  s+=`<text x="${(l+W-r)/2}" y="${H-6}" fill="${mute}" font-size="12" text-anchor="middle">Fertigungsmenge m [Stück]</text>`;
  s+=`<text transform="translate(16 ${(t+H-bm)/2}) rotate(-90)" fill="${mute}" font-size="12" text-anchor="middle">Gesamtkosten K [€]</text>`;
  s+=`<text x="${l+8}" y="${t+14}" style="fill:${css("--x")}" font-size="12">— A: ${st.A.n}</text><text x="${l+8}" y="${t+30}" style="fill:${css("--bad")}" font-size="12">- - B: ${st.B.n}</text>`;
  $("chart").innerHTML=s;
}
function load(key){
  cur=key; st=JSON.parse(JSON.stringify(PRESETS[key]));
  card("A");card("B"); $("m").value=st.m; $("mNum").value=st.m;
  document.querySelectorAll("#presets button").forEach(b=>b.classList.toggle("on",b.dataset.p===key)); render();
}
$("presets").innerHTML=Object.entries(PRESETS).map(([k,p])=>`<button data-p="${k}">${p.name}</button>`).join("");
$("presets").addEventListener("click",e=>{if(e.target.dataset.p)load(e.target.dataset.p)});
document.addEventListener("input",e=>{
  const el=e.target;
  if(el.dataset.k){const v=parseFloat(el.value); if(!isNaN(v)){st[el.dataset.k][el.dataset.f]=v; render();}}
  if(el.id==="m"){st.m=+el.value;$("mNum").value=st.m;render();}
  if(el.id==="mNum"){const v=Math.max(1,parseInt(el.value)||1);st.m=v;$("m").value=Math.min(v,3000);render();}
});
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",render);
load("probe");

"""

HTML = page("Kostenvergleich & Grenzstückzahl", "Kostenvergleichsrechnung &amp; Grenzstückzahl",
            "FT1 · Modul 1 (Folien 31–32). Bewege die Fertigungsmenge <span class=\"m\">m</span> oder ändere die Angaben und sieh, wo sich die Kostengeraden schneiden.",
            BODY, SCRIPT, crumb="Fertigungstechnik 1 · Modul 1")
