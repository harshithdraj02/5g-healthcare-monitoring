"""Figures 1-4 of the report."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import config as C

NAVY, ORANGE, RED, GREEN, GREY = "#1f2a7a", "#f28c1b", "#c0392b", "#2e8b57", "#6b6b6b"
plt.rcParams.update({"font.family": "serif", "font.size": 9})


def fig_architecture(path):
    def box(ax, x, y, w, h, text, fc, ec):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.04", fc=fc, ec=ec, lw=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=7.5)

    def arrow(ax, x1, y1, x2, y2, c=NAVY):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="-|>", color=c, lw=1.2))

    fig, ax = plt.subplots(figsize=(7.4, 3.3)); ax.set_xlim(0, 10); ax.set_ylim(0, 4.4); ax.axis("off")
    ax.text(0.1, 4.15, "Patient and 5G network layer", color=NAVY, fontsize=8, weight="bold")
    ax.text(0.1, 1.95, "Edge AI and clinical layer", color=ORANGE, fontsize=8, weight="bold")
    LB, LE, OB, OE = "#e8eaf6", NAVY, "#fff1e0", ORANGE
    box(ax, 0.1, 2.9, 2.0, 1.0, "Wearable sensors\n(ECG, SpO\u2082, HR, temp)", LB, LE)
    box(ax, 2.6, 2.9, 2.0, 1.0, "Patient gateway\n(phone / hub, 5G UE)", LB, LE)
    box(ax, 5.1, 2.9, 2.2, 1.0, "5G gNB\nURLLC slice | eMBB slice", LB, LE)
    box(ax, 7.8, 2.9, 2.1, 1.0, "UPF + MEC host\n(hospital edge)", LB, LE)
    for x1, x2 in ((2.1, 2.6), (4.6, 5.1), (7.3, 7.8)):
        arrow(ax, x1, 3.4, x2, 3.4)
    box(ax, 7.8, 0.35, 2.1, 1.0, "Edge pre-processing\nfilter, features", OB, OE)
    box(ax, 5.2, 0.35, 2.1, 1.0, "Adaptive anomaly\ndetector", OB, OE)
    box(ax, 2.6, 0.35, 2.1, 1.0, "Alert manager\n(priority, dedup)", OB, OE)
    box(ax, 0.1, 0.35, 2.1, 1.0, "Clinician dashboard\n+ cloud EHR", OB, OE)
    arrow(ax, 8.85, 2.9, 8.85, 1.35)
    for x1, x2 in ((7.8, 7.3), (5.2, 4.7), (2.6, 2.2)):
        arrow(ax, x1, 0.85, x2, 0.85, ORANGE)
    ax.text(8.95, 2.1, "vitals", fontsize=7, color=NAVY)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def fig_detection(path, hr, fixed, adaptive, events):
    cands = [e for e in events if e[3] == "tachycardia" and e[1] > 1500]
    p0, s0, e0, _ = cands[0]
    lo, hi = s0 - 240, e0 + 240
    tt = np.arange(lo, hi) / 60.0
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.plot(tt, hr[p0, lo:hi], color=NAVY, lw=0.9, label="Heart rate (bpm)")
    ax.axhline(100, color=GREY, ls="--", lw=0.8, label="Fixed limit (100 bpm)")
    ax.axvspan(s0 / 60, e0 / 60, color=ORANGE, alpha=0.18, label="True clinical event")
    fa = np.flatnonzero(fixed[p0, lo:hi]) + lo; ad = np.flatnonzero(adaptive[p0, lo:hi]) + lo
    ax.scatter(fa / 60.0, np.full(fa.size, 38), s=5, color=RED, label="Fixed-threshold alarm")
    ax.scatter(ad / 60.0, np.full(ad.size, 33), s=5, color=GREEN, label="Adaptive alarm")
    ax.set_xlabel("Time (minutes since admission)"); ax.set_ylabel("Heart rate (bpm)")
    ax.set_ylim(28, 152); ax.grid(alpha=0.25); ax.legend(ncol=3, fontsize=7, loc="upper left", frameon=False)
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def fig_cdf(path, raw):
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for k, c in (("A", RED), ("B", ORANGE), ("C", NAVY)):
        x = np.sort(raw[k]); y = np.arange(1, len(x) + 1) / len(x)
        ax.plot(x, y, color=c, lw=1.4, label=C.ARCH[k]["name"])
    ax.axvline(100, color=GREY, ls="--", lw=0.8); ax.text(101, 0.05, "100 ms target", fontsize=7, color=GREY)
    ax.set_xscale("log"); ax.set_xlim(3, 500)
    ax.set_xlabel("End-to-end alert latency (ms, log scale)"); ax.set_ylabel("Cumulative probability")
    ax.grid(alpha=0.25, which="both"); ax.legend(frameon=False, fontsize=8, loc="lower right", bbox_to_anchor=(1.0, 0.08))
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)


def fig_p99(path, lat_busy):
    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for k, c, m in (("A", RED, "o"), ("B", ORANGE, "s"), ("C", NAVY, "^")):
        ax.plot(C.NS, [lat_busy[k][str(N)]["p99"] for N in C.NS], color=c, marker=m, ms=4, lw=1.3, label=C.ARCH[k]["name"])
    ax.axhline(100, color=GREY, ls="--", lw=0.8)
    ax.set_xlabel("Monitored patients in the cell"); ax.set_ylabel("99th-percentile latency (ms)")
    ax.grid(alpha=0.25); ax.legend(frameon=False, fontsize=8, loc="center", bbox_to_anchor=(0.5, 0.36))
    fig.tight_layout(); fig.savefig(path, dpi=200); plt.close(fig)
