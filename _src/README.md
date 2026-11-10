# Sources

- `common.py`: shared page shell (CSS tokens for light/dark, IBM Plex fonts, `plot()` SVG helper for lines, stems, areas and windows, `sample()`, `onRedraw()`). Import it and call `page(title, h1, intro, body_html, script_js, crumb=…)`.
- `<subject>_<chapter>/`: one `p_*.py` per page plus `build.py`. Run `python3 _src/<subject>_<chapter>/build.py` from the repo root.
- Hand-written pages (e.g. `sus/kap06/faltung.html`) are edited directly.

Every page is a single self-contained HTML file. External scripts only from cdnjs / jsdelivr / unpkg with pinned versions.
