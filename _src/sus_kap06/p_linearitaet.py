from common import page

BODY = r"""
  <section class="panel">
    <div class="row"><span class="label">System</span><div class="seg" id="sys" role="group" aria-label="System"></div></div>
    <div class="formula" id="eq"></div>
    <div class="row" id="verdicts"></div>
  </section>

  <section class="panel">
    <h2><span class="tag">Test 1</span>Linearität: λ-Test</h2>
    <p class="note">Scale the input by λ. A linear system gives exactly λ times the old output, so the two curves lie on top of each other.</p>
    <div class="row">
      <div class="slider"><span class="m">λ</span><input type="range" id="lam" min="-2" max="3" step="0.25" value="2" aria-label="lambda"><span class="val" id="lamv"></span></div>
      <span id="linv"></span>
    </div>
    <div class="legend"><span style="--c:var(--x)">response to λ·x</span><span class="dash" style="--c:var(--g)">λ · (response to x)</span></div>
    <div class="plotbox" id="pL"></div>
  </section>

  <section class="panel">
    <h2><span class="tag">Test 2</span>Zeitinvarianz: Verschiebe-Test</h2>
    <p class="note">Delay the input by a. A time-invariant system gives the same output, just delayed by a ("heute genauso wie morgen").</p>
    <div class="row">
      <div class="slider"><span class="m">a</span><input type="range" id="sh" min="0" max="3" step="0.25" value="1.5" aria-label="shift a"><span class="val" id="shv"></span></div>
      <span id="tiv"></span>
    </div>
    <div class="legend"><span style="--c:var(--x)">response to the delayed input</span><span class="dash" style="--c:var(--g)">old response, delayed by a</span></div>
    <div class="plotbox" id="pT"></div>
  </section>

  <section class="panel">
    <h2>Equation test (what you write in the exam)</h2>
    <div id="why"></div>
  </section>
"""

SCRIPT = r"""
// ---------- systems from Aufgabe 1 ----------
const DT_N = 16;
const xDT = (n) => ({ 0: 1, 1: 2, 2: -1, 3: 0.5 }[n] || 0);              // test input x[n]
const bump = (t) => (t >= 0.5 && t <= 2.5 ? Math.pow(Math.sin(Math.PI * (t - 0.5) / 2), 2) : 0);  // test input x(t)

function simDT(step, x) {        // step(n, x, y) -> y[n]; system starts at rest
  const y = [];
  const Y = (k) => (k >= 0 ? y[k] : 0);
  for (let n = 0; n < DT_N; n++) y.push(step(n, x, Y));
  return y;
}
function rk4(f, x, T, dt, dim) { // f(t, z, x) -> dz ; returns [t, z]
  let z = new Array(dim).fill(0); const out = [[0, z.slice()]];
  for (let t = 0; t < T - 1e-9; t += dt) {
    const k1 = f(t, z, x), z2 = z.map((v, i) => v + dt / 2 * k1[i]);
    const k2 = f(t + dt / 2, z2, x), z3 = z.map((v, i) => v + dt / 2 * k2[i]);
    const k3 = f(t + dt / 2, z3, x), z4 = z.map((v, i) => v + dt * k3[i]);
    const k4 = f(t + dt, z4, x);
    z = z.map((v, i) => v + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]));
    out.push([t + dt, z.slice()]);
  }
  return out;
}
const DT = 0.01;
const SYS = {
  A: { dt: true, eq: "y[n] = x[n] · y[n−1]", lin: false, ti: true,
       run: (x) => simDT((n, x, Y) => x(n) * Y(n - 1), x),
       why: `Substitute x → λx and y → λy: <span class="m">λy[n] = λx[n] · λy[n−1] = λ²·x[n]y[n−1]</span>. λ does not cancel, so the system is <b>nicht linear</b> (product of two signals). <span class="m">n</span> does not appear on its own, so it is <b>zeitinvariant</b>.<br><br><b>Why the plots show only zeros:</b> starting from rest, <span class="m">y[−1] = 0</span>, so every later value is 0 too, whatever the input. The simulation can't reveal the nonlinearity here; the equation test can. That's why the exam asks for the equation argument.` },
  B: { dt: true, eq: "y[n] = 0.5·y[n−1] + n·x[n]", lin: true, ti: false,
       run: (x) => simDT((n, x, Y) => 0.5 * Y(n - 1) + n * x(n), x),
       why: `λ factors out of every term: <span class="m">λy[n] = 0.5·λy[n−1] + n·λx[n]</span> → <b>linear</b>. The coefficient <span class="m">n</span> appears explicitly, so a delayed input meets a different factor → <b>nicht zeitinvariant</b>.` },
  C: { dt: true, eq: "Y/X = R / (1 − 0.5R²)   ⇔   y[n] = x[n−1] + 0.5·y[n−2]", lin: true, ti: true,
       run: (x) => simDT((n, x, Y) => x(n - 1) + 0.5 * Y(n - 2), x),
       why: `Operator form ⇒ LTI. Written out, <span class="m">y[n] = x[n−1] + 0.5y[n−2]</span>: constant coefficients, no products, no explicit <span class="m">n</span> → <b>linear</b> and <b>zeitinvariant</b>.` },
  D: { dt: false, eq: "y(t) = x(t − 2) + 1", lin: false, ti: true, T: 8, rest: 1,
       run: (x) => { const o = []; for (let t = 0; t <= 8 + 1e-9; t += DT) o.push([t, x(t - 2) + 1]); return o; },
       why: `<span class="m">λ·(x(t−2) + 1) = λx(t−2) + λ ≠ λx(t−2) + 1</span> → <b>nicht linear</b>. The constant offset is the culprit: with <span class="m">x = 0</span> a linear system must give <span class="m">y = 0</span>, here it gives 1. The delay <span class="m">x(t−2)</span> is only a shifted signal, not an explicit <span class="m">t</span> → <b>zeitinvariant</b>.` },
  E: { dt: false, eq: "ẏ(t) = sin(t) · y(t) + x(t)", lin: true, ti: false, T: 8,
       run: (x) => rk4((t, z, x) => [Math.sin(t) * z[0] + x(t)], x, 8, DT, 1).map(([t, z]) => [t, z[0]]),
       why: `λ factors out: <span class="m">λẏ = sin(t)·λy + λx</span> → <b>linear</b>. The coefficient <span class="m">sin(t)</span> depends explicitly on <span class="m">t</span>, so a delayed input sees a different gain → <b>nicht zeitinvariant</b>.` },
  F: { dt: false, eq: "2ÿ(t) − 5y(t) = ẋ(t) − 3x(t)", lin: true, ti: true, T: 4.5,
       // G(s) = (s − 3)/(2s² − 5): z1' = z2, z2' = 2.5 z1 + x, y = −1.5 z1 + 0.5 z2
       run: (x) => rk4((t, z, x) => [z[1], 2.5 * z[0] + x(t)], x, 4.5, DT, 2).map(([t, z]) => [t, -1.5 * z[0] + 0.5 * z[1]]),
       why: `Constant coefficients, every term contains exactly one signal → <b>linear</b> and <b>zeitinvariant</b> (LTI). It is unstable (poles <span class="m">s = ±√2.5</span>), which is why the output grows, but stability has nothing to do with being LTI.` },
};

let key = "B";
const sysEl = $("sys");
Object.keys(SYS).forEach((k) => {
  const b = document.createElement("button"); b.textContent = k; b.dataset.key = k; b.setAttribute("aria-pressed", "false");
  b.title = SYS[k].eq; b.addEventListener("click", () => { key = k; render(); }); sysEl.appendChild(b);
});

function pill(ok, yes, no) { return `<span class="pill ${ok ? "ok" : "bad"}">${ok ? yes : no}</span>`; }
function maxdiff(a, b) { let m = 0, s = 1; a.forEach((v, i) => { m = Math.max(m, Math.abs(v - b[i])); s = Math.max(s, Math.abs(v), Math.abs(b[i])); }); return m / s; }

function render() {
  const S = SYS[key]; pressGroup(sysEl, key);
  $("eq").textContent = S.eq;
  const lam = parseFloat($("lam").value); $("lamv").textContent = "λ = " + fmt(lam);
  let a = parseFloat($("sh").value);
  if (S.dt) { $("sh").step = 1; $("sh").max = 5; a = Math.round(a); $("sh").value = a; } else { $("sh").step = 0.25; $("sh").max = 3; }
  $("shv").textContent = "a = " + fmt(a);

  if (S.dt) {
    const y = S.run(xDT), yl = S.run((n) => lam * xDT(n)), ly = y.map((v) => lam * v);
    const ys = S.run((n) => xDT(n - a)), yd = y.map((_, n) => (n - a >= 0 ? y[n - a] : 0));
    const linOK = maxdiff(yl, ly) < 1e-9, tiOK = maxdiff(ys, yd) < 1e-9;
    $("linv").innerHTML = pill(linOK, "curves identical → passes", "curves differ → nicht linear");
    $("tiv").innerHTML = pill(tiOK, "curves identical → passes", "curves differ → nicht zeitinvariant");
    const st = (arr, c, extra) => ({ kind: "stem", pts: arr.map((v, n) => [n, v]), color: c, ...extra });
    plot($("pL"), { x: [-0.8, DT_N - 0.2], xint: true, h: 210, xlabel: "n", series: [st(yl, "--x", { r: 5 }), st(ly, "--g", { r: 3, fill: true, w: 0 })] });
    plot($("pT"), { x: [-0.8, DT_N - 0.2], xint: true, h: 210, xlabel: "n", series: [st(ys, "--x", { r: 5 }), st(yd, "--g", { r: 3, fill: true, w: 0 })] });
  } else {
    const y = S.run(bump), yl = S.run((t) => lam * bump(t)), ly = y.map(([t, v]) => [t, lam * v]);
    const ys = S.run((t) => bump(t - a));
    const rest = S.rest || 0;
    const yd = y.map(([t]) => { const k = Math.round((t - a) / DT); return [t, k >= 0 ? y[k][1] : rest]; });
    const linOK = maxdiff(yl.map((p) => p[1]), ly.map((p) => p[1])) < 1e-6;
    const tiOK = maxdiff(ys.map((p) => p[1]), yd.map((p) => p[1])) < 1e-4;
    $("linv").innerHTML = pill(linOK, "curves identical → passes", "curves differ → nicht linear");
    $("tiv").innerHTML = pill(tiOK, "curves identical → passes", "curves differ → nicht zeitinvariant");
    const T = S.T;
    plot($("pL"), { x: [0, T], h: 210, xlabel: "t", series: [
      { kind: "line", pts: yl, color: "--x", w: 3 }, { kind: "line", pts: ly, color: "--g", w: 2, dash: "6 4" }] });
    plot($("pT"), { x: [0, T], h: 210, xlabel: "t", series: [
      { kind: "line", pts: ys, color: "--x", w: 3 }, { kind: "line", pts: yd, color: "--g", w: 2, dash: "6 4" }] });
  }
  $("verdicts").innerHTML = `Answer key: ${pill(S.lin, "linear", "nicht linear")} ${pill(S.ti, "zeitinvariant", "nicht zeitinvariant")}`;
  $("why").innerHTML = `<p style="margin:0">${S.why}</p>`;
}
["lam", "sh"].forEach((id) => $(id).addEventListener("input", render));
onRedraw(render);
render();
"""

HTML = page("Linearität & Zeitinvarianz",
            "Linearität &amp; Zeitinvarianz testen",
            "The six systems from Aufgabe 1 of the Kap. 6 Übungsklausur. Pick one, then run the two tests from Folie 144–145: "
            "scale the input (λ-test) and delay it (shift test). The test input is a short pulse.",
            BODY, SCRIPT)
