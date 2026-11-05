"""Live end-to-end pipeline for the architecture in Figure 1:
Wearable -> Gateway (5G UE) -> Network (slice / queue model) -> Edge (pre-processing + adaptive detector)
-> Alert manager (priority + de-duplication) -> Clinician dashboard (HTML).

Usage:  python pipeline.py --arch C            # try A, B or C
Time is simulated (one tick = 1 s of patient time), so a 1-hour ward runs in a few seconds."""
import argparse, html, os
import numpy as np
import config as C
from vitals import make_cohort
from detectors import StreamingAdaptive
from network import packet_latencies


class Wearable:                       # sensor: yields (hr, spo2) once per second
    def __init__(self, hr, sp): self.hr, self.sp = hr, sp
    def read(self, t): return float(self.hr[t]), float(self.sp[t])


class Gateway:                        # patient hub / phone acting as the 5G UE: adds timestamp, sends 1 packet per second
    def __init__(self, pid, offset): self.pid, self.offset = pid, offset
    def packet(self, t, hr, sp): return dict(pid=self.pid, t=t, send=t + self.offset, hr=hr, sp=sp)


class EdgeNode:                       # MEC host: summaries + adaptive detector per patient and signal
    def __init__(self): self.det, self.state, self.sums, self.bytes_out = {}, {}, {}, 0
    def process(self, pkt):
        pid, t = pkt["pid"], pkt["t"]
        if pid not in self.det:
            self.det[pid] = (StreamingAdaptive(pkt["hr"], "hr"), StreamingAdaptive(pkt["sp"], "spo2"))
            self.state[pid] = [False, False]; self.sums[pid] = []
        self.sums[pid].append((pkt["hr"], pkt["sp"]))
        if t % 60 == 59:                              # edge pre-processing: forward only a 1-minute summary
            self.bytes_out += C.BW["summary"]; self.sums[pid].clear()
        fired = []
        for i, (d, name) in enumerate(zip(self.det[pid], ("heart rate", "SpO2"))):
            on = d.update(pkt["hr"] if i == 0 else pkt["sp"])
            if on and not self.state[pid][i]:         # rising edge of the alarm condition
                fired.append(name)
            self.state[pid][i] = on
        return fired


class AlertManager:                   # priority + de-duplication (60 s cool-down per patient and signal)
    def __init__(self, cooldown=60): self.last, self.alerts, self.cool = {}, [], cooldown
    def raise_alert(self, pid, signal, t, value, deliver_t, latency_ms):
        if t - self.last.get((pid, signal), -10**9) < self.cool:
            return None
        self.last[(pid, signal)] = t
        critical = (signal == "SpO2" and value < 90) or (signal == "heart rate" and value > 120)
        a = dict(pid=pid, signal=signal, t=t, value=value, priority="CRITICAL" if critical else "WARNING",
                 deliver=deliver_t, latency_ms=latency_ms)
        self.alerts.append(a); return a


def run(arch="C", patients=6, minutes=60, bg=None, seed=11):
    bg = C.LAM_BUSY if bg is None else bg
    T = minutes * 60
    hr, sp, events, _ = make_cohort(seed, patients, minutes / 60, event_every_h=0.5)
    rng = np.random.default_rng(seed)
    offs = rng.uniform(0, 1, patients)
    gws = [Gateway(p, offs[p]) for p in range(patients)]
    wear = [Wearable(hr[p], sp[p]) for p in range(patients)]
    pk = [gws[p].packet(t, *wear[p].read(t)) for t in range(T) for p in range(patients)]
    arr = np.array([x["send"] for x in pk]); order = np.argsort(arr, kind="stable")
    lat = np.empty(len(pk)); lat[order] = packet_latencies(arch, arr[order], bg, T + 2, rng)  # network model
    edge, mgr = EdgeNode(), AlertManager()
    for i, x in enumerate(pk):
        for sig in edge.process(x):
            if x["t"] < C.WARMUP_S:        # learning period: personal baselines are still settling
                continue
            mgr.raise_alert(x["pid"], sig, x["t"], x["hr"] if sig == "heart rate" else x["sp"], x["t"] + lat[i] / 1000, lat[i])
    # ground truth check
    rows = []
    for a in mgr.alerts:
        ev = [e for e in events if e[0] == a["pid"] and e[1] <= a["t"] <= e[2] + 10]
        a["real"] = bool(ev); a["delay_s"] = a["t"] - ev[0][1] if ev else None
    raw = (C.BW["vitals_per_s"] + C.BW["ecg_per_s"]) * T * patients
    # cloud architectures (A, B) stream everything; the edge architecture (C) forwards only summaries + alert clips
    sent = edge.bytes_out + C.BW["alert_clip"] * len(mgr.alerts) if C.ARCH[arch]["prio"] else raw
    return dict(arch=arch, patients=patients, minutes=minutes, events=events, alerts=mgr.alerts, lat=lat,
                raw_bytes=raw, edge_bytes=sent, hr=hr, sp=sp)


def dashboard(res, path):
    name = C.ARCH[res["arch"]]["name"]; al = res["alerts"]
    css = "body{font-family:Calibri,Arial;margin:24px;background:#f4f7fb;color:#1e293b}h1{color:#0b1b3f}table{border-collapse:collapse;background:#fff}" \
          "td,th{border:1px solid #cbd5e1;padding:6px 10px;font-size:13px}th{background:#dce3f4}.CRITICAL{color:#e11d48;font-weight:bold}.WARNING{color:#b45309}" \
          ".card{display:inline-block;background:#fff;border:1px solid #e2e8f0;border-radius:8px;padding:10px 16px;margin:0 10px 12px 0}.big{font-size:22px;font-weight:bold}"
    rows = "".join(f"<tr><td>{a['t']//60:02d}:{a['t']%60:02d}</td><td>Patient {a['pid']+1}</td><td>{a['signal']}</td><td>{a['value']:.0f}</td>"
                   f"<td class='{a['priority']}'>{a['priority']}</td><td>{a['latency_ms']:.1f}</td><td>{'yes' if a['real'] else 'no'}</td></tr>" for a in sorted(al, key=lambda a: a["t"]))
    svgs = ""
    for p in range(res["patients"]):
        h = res["hr"][p]; T = len(h); w, ht = 560, 70
        pts = " ".join(f"{i*w/T:.1f},{ht-(v-40)*ht/110:.1f}" for i, v in enumerate(h[::10]) for i in [i * 10])
        marks = "".join(f"<line x1='{a['t']*w/T:.1f}' x2='{a['t']*w/T:.1f}' y1='0' y2='{ht}' stroke='#e11d48' stroke-width='2'/>" for a in al if a["pid"] == p)
        shade = "".join(f"<rect x='{e[1]*w/T:.1f}' width='{(e[2]-e[1])*w/T:.1f}' y='0' height='{ht}' fill='#f59e0b' opacity='0.2'/>" for e in res["events"] if e[0] == p)
        svgs += f"<div><b>Patient {p+1}</b> heart rate (shaded = true event, red line = alert)<br><svg width='{w}' height='{ht}' style='background:#fff;border:1px solid #e2e8f0'>{shade}<polyline points='{pts}' fill='none' stroke='#1f2a7a' stroke-width='1'/>{marks}</svg></div>"
    real = sum(a["real"] for a in al); L = res["lat"]
    cards = "".join(f"<div class='card'><div class='big'>{v}</div>{k}</div>" for k, v in (
        ("alerts raised", len(al)), ("real events caught", f"{real}"), ("false alerts", len(al) - real),
        ("mean packet latency (ms)", f"{L.mean():.1f}"), ("p99 latency (ms)", f"{np.percentile(L,99):.1f}"),
        ("data kept off the cloud link", f"{100*(1-res['edge_bytes']/res['raw_bytes']):.1f}%")))
    open(path, "w").write(f"<html><head><meta charset='utf-8'><title>Clinician dashboard</title><style>{css}</style></head><body>"
                          f"<h1>Clinician dashboard: {html.escape(name)}</h1>{cards}<h3>Alerts</h3>"
                          f"<table><tr><th>Time</th><th>Patient</th><th>Signal</th><th>Value</th><th>Priority</th><th>Latency (ms)</th><th>Real event?</th></tr>{rows}</table>"
                          f"<h3>Traces</h3>{svgs}</body></html>")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--arch", default="C", choices=list(C.ARCH))
    ap.add_argument("--patients", type=int, default=6); ap.add_argument("--minutes", type=int, default=60)
    a = ap.parse_args()
    res = run(a.arch, a.patients, a.minutes)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); os.makedirs(out, exist_ok=True)
    path = f"{out}/dashboard_{a.arch}.html"; dashboard(res, path)
    real = sum(x["real"] for x in res["alerts"])
    print(f"{C.ARCH[a.arch]['name']}: {len(res['alerts'])} alerts ({real} real, {len(res['alerts'])-real} false) for "
          f"{len(res['events'])} true events; mean latency {res['lat'].mean():.1f} ms, p99 {np.percentile(res['lat'],99):.1f} ms; "
          f"data sent to cloud {100*res['edge_bytes']/res['raw_bytes']:.2f}% of raw")
    print("Dashboard:", path)
