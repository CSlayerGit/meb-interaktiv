"""Shared shell (head, CSS tokens, plotting helpers) for the meb-interaktiv simulation pages."""

CSS = r"""
:root {
  --bg: #f6f7f9; --panel: #ffffff; --fg: #1c2230; --muted: #5d6678; --line: #d9dde5; --grid: #eceff4;
  --x: #2459c7; --g: #d0641a; --p: #7a3fb8; --y: #13805c; --bad: #c0392b; --ok: #13805c;
  --hl: #fff3c4; --win: rgba(36, 89, 199, 0.08);
  --font-body: "IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-math: "IBM Plex Serif", Georgia, "Times New Roman", serif;
  --font-mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #12151c; --panel: #1a1e27; --fg: #e4e7ee; --muted: #9aa3b5; --line: #2e3441; --grid: #232834;
    --x: #7ea6ff; --g: #f39a55; --p: #c39af0; --y: #4fd1a0; --bad: #ff7b6b; --ok: #4fd1a0;
    --hl: #3b3620; --win: rgba(126, 166, 255, 0.12); color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --bg: #12151c; --panel: #1a1e27; --fg: #e4e7ee; --muted: #9aa3b5; --line: #2e3441; --grid: #232834;
  --x: #7ea6ff; --g: #f39a55; --p: #c39af0; --y: #4fd1a0; --bad: #ff7b6b; --ok: #4fd1a0;
  --hl: #3b3620; --win: rgba(126, 166, 255, 0.12); color-scheme: dark;
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
body {
  margin: 0; background: var(--bg); color: var(--fg); font-family: var(--font-body); font-size: 15px; line-height: 1.5;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 20px 40px;
}
.wrap { max-width: 920px; margin: 0 auto; display: flex; flex-direction: column; gap: 18px; }
.crumb { font-size: 0.82rem; color: var(--muted); }
.crumb a { color: var(--x); text-decoration: none; } .crumb a:hover { text-decoration: underline; }
header h1 { font-size: 1.6rem; font-weight: 600; margin: 2px 0 4px; text-wrap: balance; letter-spacing: -0.01em; }
header p { margin: 0; color: var(--muted); max-width: 70ch; }
h2 { font-size: 1.1rem; margin: 0; font-weight: 600; }
h2 .tag { font-size: 0.75rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-right: 8px; }
.m { font-family: var(--font-math); font-style: italic; white-space: nowrap; }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.row { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; }
.label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-weight: 600; min-width: 64px; }
.seg { display: flex; flex-wrap: wrap; gap: 6px; }
button {
  font: inherit; font-size: 0.9rem; color: var(--fg); background: var(--bg); border: 1px solid var(--line);
  border-radius: 7px; padding: 6px 12px; cursor: pointer;
}
button:hover { border-color: var(--muted); }
button[aria-pressed="true"] { background: var(--fg); color: var(--panel); border-color: var(--fg); }
button:focus-visible, input:focus-visible, label:focus-within { outline: 2px solid var(--x); outline-offset: 2px; }
.chk { display: inline-flex; align-items: center; gap: 6px; padding: 5px 10px; border: 1px solid var(--line); border-radius: 7px; background: var(--bg); cursor: pointer; font-size: 0.9rem; }
.chk input { accent-color: var(--x); margin: 0; }
.chk.on { border-color: var(--muted); }
.slider { display: flex; align-items: center; gap: 8px; flex: 1 1 240px; min-width: 0; }
.slider input[type=range] { flex: 1; min-width: 80px; accent-color: var(--g); }
.val { font-family: var(--font-mono); font-size: 0.95rem; min-width: 76px; }
.formula { font-family: var(--font-math); font-size: 1.08rem; overflow-x: auto; white-space: nowrap; padding-bottom: 2px; }
.note { font-size: 0.88rem; color: var(--muted); margin: 0; }
.pill { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 0.85rem; font-weight: 600; border: 1px solid currentColor; }
.pill.ok { color: var(--ok); } .pill.bad { color: var(--bad); }
.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; font-size: 0.82rem; color: var(--muted); }
.legend span::before { content: ""; display: inline-block; width: 14px; height: 3px; margin-right: 6px; vertical-align: middle; background: var(--c); border-top: 0 dashed var(--c); }
.legend span.dash::before { background: none; border-top: 2px dashed var(--c); height: 0; }
.plotbox { min-width: 0; }
svg { display: block; width: 100%; }
svg text { font-family: var(--font-mono); font-size: 11px; fill: var(--muted); }
.tablewrap { overflow-x: auto; }
table { border-collapse: collapse; font-family: var(--font-mono); font-size: 0.85rem; font-variant-numeric: tabular-nums; }
th, td { padding: 5px 9px; text-align: right; border-bottom: 1px solid var(--line); white-space: nowrap; }
th:first-child, td:first-child { text-align: left; font-family: var(--font-math); font-style: italic; color: var(--muted); }
td.cur, th.cur { background: var(--hl); }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
"""

LIB = r"""
const $ = (id) => document.getElementById(id);
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const col = (c) => (c && c.startsWith("--") ? css(c) : c);
const fmt = (v, d = 4) => {
  if (!isFinite(v)) return "–";
  if (Math.abs(v) < 1e-10) return "0";
  const r = Math.round(v * Math.pow(10, d)) / Math.pow(10, d);
  return (r < 0 ? "−" : "") + String(Math.abs(r));
};
const num = (v) => (v < 0 ? "−" + -v : String(v));
const sig = (t) => (t >= 0 ? 1 : 0);
function niceStep(span, target) {
  const raw = span / (target || 4); const p = Math.pow(10, Math.floor(Math.log10(raw)));
  const m = raw / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p;
}
// sample f on [a,b]; insert a break (null) at jumps
function sample(f, a, b, dt, jump) {
  const pts = []; let prev = null;
  for (let t = a; t <= b + 1e-9; t += dt) {
    const v = f(t);
    if (prev !== null && Math.abs(v - prev) > (jump || 0.25)) pts.push(null);
    pts.push([t, v]); prev = v;
  }
  return pts;
}
/* plot(el, {x:[a,b], y:[lo,hi]|null, h, series:[{kind:'line'|'stem'|'area'|'band', pts, color, w, dash, op}],
             vlines:[{x,color,label}], dots:[{x,y,color,label}], xlabel, ylabel, xint}) */
function plot(el, o) {
  const W = Math.max(280, el.clientWidth || 600), H = o.h || 200;
  const ml = 44, mr = 12, mt = 16, mb = 26;
  let lo, hi;
  if (o.y) { [lo, hi] = o.y; } else {
    lo = 0; hi = 0;
    o.series.forEach((s) => { if (s.kind === "band") return; s.pts.forEach((p) => { if (p) { lo = Math.min(lo, p[1]); hi = Math.max(hi, p[1]); } }); });
    (o.dots || []).forEach((d) => { lo = Math.min(lo, d.y); hi = Math.max(hi, d.y); });
    if (hi - lo < 1e-9) { lo -= 1; hi += 1; }
    const pad = (hi - lo) * 0.12; if (lo < 0) lo -= pad; if (hi > 0) hi += pad;
  }
  const [a, b] = o.x;
  const sx = (t) => ml + ((t - a) / (b - a)) * (W - ml - mr);
  const sy = (v) => mt + ((hi - Math.max(lo, Math.min(hi, v))) / (hi - lo)) * (H - mt - mb);
  let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="${o.aria || ""}">`;
  // bands (windows) first
  o.series.filter((q) => q.kind === "band").forEach((q) => {
    q.pts.forEach(([u, v]) => { s += `<rect x="${sx(u)}" y="${mt}" width="${Math.max(0, sx(v) - sx(u))}" height="${H - mt - mb}" fill="${col(q.color || "--win")}"/>`; });
  });
  const ys = niceStep(hi - lo, Math.max(3, Math.floor((H - mt - mb) / 36)));
  for (let v = Math.ceil(lo / ys) * ys; v <= hi + 1e-9; v += ys) {
    s += `<line x1="${ml}" x2="${W - mr}" y1="${sy(v)}" y2="${sy(v)}" stroke="${css("--grid")}"/>`;
    s += `<text x="${ml - 6}" y="${sy(v) + 4}" text-anchor="end">${fmt(v, 3)}</text>`;
  }
  const xs = o.xint ? Math.max(1, Math.ceil(niceStep(b - a, Math.floor((W - ml - mr) / 34)))) : niceStep(b - a, Math.floor((W - ml - mr) / 44));
  for (let t = Math.ceil(a / xs) * xs; t <= b + 1e-9; t += xs) {
    if (Math.abs(t) < 1e-9) continue;
    s += `<line x1="${sx(t)}" x2="${sx(t)}" y1="${mt}" y2="${H - mb}" stroke="${css("--grid")}"/>`;
    s += `<text x="${sx(t)}" y="${H - 8}" text-anchor="middle">${fmt(t, 3)}</text>`;
  }
  if (a < 0 && b > 0) s += `<line x1="${sx(0)}" x2="${sx(0)}" y1="${mt}" y2="${H - mb}" stroke="${css("--muted")}" stroke-width="1"/>`;
  if (lo <= 0 && hi >= 0) s += `<line x1="${ml}" x2="${W - mr}" y1="${sy(0)}" y2="${sy(0)}" stroke="${css("--muted")}" stroke-width="1"/>`;
  if (o.xlabel) s += `<text x="${W - mr}" y="${sy(Math.max(lo, Math.min(hi, 0))) - 5}" text-anchor="end" style="font-style:italic">${o.xlabel}</text>`;
  (o.vlines || []).forEach((v) => {
    const c = col(v.color || "--muted");
    s += `<line x1="${sx(v.x)}" x2="${sx(v.x)}" y1="${mt - 6}" y2="${H - mb}" stroke="${c}" stroke-dasharray="4 3" stroke-width="1.3"/>`;
    if (v.label) s += `<text x="${sx(v.x) + 4}" y="${mt + 2}" style="fill:${c}">${v.label}</text>`;
  });
  o.series.forEach((q) => {
    const c = col(q.color), op = q.op ?? 1;
    if (q.kind === "line" || q.kind === "area") {
      let d = "", pen = false, seg = [];
      const segs = [];
      q.pts.forEach((p) => { if (!p) { if (seg.length) segs.push(seg); seg = []; } else seg.push(p); });
      if (seg.length) segs.push(seg);
      segs.forEach((sg) => {
        if (q.kind === "area") {
          let pd = `M${sx(sg[0][0])},${sy(0)} ` + sg.map((p) => `L${sx(p[0])},${sy(p[1])}`).join(" ") + ` L${sx(sg[sg.length - 1][0])},${sy(0)} Z`;
          s += `<path d="${pd}" fill="${c}" fill-opacity="${q.fop ?? 0.22}" stroke="none"/>`;
        } else {
          d = sg.map((p, i) => `${i ? "L" : "M"}${sx(p[0]).toFixed(1)},${sy(p[1]).toFixed(1)}`).join(" ");
          s += `<path d="${d}" fill="none" stroke="${c}" stroke-width="${q.w || 2}" stroke-dasharray="${q.dash || ""}" opacity="${op}" stroke-linejoin="round"/>`;
        }
      });
    } else if (q.kind === "stem") {
      q.pts.forEach((p) => {
        if (!p) return; const [n, v] = p; const pop = p[2] ?? op;
        if (Math.abs(v) > 1e-12) s += `<line x1="${sx(n)}" x2="${sx(n)}" y1="${sy(0)}" y2="${sy(v)}" stroke="${c}" stroke-width="${q.w || 1.8}" opacity="${pop}"/>`;
        s += `<circle cx="${sx(n)}" cy="${sy(v)}" r="${q.r || 4}" fill="${q.fill ? c : css("--panel")}" stroke="${c}" stroke-width="1.6" opacity="${pop}"/>`;
        if (q.labels && Math.abs(v) > 1e-12) s += `<text x="${sx(n)}" y="${v >= 0 ? sy(v) - 8 : sy(v) + 16}" text-anchor="middle" style="fill:${c}" opacity="${pop}">${fmt(v, 3)}</text>`;
      });
    }
  });
  (o.dots || []).forEach((d) => {
    const c = col(d.color);
    s += `<circle cx="${sx(d.x)}" cy="${sy(d.y)}" r="5" fill="${c}"/>`;
    if (d.label) s += `<text x="${sx(d.x) + 8}" y="${sy(d.y) - 8}" style="fill:${c};font-weight:500">${d.label}</text>`;
  });
  s += "</svg>"; el.innerHTML = s;
}
function onRedraw(fn) {
  let rt; new ResizeObserver(() => { clearTimeout(rt); rt = setTimeout(fn, 60); }).observe(document.querySelector(".wrap"));
  try { matchMedia("(prefers-color-scheme: dark)").addEventListener("change", fn); } catch (e) {}
  new MutationObserver(fn).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
}
function pressGroup(container, key) { [...container.children].forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.key === key))); }
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600'
         '&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Serif:ital,wght@0,500;1,400&display=swap">')


def page(title, h1, intro, body, script, crumb="Signale &amp; Systeme · Kap. 6", home="../../index.html"):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
{FONTS}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="crumb"><a href="{home}">MEB Interaktiv</a> › {crumb}</div>
    <h1>{h1}</h1>
    <p>{intro}</p>
  </header>
{body}
</div>
<script>{LIB}
{script}
</script>
</body>
</html>
"""
