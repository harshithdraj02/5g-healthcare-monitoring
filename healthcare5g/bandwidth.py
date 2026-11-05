"""Uplink data per patient per day: cloud-centric vs edge-filtered (Section 8.3)."""
import config as C


def estimate(alerts_per_patient_day):
    b = C.BW
    raw_MB = (b["vitals_per_s"] + b["ecg_per_s"]) * 86400 / 1e6
    edge_MB = (b["summary"] * b["summaries_per_day"] + b["alert_clip"] * alerts_per_patient_day) / 1e6
    return dict(raw_MB=raw_MB, edge_MB=edge_MB, reduction_pct=(1 - edge_MB / raw_MB) * 100,
                alerts_per_patient_day=alerts_per_patient_day)
