from common import page

BODY = r"""
  <section class="panel">
    <h2><span class="tag">5a–b</span>Response from shifted step responses</h2>
    <p class="note">Known: the step response h(t) = 2(1 − e<sup>−t</sup>)σ(t). An input made of steps, A·σ(t−t₁) − A·σ(t−t₃), gives A·h(t−t₁) − A·h(t−t₃): scale by A (Linearität), delay by t₁ and t₃ (Zeitinvarianz), and add.</p>
    <div class="row">
      <div class="slider"><span class="m">A</span><input type="range" id="amp" min="0.5" max="5" step="0.5" value="3" aria-label="amplitude"><span class="val" id="ampv"></span></div>
      <div class="slider"><span class="m">t₁</span><input type="range" id="t1" min="0" max="3" step="0.25" value="1" aria-label="t1"><span class="val" id="t1v"></span></div>
    </div>
    <div class="row">
      <div class="slider"><span class="m">t₃</span><input type="range" id="t3" min="0.5" max="6" step="0.25" value="3" aria-label="t3"><span class="val" id="t3v"></span></div>
      <label class="chk"><input type="checkbox" id="second" checked><span>second step (rectangle)</span></label>
    </div>
    <div class="row">
      <div class="slider"><span class="m">t*</span><input type="range" id="probe" min="0" max="8" step="0.05" value="4" aria-label="probe time"><span class="val" id="probev"></span></div>
      <button id="exam">Exam values</button>
    </div>
    <div class="formula" id="yFormula"></div>
    <div class="formula" id="yProbe"></div>
    <div class="legend"><span style="--c:var(--muted)">input x(t)</span><span class="dash" style="--c:var(--x)">A·h(t − t₁)</span><span class="dash" style="--c:var(--g)">−A·h(t − t₃)</span><span style="--c:var(--y)">y(t) = sum</span></div>
    <div class="plotbox" id="pA"></div>
    <p class="note" id="examNote"></p>
  </section>

  <section class="panel">
    <h2><span class="tag">5c–d</span>Faltungsintegral: y(t) = ∫ x(τ) · g(t − τ) dτ</h2>
    <p class="note">The impulse response is g(t) = ḣ(t) = 2e<sup>−t</sup>σ(t). Flip it and move it to position t: g(t − τ) starts at τ = t and decays to the <i>left</i>. y(t) is the shaded area under x(τ)·g(t − τ). The two σ factors set the integration limits.</p>
    <div class="row"><span class="label">Input</span><div class="seg" id="inp" role="group" aria-label="Input"></div></div>
    <div class="row">
      <div class="slider"><span class="m">t</span><input type="range" id="tc" min="-1" max="8" step="0.05" value="2" aria-label="t"><span class="val" id="tcv"></span></div>
      <button id="play">Play</button>
    </div>
    <div class="formula" id="cFormula"></div>
    <div class="legend"><span style="--c:var(--x)">x(τ)</span><span style="--c:var(--g)">g(t − τ)</span><span style="--c:var(--p)">x(τ)·g(t − τ), area = y(t)</span></div>
    <div class="plotbox" id="pC"></div>
    <div class="legend"><span style="--c:var(--y)">y(t) so far</span><span class="dash" style="--c:var(--muted)">full y(t)</span></div>
    <div class="plotbox" id="pD"></div>
  </section>
"""

SCRIPT = r"""
const h = (t) => 2 * (1 - Math.exp(-t)) * sig(t);
const g = (t) => 2 * Math.exp(-t) * sig(t);

// ---------- 5a/b ----------
function P() { return { A: +$("amp").value, t1: +$("t1").value, t3: +$("t3").value, two: $("second").checked, ts: +$("probe").value }; }
$("exam").addEventListener("click", () => { $("amp").value = 3; $("t1").value = 1; $("t3").value = 3; $("second").checked = true; $("probe").value = 4; render(); });

// ---------- 5c/d ----------
const INPUTS = {
  step: { name: "x(t) = σ(t)  (5d)", x: (t) => sig(t), exact: (t) => h(t) },
  rect: { name: "x(t) = 3σ(t−1) − 3σ(t−3)  (5b)", x: (t) => 3 * sig(t - 1) - 3 * sig(t - 3), exact: (t) => 3 * h(t - 1) - 3 * h(t - 3) },
};
let inp = "step", timer = null;
Object.entries(INPUTS).forEach(([k, v]) => {
  const b = document.createElement("button"); b.textContent = v.name; b.dataset.key = k;
  b.addEventListener("click", () => { inp = k; render(); }); $("inp").appendChild(b);
});
function conv(xf, t) {          // Simpson, split at the jumps of x (0, 1, 3) and of g(t − τ) (τ = t)
  const br = [-2, 0, 1, 3, t].filter((u) => u <= t).sort((a, b) => a - b);
  let s = 0;
  for (let k = 0; k < br.length - 1; k++) {
    const a = br[k] + 1e-9, b = br[k + 1] - 1e-9; if (b <= a) continue;
    const m = 200, d = (b - a) / m, F = (u) => xf(u) * g(t - u);
    let acc = F(a) + F(b);
    for (let i = 1; i < m; i++) acc += (i % 2 ? 4 : 2) * F(a + i * d);
    s += acc * d / 3;
  }
  return s;
}
function stop() { if (timer) clearInterval(timer); timer = null; $("play").textContent = "Play"; }
$("play").addEventListener("click", () => {
  if (timer) { stop(); return; }
  if (+$("tc").value >= 8) $("tc").value = -1;
  $("play").textContent = "Pause";
  timer = setInterval(() => { const v = +$("tc").value + 0.1; if (v > 8) { stop(); return; } $("tc").value = v; render(); }, 80);
});

function render() {
  // 5a/b
  const p = P();
  if (p.t3 <= p.t1) { p.t3 = p.t1 + 0.25; $("t3").value = p.t3; }
  $("ampv").textContent = "A = " + fmt(p.A); $("t1v").textContent = "t₁ = " + fmt(p.t1);
  $("t3v").textContent = "t₃ = " + fmt(p.t3); $("probev").textContent = "t* = " + fmt(p.ts, 2);
  $("t3").disabled = !p.two;
  const x = (t) => p.A * sig(t - p.t1) - (p.two ? p.A * sig(t - p.t3) : 0);
  const y1 = (t) => p.A * h(t - p.t1), y2 = (t) => (p.two ? -p.A * h(t - p.t3) : 0);
  const y = (t) => y1(t) + y2(t);
  const ser = [{ kind: "line", pts: sample(x, -0.5, 8, 0.01), color: "--muted", w: 1.6 },
               { kind: "line", pts: sample(y1, -0.5, 8, 0.01), color: "--x", w: 1.6, dash: "6 4" }];
  if (p.two) ser.push({ kind: "line", pts: sample(y2, -0.5, 8, 0.01), color: "--g", w: 1.6, dash: "6 4" });
  ser.push({ kind: "line", pts: sample(y, -0.5, 8, 0.01), color: "--y", w: 3 });
  plot($("pA"), { x: [-0.5, 8], h: 260, xlabel: "t", series: ser, vlines: [{ x: p.ts, color: "--muted", label: "t*" }],
    dots: [{ x: p.ts, y: y(p.ts), color: "--y", label: fmt(y(p.ts), 3) }] });
  const A2 = fmt(2 * p.A), sh = (t) => (t === 0 ? "t" : `t−${fmt(t)}`);
  const term = (tk) => `${A2}(1 − e<sup>−(${sh(tk)})</sup>)σ(${sh(tk)})`;
  $("yFormula").innerHTML = "y(t) = " + term(p.t1) + (p.two ? " − " + term(p.t3) : "");
  const parts = [];
  if (p.ts >= p.t1) parts.push(`${A2}(1 − e<sup>−${fmt(p.ts - p.t1, 2)}</sup>)`);
  if (p.two && p.ts >= p.t3) parts.push(`${A2}(1 − e<sup>−${fmt(p.ts - p.t3, 2)}</sup>)`);
  $("yProbe").innerHTML = `y(${fmt(p.ts, 2)}) = ` + (parts.length ? parts.join(" − ") : "0 (no step has started yet)") + ` = ${fmt(y(p.ts), 4)}`;
  const isExam = p.A === 3 && p.t1 === 1 && p.t3 === 3 && p.two;
  $("examNote").innerHTML = isExam
    ? `Exam case (Aufgabe 5b): y(2) = ${fmt(y(2), 4)}, y(3) = ${fmt(y(3), 4)}, y(4) = ${fmt(y(4), 4)}. Untick the second step for Aufgabe 5a, y(t) = 3h(t − 1).`
    : `Press “Exam values” to return to Aufgabe 5b.`;

  // 5c/d
  pressGroup($("inp"), inp);
  const I = INPUTS[inp], t = +$("tc").value;
  $("tcv").textContent = "t = " + fmt(t, 2);
  const prod = (u) => I.x(u) * g(t - u);
  plot($("pC"), { x: [-2, 8.5], h: 230, xlabel: "τ", y: [-0.3, inp === "rect" ? 6.6 : 2.4], series: [
    { kind: "area", pts: sample(prod, -2, 8.5, 0.005, 0.4), color: "--p", fop: 0.3 },
    { kind: "line", pts: sample(I.x, -2, 8.5, 0.005), color: "--x", w: 2.4 },
    { kind: "line", pts: sample((u) => g(t - u), -2, 8.5, 0.005, 0.4), color: "--g", w: 2.4 },
    { kind: "line", pts: sample(prod, -2, 8.5, 0.005, 0.4), color: "--p", w: 1.4 }],
    vlines: [{ x: t, color: "--g", label: "τ = t" }] });
  const val = conv(I.x, t);
  const yfull = sample(I.exact, -1, 8, 0.02), ysofar = sample(I.exact, -1, t, 0.02);
  plot($("pD"), { x: [-1, 8], h: 170, xlabel: "t", series: [
    { kind: "line", pts: yfull, color: "--muted", w: 1.4, dash: "5 4" },
    { kind: "line", pts: ysofar, color: "--y", w: 3 }], dots: [{ x: t, y: val, color: "--y", label: fmt(val, 3) }] });
  let lim;
  if (inp === "step") lim = t <= 0 ? "no overlap (t ≤ 0) → y(t) = 0" : `limits 0 … ${fmt(t, 2)}: ∫<sub>0</sub><sup>${fmt(t, 2)}</sup> 2e<sup>−(t−τ)</sup> dτ = 2(1 − e<sup>−${fmt(t, 2)}</sup>)`;
  else lim = t <= 1 ? "no overlap (t ≤ 1) → y(t) = 0" : `overlap τ ∈ [1, ${fmt(Math.min(t, 3), 2)}]`;
  $("cFormula").innerHTML = `y(${fmt(t, 2)}) = ${lim} = ${fmt(val, 4)}   (exact: ${fmt(I.exact(t), 4)})`;
}
["amp", "t1", "t3", "second", "probe"].forEach((id) => $(id).addEventListener("input", render));
$("tc").addEventListener("input", () => { stop(); render(); });
onRedraw(render);
render();
"""

HTML = page("Superposition & Faltungsintegral",
            "Superposition &amp; Faltungsintegral (CT)",
            "Aufgabe 5 of the Kap. 6 Übungsklausur, interactive: build the response to a rectangular pulse from shifted step "
            "responses, then watch the convolution integral compute the same thing (Folie 148–155, Formelblatt Nr. 20).",
            BODY, SCRIPT)
