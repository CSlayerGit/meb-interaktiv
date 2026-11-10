from common import page

BODY = r"""
  <section class="panel">
    <h2><span class="tag">3a</span>Build f[n] from windows and one δ</h2>
    <p class="note">Switch the terms on and compare with the grey target from the exam figure. Then try the <i>difference form</i>: it describes the same signal, but every window must end one sample later (σ[n−5], not σ[n−4]).</p>
    <div class="row"><span class="label">Form</span><div class="seg" id="form" role="group" aria-label="Form"></div></div>
    <div class="row" id="terms"></div>
    <div class="formula" id="aFormula"></div>
    <div class="row"><span id="aState"></span></div>
    <div class="legend"><span style="--c:var(--muted)">target f[n]</span><span style="--c:var(--x)">your model</span></div>
    <div class="plotbox" id="pA"></div>
  </section>

  <section class="panel">
    <h2><span class="tag">3b</span>Window σ[n − a] · σ[b − n] times a signal</h2>
    <p class="note">σ[n−a] keeps n ≥ a, σ[b−n] keeps n ≤ b. Because σ[0] = 1, <b>both end points are inside</b>. The exam signal is a = −1, b = 5 with (2 − n)·(−1)ⁿ.</p>
    <div class="row">
      <div class="slider"><span class="m">a</span><input type="range" id="wa" min="-3" max="4" step="1" value="-1" aria-label="window start a"><span class="val" id="wav"></span></div>
      <div class="slider"><span class="m">b</span><input type="range" id="wb" min="-1" max="8" step="1" value="5" aria-label="window end b"><span class="val" id="wbv"></span></div>
    </div>
    <div class="row" id="facs"></div>
    <div class="formula" id="bFormula"></div>
    <div class="legend"><span style="--c:var(--win)">window open</span><span style="--c:var(--g)">f[n]</span></div>
    <div class="plotbox" id="pB"></div>
    <div class="tablewrap"><table id="bTable"></table></div>
  </section>
"""

SCRIPT = r"""
const delta = (n) => (n === 0 ? 1 : 0);
const target = (n) => n * sig(n - 1) * sig(4 - n) + 2 * sig(n - 5) * sig(7 - n) - 3 * delta(n - 6);
const FORMS = {
  win: [
    { tex: "n·σ[n−1]·σ[4−n]", f: (n) => n * sig(n - 1) * sig(4 - n), what: "ramp n on n = 1…4" },
    { tex: "2·σ[n−5]·σ[7−n]", f: (n) => 2 * sig(n - 5) * sig(7 - n), what: "level 2 on n = 5…7" },
    { tex: "−3·δ[n−6]", f: (n) => -3 * delta(n - 6), what: "fix n = 6: 2 → −1" },
  ],
  diff: [
    { tex: "n·(σ[n−1] − σ[n−5])", f: (n) => n * (sig(n - 1) - sig(n - 5)), what: "ramp n on n = 1…4" },
    { tex: "2·(σ[n−5] − σ[n−8])", f: (n) => 2 * (sig(n - 5) - sig(n - 8)), what: "level 2 on n = 5…7" },
    { tex: "−3·δ[n−6]", f: (n) => -3 * delta(n - 6), what: "fix n = 6: 2 → −1" },
  ],
  wrong: [
    { tex: "n·(σ[n−1] − σ[n−4])", f: (n) => n * (sig(n - 1) - sig(n - 4)), what: "trap: switches off already at n = 4" },
    { tex: "2·(σ[n−5] − σ[n−7])", f: (n) => 2 * (sig(n - 5) - sig(n - 7)), what: "trap: switches off already at n = 7" },
    { tex: "−3·δ[n−6]", f: (n) => -3 * delta(n - 6), what: "fix n = 6: 2 → −1" },
  ],
};
const FORMNAMES = { win: "Window form", diff: "Difference form", wrong: "Difference form with the classic mistake" };
let form = "win"; const on = [true, false, false];
Object.keys(FORMS).forEach((k) => {
  const b = document.createElement("button"); b.textContent = FORMNAMES[k]; b.dataset.key = k;
  b.addEventListener("click", () => { form = k; render(); }); $("form").appendChild(b);
});
for (let i = 0; i < 3; i++) {
  const l = document.createElement("label"); l.className = "chk";
  l.innerHTML = `<input type="checkbox" id="a${i}"><span class="m" id="at${i}"></span>`;
  l.querySelector("input").addEventListener("change", (e) => { on[i] = e.target.checked; render(); });
  $("terms").appendChild(l);
}

const FACS = [{ id: "lin", tex: "(2 − n)", on: true }, { id: "alt", tex: "(−1)ⁿ", on: true }];
FACS.forEach((f) => {
  const l = document.createElement("label"); l.className = "chk";
  l.innerHTML = `<input type="checkbox" checked><span class="m">${f.tex}</span>`;
  l.querySelector("input").addEventListener("change", (e) => { f.on = e.target.checked; render(); });
  $("facs").appendChild(l);
});
const fon = (id) => FACS.find((f) => f.id === id).on;

function render() {
  // 3a
  pressGroup($("form"), form);
  const T = FORMS[form];
  T.forEach((q, i) => { $("at" + i).textContent = q.tex; $("a" + i).checked = on[i]; $("a" + i).parentElement.classList.toggle("on", on[i]); });
  const model = (n) => T.reduce((s, q, i) => s + (on[i] ? q.f(n) : 0), 0);
  const ns = []; for (let n = -2; n <= 10; n++) ns.push(n);
  plot($("pA"), { x: [-2.6, 10.6], xint: true, y: [-2.5, 5.5], h: 230, xlabel: "n", series: [
    { kind: "stem", pts: ns.map((n) => [n, target(n)]), color: "--muted", r: 7, w: 6, op: 0.3 },
    { kind: "stem", pts: ns.map((n) => [n, model(n)]), color: "--x", labels: true }] });
  const act = T.filter((_, i) => on[i]).map((q) => q.tex);
  $("aFormula").textContent = "f[n] = " + (act.length ? act.join(" + ").replace(/\+ −/g, "− ") : "0");
  const bad = ns.filter((n) => Math.abs(model(n) - target(n)) > 1e-12);
  $("aState").innerHTML = !bad.length ? `<span class="pill ok">matches the exam figure</span>`
    : `<span class="pill bad">differs at n = ${bad.join(", ")}</span>` + (form === "wrong" && on.every(Boolean) ? ` <span class="note">σ[n−4] already switches off <i>at</i> n = 4, so the window loses its last sample.</span>` : "");

  // 3b
  const a = parseInt($("wa").value, 10), b = parseInt($("wb").value, 10);
  $("wav").textContent = "a = " + num(a); $("wbv").textContent = "b = " + num(b);
  const w = (n) => sig(n - a) * sig(b - n);
  const f = (n) => w(n) * (fon("lin") ? 2 - n : 1) * (fon("alt") ? Math.pow(-1, n) : 1);
  const nb = []; for (let n = -3; n <= 8; n++) nb.push(n);
  const bands = b >= a ? [[a - 0.45, b + 0.45]] : [];
  plot($("pB"), { x: [-3.6, 8.6], xint: true, y: [-6.5, 6.5], h: 240, xlabel: "n", series: [
    { kind: "band", pts: bands, color: "--win" },
    { kind: "stem", pts: nb.map((n) => [n, f(n)]), color: "--g", labels: true }] });
  const sa = a === 0 ? "σ[n]" : a > 0 ? `σ[n−${a}]` : `σ[n+${-a}]`;
  const sb = b === 0 ? "σ[−n]" : `σ[${b}−n]`;
  $("bFormula").textContent = `f[n] = ${sa}·${sb}` + (fon("lin") ? "·(2 − n)" : "") + (fon("alt") ? "·(−1)ⁿ" : "")
    + (a === -1 && b === 5 && fon("lin") && fon("alt") ? "   ← exam signal" : "");
  let h = "<thead><tr><th>n</th>" + nb.map((n) => `<th class="${w(n) ? "cur" : ""}">${num(n)}</th>`).join("") + "</tr></thead><tbody>";
  h += "<tr><td>window</td>" + nb.map((n) => `<td class="${w(n) ? "cur" : ""}">${w(n)}</td>`).join("") + "</tr>";
  if (fon("lin")) h += "<tr><td>2 − n</td>" + nb.map((n) => `<td class="${w(n) ? "cur" : ""}">${num(2 - n)}</td>`).join("") + "</tr>";
  if (fon("alt")) h += "<tr><td>(−1)ⁿ</td>" + nb.map((n) => `<td class="${w(n) ? "cur" : ""}">${num(Math.pow(-1, n))}</td>`).join("") + "</tr>";
  h += "<tr><td>f[n]</td>" + nb.map((n) => `<td class="${w(n) ? "cur" : ""}"><b>${fmt(f(n))}</b></td>`).join("") + "</tr></tbody>";
  $("bTable").innerHTML = h;
}
["wa", "wb"].forEach((id) => $(id).addEventListener("input", render));
onRedraw(render);
render();
"""

HTML = page("Signalmodelle DT",
            "Signalmodelle mit σ[n] und δ[n]",
            "Aufgabe 3 of the Kap. 6 Übungsklausur, interactive: put f[n] together from windows and an impulse, "
            "and see exactly which samples a window σ[n−a]·σ[b−n] keeps (Folie 160, 164).",
            BODY, SCRIPT)
