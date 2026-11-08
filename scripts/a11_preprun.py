# -*- coding: utf-8 -*-
"""Prepare ws_run: copy ws_restore tree, patch /home/user ROOT -> ws_run."""
import sys, os, shutil, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SRC = r"C:\Users\Mahboobian\Documents\Default Project\_draft\ws_restore"
DST = r"C:\Users\Mahboobian\Documents\Default Project\_draft\ws_run"
if os.path.exists(DST):
    shutil.rmtree(DST)
# copy everything except results (we will regenerate; legacy kept in ws_restore)
for item in ("src", "data", "paper", "README.md"):
    s = os.path.join(SRC, item)
    d = os.path.join(DST, item)
    if os.path.isdir(s):
        shutil.copytree(s, d)
    else:
        shutil.copy(s, d)
os.makedirs(os.path.join(DST, "results"), exist_ok=True)

n = 0
for root, dirs, files in os.walk(os.path.join(DST, "src")):
    for fn in files:
        if not fn.endswith(".py"):
            continue
        p = os.path.join(root, fn)
        x = open(p, encoding="utf-8", errors="replace").read()
        if 'Path("/home/user")' in x:
            x = x.replace('ROOT = Path("/home/user")', 'ROOT = Path(r"%s")' % DST)
            open(p, "w", encoding="utf-8").write(x)
            n += 1
print("patched files:", n)
import subprocess
print(subprocess.run([sys.executable, "-X", "utf8", "src/run_experiments.py"], capture_output=True, text=True, cwd=DST, timeout=900).stdout[-3000:])
