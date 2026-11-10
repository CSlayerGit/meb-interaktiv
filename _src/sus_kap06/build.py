"""Rebuild the SuS Kap. 6 pages:  python3 _src/sus_kap06/build.py  (run from the repo root)."""
import os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, os.path.dirname(HERE)]          # page scripts + common.py
OUT = os.path.join(ROOT, "sus", "kap06")
for mod, fn in [("p_linearitaet", "linearitaet.html"), ("p_signal_ct", "signalmodelle-ct.html"),
                ("p_signal_dt", "signalmodelle-dt.html"), ("p_superposition", "superposition.html")]:
    open(os.path.join(OUT, fn), "w").write(importlib.import_module(mod).HTML)
print("built", OUT)
