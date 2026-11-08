# -*- coding: utf-8 -*-
import sys, subprocess, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
DST = r"C:\Users\Mahboobian\Documents\Default Project\_draft\gate10_run"
t0 = time.time()
r = subprocess.run([sys.executable, "RUN_GATE10_REAL_OOS_ARTICLE_READY_FIXED.py"],
                   capture_output=True, text=True, cwd=DST, timeout=1800)
print("rc:", r.returncode, "elapsed", round(time.time()-t0,1))
print(r.stdout[-4000:])
print("STDERR:", r.stderr[-2000:])
