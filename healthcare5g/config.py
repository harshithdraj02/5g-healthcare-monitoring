"""All parameters used in the report (Tables 2 and 3). Change them here and re-run."""
SEED_COHORT = 2026
PATIENTS, HOURS = 100, 12

# Fixed-threshold baseline alarm
FIXED = dict(hr_hi=100, hr_lo=50, spo2_lo=92)

# Adaptive detector: EWMA memory ~30 min, |z| > 4, persistence 8 of last 10 samples
ADAPTIVE = dict(alpha=1 / 1800, persist=(8, 10), zthr=4.0)

WARMUP_S = 600                          # learning period before alerts are trusted (first 10 minutes)

# Latency study
LAM_BUSY, LAM_OFF = 1500, 300          # background traffic, packet-units per second
NS = [50, 100, 200, 300, 400]          # monitored patients per cell
T_LAT = 300                            # simulated seconds per run
DEADLINES_MS = (100, 20)

# Table 3: three architectures (all delays in ms; capacities in packet-units/s)
ARCH = {
    "A": dict(name="4G + Cloud",           mu=2000, prio=False, radio=10.0, tr_med=30.0, tr_sig=0.35, proc=(5.0, 8.0), dl=10.0, loss=0.010,   retx=20.0),
    "B": dict(name="5G eMBB + Cloud",      mu=8000, prio=False, radio=5.0,  tr_med=22.0, tr_sig=0.30, proc=(5.0, 8.0), dl=5.0,  loss=0.005,   retx=10.0),
    "C": dict(name="5G URLLC slice + MEC", mu=8000, prio=True,  radio=1.5,  tr_med=2.0,  tr_sig=0.20, proc=(3.0, 2.0), dl=1.5,  loss=0.00001, retx=2.0),
}

# Uplink data-volume assumptions (bytes)
BW = dict(vitals_per_s=64, ecg_per_s=250 * 2 + 60, summary=100, alert_clip=30 * 250 * 2 + 200, summaries_per_day=1440)
