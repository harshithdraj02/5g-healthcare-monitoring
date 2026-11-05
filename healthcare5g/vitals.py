"""Synthetic patient vitals: baselines, drift, noise, clinical events and motion artefacts."""
import numpy as np
from scipy.signal import lfilter


def make_cohort(seed, P=100, hours=12, event_every_h=3.0):
    rng = np.random.default_rng(seed)
    T = int(hours * 3600)
    hr_base = np.clip(rng.normal(78, 12, P), 52, 104)
    sp_base = np.clip(rng.normal(97, 1.0, P), 94.5, 99.5)

    def ar1(sd, tau, size):
        a = np.exp(-1 / tau)
        e = rng.normal(0, sd * np.sqrt(1 - a * a), size)
        return lfilter([1], [1, -a], e, axis=1)

    hr = hr_base[:, None] + ar1(5.0, 600, (P, T)) + rng.normal(0, 1.8, (P, T))
    sp = sp_base[:, None] + ar1(0.5, 900, (P, T)) + rng.normal(0, 0.5, (P, T))

    truth = np.zeros((P, T), bool)
    events = []  # (patient, start, end, kind)
    for p in range(P):
        n_ev = rng.poisson(hours / event_every_h)
        starts = rng.integers(900, T - 400, n_ev)
        for s in starts:
            dur = int(rng.integers(45, 181))
            if rng.random() < 0.5:
                hr[p, s:s + dur] += rng.uniform(32, 55); kind = "tachycardia"
            else:
                sp[p, s:s + dur] -= rng.uniform(6, 11); kind = "desaturation"
            truth[p, s:s + dur] = True
            events.append((p, int(s), int(s + dur), kind))

    # motion artefacts: short spikes / dropouts that are NOT clinical events
    for p in range(P):
        for _ in range(rng.poisson(hours * 6)):
            s = int(rng.integers(0, T - 5)); d = int(rng.integers(1, 4))
            hr[p, s:s + d] += rng.choice([-1, 1]) * rng.uniform(25, 50)
        for _ in range(rng.poisson(hours * 8)):
            s = int(rng.integers(0, T - 5)); d = int(rng.integers(1, 4))
            sp[p, s:s + d] = rng.uniform(84, 91)
    return hr, np.minimum(sp, 100), events, truth
