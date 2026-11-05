"""Latency model: discrete queue at the shared radio resource + fixed/random delay components (Section 4.2)."""
import numpy as np
import config as C


def queue_delays(a_med, a_bg, mu, prio, rng):
    nm, nb = len(a_med), len(a_bg)
    if not prio:   # FIFO: medical and background packets share one queue
        a = np.concatenate([a_med, a_bg]); lab = np.concatenate([np.ones(nm, bool), np.zeros(nb, bool)])
        o = np.argsort(a, kind="stable"); a = a[o].tolist(); lab = lab[o]
        svc = rng.exponential(1 / mu, len(a)).tolist()
        fin, d = 0.0, np.empty(len(a))
        for i in range(len(a)):
            s = a[i] if a[i] > fin else fin
            fin = s + svc[i]; d[i] = fin - a[i]
        return d[lab]
    # non-preemptive priority: medical packets are served before waiting background packets
    med, bg = a_med.tolist(), a_bg.tolist()
    svm = rng.exponential(1 / mu, nm).tolist(); svb = rng.exponential(1 / mu, nb).tolist()
    im = ib = 0; t = 0.0; d = np.empty(nm)
    while im < nm:
        if med[im] <= t:
            t += svm[im]; d[im] = t - med[im]; im += 1
        elif ib < nb and bg[ib] <= t:
            t += svb[ib]; ib += 1
        else:
            nxt = med[im]
            if ib < nb and bg[ib] < nxt:
                nxt = bg[ib]
            t = nxt
    return d


def packet_latencies(key, a_med, lam_bg, T, rng):
    """End-to-end latency (ms) for each medical packet in a_med (sorted arrival times, seconds)."""
    cfg = C.ARCH[key]
    nb = rng.poisson(lam_bg * T); a_bg = np.sort(rng.uniform(0, T, nb))
    q = queue_delays(a_med, a_bg, cfg["mu"], cfg["prio"], rng) * 1000.0
    n = len(q)
    transport = cfg["tr_med"] * rng.lognormal(0, cfg["tr_sig"], n)
    proc = cfg["proc"][0] + rng.exponential(cfg["proc"][1], n)
    lost = rng.random(n) < cfg["loss"]
    return q + cfg["radio"] + transport + proc + cfg["dl"] + lost * cfg["retx"]


def run_arch(key, n_patients, lam_bg, T=None, seed=7):
    T = T or C.T_LAT
    rng = np.random.default_rng(seed + ord(key) * 13)
    off = rng.uniform(0, 1, n_patients)
    a_med = np.sort(np.concatenate([off + k + rng.normal(0, 0.01, n_patients) for k in range(T)]))
    a_med = a_med[(a_med >= 0) & (a_med < T)]
    return packet_latencies(key, a_med, lam_bg, T, rng)


def summarise(x):
    return dict(mean=float(x.mean()), p95=float(np.percentile(x, 95)), p99=float(np.percentile(x, 99)),
                miss100=float((x > 100).mean() * 100), miss20=float((x > 20).mean() * 100))
