"""Rebuild the FT1 Modul 1 pages:  python3 _src/ft1_modul1/build.py  (run from the repo root)."""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, os.path.dirname(HERE)]          # page scripts + common.py
OUT = os.path.join(ROOT, "ft1", "modul1")
os.makedirs(OUT, exist_ok=True)
for mod, fn in [("p_kostenvergleich", "kostenvergleich.html")]:
    open(os.path.join(OUT, fn), "w").write(importlib.import_module(mod).HTML)
print("built", OUT)
