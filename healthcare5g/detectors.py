"""Fixed-threshold alarm, adaptive per-patient detector (batch + streaming), and evaluation."""
from collections import deque
import numpy as np
from scipy.signal import lfilter
import config as C


def ewma(x, alpha, x0):
    return lfilter([alpha], [1, -(1 - alpha)], x, axis=1, zi=((1 - alpha) * x0)[:, None])[0]


def rolling_sum(b, n):
    return lfilter(np.ones(n), [1], b.astype(float), axis=1)


def detect_fixed(hr, sp):
    f = C.FIXED
    return (hr > f["hr_hi"]) | (hr < f["hr_lo"]) | (sp < f["spo2_lo"])


def detect_adaptive(hr, sp, alpha=None, persist=None, zthr=None):
    alpha = alpha or C.ADAPTIVE["alpha"]; persist = persist or C.ADAPTIVE["persist"]; zthr = zthr or C.ADAPTIVE["zthr"]
    out = np.zeros(hr.shape, bool)
    for x, sign in ((hr, 0), (sp, -1)):
        mu = ewma(x, alpha, x[:, 0])
        mu_prev = np.concatenate([mu[:, :1], mu[:, :-1]], axis=1)   # baseline BEFORE this sample
        dev = x - mu_prev
        sd = np.maximum(np.sqrt(ewma(dev ** 2, alpha, np.full(x.shape[0], 4.0))), 0.4)
        z = dev / sd
        flag = (np.abs(z) > zthr) if sign == 0 else (z < -zthr)
        out |= rolling_sum(flag, persist[1]) >= persist[0]
    return out


class StreamingAdaptive:
    """Sample-by-sample version of detect_adaptive for ONE signal of ONE patient (used by the live pipeline)."""
    def __init__(self, first_value, signal="hr"):
        self.a = C.ADAPTIVE["alpha"]; self.k, self.n = C.ADAPTIVE["persist"]; self.z = C.ADAPTIVE["zthr"]
        self.mu, self.var, self.sig = float(first_value), 4.0, signal
        self.win = deque(maxlen=self.n)

    def update(self, x):
        dev = x - self.mu
        self.var = self.a * dev * dev + (1 - self.a) * self.var
        sd = max(self.var ** 0.5, 0.4)
        z = dev / sd
        self.mu += self.a * dev
        flag = abs(z) > self.z if self.sig == "hr" else z < -self.z
        self.win.append(flag)
        return sum(self.win) >= self.k          # True while the alarm condition holds


def episodes(flag_row, merge_gap=30):
    idx = np.flatnonzero(flag_row)
    if idx.size == 0:
        return []
    eps, s, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > merge_gap:
            eps.append((s, prev)); s = i
        prev = i
    eps.append((s, prev))
    return eps


def evaluate(alarm, events, hours, warm=600):
    P = alarm.shape[0]
    alarm = alarm.copy(); alarm[:, :warm] = False
    by_p = {p: [] for p in range(P)}
    for e in events:
        by_p[e[0]].append(e)
    detected, delays, false_alarms, total, missed = 0, [], 0, 0, []
    for p in range(P):
        for x in by_p[p]:
            s, e = x[1], x[2]
            seg = np.flatnonzero(alarm[p, s:e + 10])
            if seg.size:
                detected += 1; delays.append(seg[0])
            else:
                missed.append(x[3])
        for a, b in episodes(alarm[p]):
            total += 1
            if not any((a <= x[2] + 10) and (b >= x[1] - 5) for x in by_p[p]):
                false_alarms += 1
    n = len(events)
    return dict(events=n, detected=detected, recall=detected / n, alarms=total, false_alarms=false_alarms,
                precision=(total - false_alarms) / max(total, 1), fa_per_patient_day=false_alarms / (P * hours / 24),
                missed_tachy=missed.count("tachycardia"), missed_desat=missed.count("desaturation"),
                mean_delay_s=float(np.mean(delays)), median_delay_s=float(np.median(delays)))
