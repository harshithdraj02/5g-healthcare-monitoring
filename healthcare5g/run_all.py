"""Reproduces every table and figure in the report: Tables 4-6 and Figures 1-4.
Usage:  python run_all.py            (outputs go to ./results)"""
import json, os, time
import config as C
from vitals import make_cohort
from detectors import detect_fixed, detect_adaptive, evaluate
from network import run_arch, summarise
from bandwidth import estimate
import plots

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
t0 = time.time(); R = {}

# ---- Part 1: detection (Table 4, Figure 2) ----
hr, sp, events, truth = make_cohort(C.SEED_COHORT, C.PATIENTS, C.HOURS)
fixed, adaptive = detect_fixed(hr, sp), detect_adaptive(hr, sp)
R["detection"] = dict(fixed=evaluate(fixed, events, C.HOURS), adaptive=evaluate(adaptive, events, C.HOURS),
                      patients=C.PATIENTS, hours=C.HOURS)
R["alerts_per_patient_day_adaptive"] = R["detection"]["adaptive"]["alarms"] / (C.PATIENTS * C.HOURS / 24)
plots.fig_detection(f"{OUT}/fig2_detection.png", hr, fixed, adaptive, events)

# ---- Part 2: latency (Table 5, Figures 3-4) ----
lat, raw_main = {"busy": {}, "off": {}}, {}
for scen, lam in (("busy", C.LAM_BUSY), ("off", C.LAM_OFF)):
    for k in C.ARCH:
        lat[scen][k] = {}
        for N in C.NS:
            x = run_arch(k, N, lam)
            lat[scen][k][str(N)] = summarise(x)
            if scen == "busy" and N == 400:
                raw_main[k] = x
R["latency"] = lat; R["arch"] = {k: v["name"] for k, v in C.ARCH.items()}
plots.fig_cdf(f"{OUT}/fig3_cdf.png", raw_main); plots.fig_p99(f"{OUT}/fig4_p99.png", lat["busy"])

# ---- Part 3: uplink data (Table 6) and Figure 1 ----
R["bandwidth"] = estimate(R["alerts_per_patient_day_adaptive"])
plots.fig_architecture(f"{OUT}/fig1_architecture.png")
json.dump(R, open(f"{OUT}/results.json", "w"), indent=2)

# ---- Console summary (matches the report tables) ----
F, A = R["detection"]["fixed"], R["detection"]["adaptive"]
print("\nTable 4  Detection ({} patients x {} h, {} events)".format(C.PATIENTS, C.HOURS, F["events"]))
for n, d in (("Fixed threshold", F), ("Adaptive", A)):
    print(f"  {n:16s} detected {d['detected']}/{d['events']}  recall {d['recall']*100:.1f}%  alarms {d['alarms']}  "
          f"false {d['false_alarms']}  FA/patient-day {d['fa_per_patient_day']:.1f}  delay {d['mean_delay_s']:.1f}s")
print("\nTable 5  Latency, 400 patients, busy hour")
for k in C.ARCH:
    x = lat["busy"][k]["400"]
    print(f"  {C.ARCH[k]['name']:22s} mean {x['mean']:.1f}  p95 {x['p95']:.1f}  p99 {x['p99']:.1f} ms   >100ms {x['miss100']:.2f}%   >20ms {x['miss20']:.2f}%")
b = R["bandwidth"]
print(f"\nTable 6  Uplink per patient-day: cloud {b['raw_MB']:.1f} MB, edge {b['edge_MB']:.2f} MB  (-{b['reduction_pct']:.1f}%)")
print(f"\nDone in {time.time()-t0:.0f} s. Files in {OUT}")
