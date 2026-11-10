from common import page

BODY = r"""
  <section class="panel">
    <h2><span class="tag">2a</span>Build f(t) term by term (slope method)</h2>
    <p class="note">Walk from left to right. Every kink adds Δm·(t−t<sub>k</sub>)·σ(t−t<sub>k</sub>), every jump adds Δ·σ(t−t<sub>k</sub>). Switch the terms on one after another and watch the coloured curve grow into the dashed target f(t).</p>
    <div class="row" id="terms"></div>
    <div class="row"><button id="tNext">Next term</button><button id="tAll">All</button><button id="tNone">None</button><span id="tState"></span></div>
    <div class="formula" id="tFormula"></div>
    <div class="legend"><span class="dash" style="--c:var(--muted)">target f(t)</span><span style="--c:var(--x)">sum of the switched-on terms</span><span class="dash" style="--c:var(--g)">last term on its own</span></div>
    <div class="plotbox" id="pA"></div>
  </section>

  <section class="panel">
    <h2><span class="tag">2b</span>Discretise with step T</h2>
    <p class="note">Sample at t = n·T. Break points move to n<sub>k</sub> = t<sub>k</sub>/T, slopes are multiplied by T, jump heights stay the same.</p>
    <div class="row"><span class="label">Step T</span><div class="seg" id="Tsel" role="group" aria-label="Step T"></div></div>
    <div class="formula" id="hFormula"></div>
    <div class="legend"><span style="--c:var(--x)">h[n] = f(n·T)</span><span class="dash" style="--c:var(--muted)">f(t) drawn over n = t/T</span></div>
    <div class="plotbox" id="pB"></div>
    <p class="note" id="hNote"></p>
  </section>

  <section class="panel">
    <h2><span class="tag">2c</span>Signalschere: g(t) = (4 − t) · σ(t) · σ(sin(π t / 2))</h2>
    <p class="note">Each σ factor is a switch: the blue shading shows where all switched-on σ factors equal 1 (window open). Inside the windows you see the straight line 4 − t, outside the product is 0.</p>
    <div class="row" id="facs"></div>
    <div class="legend"><span style="--c:var(--g)">product of the switched-on factors</span><span class="dash" style="--c:var(--muted)">line 4 − t</span><span style="--c:var(--win)">window open</span></div>
    <div class="plotbox" id="pC"></div>
    <p class="note" id="cNote"></p>
  </section>
"""

SCRIPT = r"""
// ---------- 2a ----------
const TERMS = [
  { c: 2,  tk: 1, p: 1, tex: "2(t−1)σ(t−1)",  what: "kink at t = 1: slope 0 → 2" },
  { c: -2, tk: 2, p: 1, tex: "−2(t−2)σ(t−2)", what: "kink at t = 2: slope 2 → 0" },
  { c: -3, tk: 4, p: 0, tex: "−3σ(t−4)",      what: "jump at t = 4: 2 → −1" },
  { c: 1,  tk: 4, p: 1, tex: "(t−4)σ(t−4)",   what: "kink at t = 4: slope 0 → 1" },
  { c: -1, tk: 5, p: 1, tex: "−(t−5)σ(t−5)",  what: "kink at t = 5: slope 1 → 0" },
];
const termVal = (q, t) => q.c * Math.pow(t - q.tk, q.p) * sig(t - q.tk);
const fT = (t) => TERMS.reduce((s, q) => s + termVal(q, t), 0);
const on = TERMS.map(() => false); on[0] = true; let last = 0;
TERMS.forEach((q, i) => {
  const l = document.createElement("label"); l.className = "chk";
  l.innerHTML = `<input type="checkbox" id="t${i}"><span class="m">${q.tex}</span>`;
  l.querySelector("input").addEventListener("change", (e) => { on[i] = e.target.checked; if (on[i]) last = i; render(); });
  $("terms").appendChild(l);
});
$("tNext").addEventListener("click", () => { const i = on.indexOf(false); if (i >= 0) { on[i] = true; last = i; } render(); });
$("tAll").addEventListener("click", () => { on.fill(true); last = TERMS.length - 1; render(); });
$("tNone").addEventListener("click", () => { on.fill(false); last = -1; render(); });

// ---------- 2b ----------
let T = 0.5;
[1, 0.5, 0.25].forEach((v) => {
  const b = document.createElement("button"); b.textContent = "T = " + v; b.dataset.key = String(v);
  b.addEventListener("click", () => { T = v; render(); }); $("Tsel").appendChild(b);
});
function hFormula(T) {
  return "h[n] = " + TERMS.map((q, i) => {
    const k = q.tk / T, c = q.c * Math.pow(T, q.p);
    const cs = q.p === 0 ? fmt(c) : (Math.abs(c) === 1 ? (c < 0 ? "−" : "") : fmt(c));
    const body = q.p === 0 ? `σ[n−${k}]` : `(n−${k})σ[n−${k}]`;
    const s = (q.p === 0 ? cs + "·" : cs) + body;
    return i === 0 ? s : (s.startsWith("−") ? " − " + s.slice(1) : " + " + s);
  }).join("");
}

// ---------- 2c ----------
const FACS = [
  { id: "lin", tex: "(4 − t)", on: true },
  { id: "s1", tex: "σ(t)", on: true },
  { id: "s2", tex: "σ(sin(π t / 2))", on: true },
];
FACS.forEach((f) => {
  const l = document.createElement("label"); l.className = "chk";
  l.innerHTML = `<input type="checkbox" ${f.on ? "checked" : ""}><span class="m">${f.tex}</span>`;
  l.querySelector("input").addEventListener("change", (e) => { f.on = e.target.checked; render(); });
  $("facs").appendChild(l);
});
const facOn = (id) => FACS.find((f) => f.id === id).on;
const win = (t) => (facOn("s1") ? sig(t) : 1) * (facOn("s2") ? (Math.sin(Math.PI * t / 2) > 1e-12 ? 1 : 0) : 1);
const gC = (t) => (facOn("lin") ? 4 - t : 1) * win(t);

function render() {
  // 2a
  TERMS.forEach((_, i) => { $("t" + i).checked = on[i]; $("t" + i).parentElement.classList.toggle("on", on[i]); });
  const sum = (t) => TERMS.reduce((s, q, i) => s + (on[i] ? termVal(q, t) : 0), 0);
  const ser = [{ kind: "line", pts: sample(fT, -1.2, 7.2, 0.01), color: "--muted", w: 2, dash: "6 4", op: 0.8 },
               { kind: "line", pts: sample(sum, -1.2, 7.2, 0.01), color: "--x", w: 3 }];
  if (last >= 0 && on[last]) ser.push({ kind: "line", pts: sample((t) => termVal(TERMS[last], t), -1.2, 7.2, 0.01), color: "--g", w: 1.6, dash: "3 3" });
  plot($("pA"), { x: [-1.2, 7.2], y: [-4.5, 5.5], h: 240, xlabel: "t", series: ser });
  const act = TERMS.filter((_, i) => on[i]);
  $("tFormula").textContent = "f(t) = " + (act.length ? act.map((q, j) => j === 0 ? q.tex : (q.tex.startsWith("−") ? " − " + q.tex.slice(1) : " + " + q.tex)).join("") : "0");
  let ok = true; for (let t = -1; t <= 7; t += 0.013) if (Math.abs(sum(t) - fT(t)) > 1e-9) { ok = false; break; }
  const firstBad = (() => { for (let t = -1; t <= 7.2; t += 0.01) if (Math.abs(sum(t) - fT(t)) > 1e-9) return t; return null; })();
  $("tState").innerHTML = ok ? `<span class="pill ok">matches f(t) everywhere</span>`
    : `<span class="pill bad">correct up to t ≈ ${fmt(Math.floor(firstBad * 10) / 10, 1)}</span>` + (last >= 0 && on[last] ? ` <span class="note">last: ${TERMS[last].what}</span>` : "");

  // 2b
  pressGroup($("Tsel"), String(T));
  const N = Math.round(7 / T);
  const stems = []; for (let n = 0; n <= N; n++) stems.push([n, fT(n * T)]);
  plot($("pB"), { x: [-0.8, N + 0.5], xint: true, y: [-2.5, 3], h: 220, xlabel: "n", series: [
    { kind: "line", pts: sample((u) => fT(u * T), -0.8, N + 0.5, 0.02 / T * T), color: "--muted", w: 1.4, dash: "5 4", op: 0.8 },
    { kind: "stem", pts: stems, color: "--x" }] });
  $("hFormula").textContent = hFormula(T);
  const jumpN = 4 / T;
  $("hNote").innerHTML = `At the jump (n = ${jumpN}) the sample takes the value right of the jump, h[${jumpN}] = ${fmt(fT(4))}, because σ[0] = 1. `
    + (T === 0.5 ? `<b>T = 0.5 is the exam case (Aufgabe 2b).</b>` : `The exam uses T = 0.5.`);

  // 2c
  const bands = []; let start = null;
  for (let t = -2; t <= 11.001; t += 0.005) {
    const w = win(t) === 1;
    if (w && start === null) start = t;
    if ((!w || t > 11) && start !== null) { bands.push([start, t]); start = null; }
  }
  if (start !== null) bands.push([start, 11]);
  const anyWin = facOn("s1") || facOn("s2");
  plot($("pC"), { x: [-2, 11], y: [-7.5, 6.5], h: 250, xlabel: "t", series: [
    ...(anyWin ? [{ kind: "band", pts: bands, color: "--win" }] : []),
    { kind: "line", pts: sample((t) => 4 - t, -2, 11, 0.05), color: "--muted", w: 1.2, dash: "4 4", op: 0.8 },
    { kind: "line", pts: sample(gC, -2, 11, 0.005, 0.2), color: "--g", w: 3 }] });
  const allOn = FACS.every((f) => f.on);
  $("cNote").innerHTML = allOn
    ? "All factors on = the exam function. sin(πt/2) has period 4 and is positive on (0, 2), (4, 6), (8, 10), …; σ(t) removes the windows left of 0. On (4, 6) the line 4 − t is already negative, so that piece lies below the axis."
    : "Switch all three factors on to get the exam function g(t).";
}
onRedraw(render);
render();
"""

HTML = page("Signalmodelle CT",
            "Signalmodelle mit σ(t)",
            "Aufgabe 2 of the Kap. 6 Übungsklausur, interactive: build the model of f(t) from σ terms, discretise it, "
            "and see how the Signalschere σ(sin(·)) cuts a line into windows (Folie 158–163).",
            BODY, SCRIPT)
