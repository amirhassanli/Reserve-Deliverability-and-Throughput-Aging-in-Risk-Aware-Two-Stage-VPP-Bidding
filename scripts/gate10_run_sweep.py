# -*- coding: utf-8 -*-
"""Gate-10 reserve-price sweep + risk-neutral P1 (repaired_final engine, K=100)."""
import sys, os, json, time, copy
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\Mahboobian\Documents\Default Project\_draft\gate10_run"
sys.path.insert(0, BASE)

runner_path = os.path.join(BASE, "RUN_GATE10_REAL_OOS_ARTICLE_READY_FIXED.py")
ns = {"__file__": runner_path, "__name__": "runner"}
code = open(runner_path, encoding="utf-8").read()
code = code.split("# 8. Run models")[0]
exec(compile(code, runner_path, "exec"), ns)
BASEdf = ns["BASE"]
CONFIG = ns["CONFIG"]
SCENARIO_FILES = ns["SCENARIO_FILES"]
load_scenario = ns["load_scenario"]
scen100 = load_scenario(SCENARIO_FILES[100], 100)
print("BASE", BASEdf.shape, "scen", scen100.scenario_id.nunique())

import pandas as pd, numpy as np
# replace global BASE name used downstream
BASE = BASEdf

import importlib.util
spec = importlib.util.spec_from_file_location("eng", os.path.join(r"C:\Users\Mahboobian\Desktop\Aericle 4\arena\VPP_IEEE_Gate10", "gate10f1_repaired_final.py"))
eng = importlib.util.module_from_spec(spec); sys.modules["eng"]=eng; spec.loader.exec_module(eng)

RP0 = 5.0
levels = [0.0, 1.25, 2.5, 3.75, 5.0, 6.25, 7.5]
rows = []
for rp in levels:
    for model, lam in (("B2", 0.0), ("P1", 0.02)):
        cfg = json.loads(json.dumps(CONFIG))
        cfg["market"]["reserve_price_eur_per_mw"] = float(rp)
        cfg["risk"]["risk_lambda"] = lam
        t0 = time.time()
        res = eng.solve(cfg, BASE, scen100, risk_lambda=lam)
        dec = res.get("decisions", {})
        res_mean = float(np.mean(dec["RES"])) if dec.get("RES") else float("nan")
        rows.append(dict(
            reserve_price_eur_per_mw=rp,
            pct_of_proxy=round(100*rp/RP0, 1),
            model=model, lambda_risk=lam, K=100,
            expected_profit=res["expected_profit"],
            cvar95=res["cvar95"],
            risk_adjusted=res["risk_adjusted_objective"],
            worst_case=res["worst_case_profit"],
            best_case=res["best_case_profit"],
            runtime_s=res["runtime_seconds"],
            status=res["status"],
            mean_RES_mw=res_mean,
            reserve_revenue_eur=res_mean*24*rp,
        ))
        print(f"rp={rp:5.2f} ({100*rp/RP0:5.0f}%) {model}: exp={res['expected_profit']:12.2f} cvar={res['cvar95']:12.2f} riskadj={res['risk_adjusted_objective']:12.2f} meanRES={res_mean:.3f}MW rev={res_mean*24*rp:9.2f} ({time.time()-t0:.1f}s)")
df = pd.DataFrame(rows)
out = r"C:\Users\Mahboobian\Documents\Default Project\_draft\sweep_reserve_price_K100.csv"
df.to_csv(out, index=False)
print("\nSAVED", out)
print(df[["reserve_price_eur_per_mw","pct_of_proxy","model","expected_profit","risk_adjusted","mean_RES_mw","reserve_revenue_eur"]].to_string(index=False))

print("\n--- Risk-neutral P1 (lambda=0) at proxy reserve price 5 ---")
cfg = json.loads(json.dumps(CONFIG))
cfg["market"]["reserve_price_eur_per_mw"] = 5.0
cfg["risk"]["risk_lambda"] = 0.0
res = eng.solve(cfg, BASE, scen100, risk_lambda=0.0)
print(f"P1 lambda=0: exp={res['expected_profit']:.2f} cvar={res['cvar95']:.2f} riskadj={res['risk_adjusted_objective']:.2f} worst={res['worst_case_profit']:.2f}")
b2 = [r for r in rows if r["reserve_price_eur_per_mw"]==5.0 and r["model"]=="B2"][0]
print(f"B2 lambda=0: exp={b2['expected_profit']:.2f} (reference)")
print(f"P1-B2 at lambda=0: {res['expected_profit']-b2['expected_profit']:.2f}")
rn = pd.DataFrame([{"model":"P1","lambda_risk":0.0,"reserve_price":5.0,"K":100,
                    "expected_profit":res["expected_profit"],"cvar95":res["cvar95"],
                    "risk_adjusted":res["risk_adjusted_objective"],
                    "worst_case":res["worst_case_profit"],"best_case":res["best_case_profit"],
                    "runtime_s":res["runtime_seconds"]}])
rn.to_csv(r"C:\Users\Mahboobian\Documents\Default Project\_draft\p1_riskneutral_K100.csv", index=False)
print("SAVED p1_riskneutral_K100.csv")
