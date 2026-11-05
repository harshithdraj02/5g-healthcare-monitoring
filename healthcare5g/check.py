"""Self-checks: python check.py"""
import numpy as np, json, os
import config as C
from vitals import make_cohort
from detectors import detect_adaptive, StreamingAdaptive

hr, sp, ev, _ = make_cohort(5, 4, 1, event_every_h=0.5)
batch = detect_adaptive(hr, sp)
for p in range(4):
    dh, ds = StreamingAdaptive(hr[p, 0], "hr"), StreamingAdaptive(sp[p, 0], "spo2")
    live = np.array([dh.update(hr[p, t]) | ds.update(sp[p, t]) for t in range(hr.shape[1])])
    assert (live == batch[p]).all(), f"streaming and batch detectors differ for patient {p}"
print("OK  streaming detector == batch detector")

res = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "results.json")))
A, F = res["detection"]["adaptive"], res["detection"]["fixed"]
assert A["false_alarms"] == 0 and F["fa_per_patient_day"] > 100 and A["recall"] > 0.9
lc, la, lb = (res["latency"]["busy"][k]["400"] for k in "CAB")
assert lc["p99"] < lb["p99"] < la["p99"] and lc["miss100"] == 0 and la["miss100"] > 1
print("OK  results.json shows the claims in the report and slides")
