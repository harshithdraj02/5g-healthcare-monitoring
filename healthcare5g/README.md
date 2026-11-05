# 5G-Enabled Intelligent Healthcare Monitoring: implementation

Everything claimed in the report and slides is implemented here and runs on a normal laptop (Python 3.9+).

## Run
```
pip install -r requirements.txt
python run_all.py              # Tables 4-6 + Figures 1-4  -> results/
python pipeline.py --arch C    # live end-to-end pipeline  -> results/dashboard_C.html   (try --arch A and B)
python check.py                # self-checks
```

## Where each claim lives
| Claim in report / slides | File |
|---|---|
| Synthetic vitals, clinical events, motion artefacts (4.1) | `vitals.py` |
| Fixed-threshold alarm vs adaptive per-patient detector, 8-of-10 persistence (5.2, 5.3, Table 4) | `detectors.py` |
| Same detector running sample-by-sample at the edge | `detectors.StreamingAdaptive` (`check.py` proves it matches the batch version) |
| 4G+Cloud, 5G eMBB+Cloud, 5G URLLC slice+MEC; queue, priority slice, loss, transport, processing (4.2, Tables 3 and 5) | `network.py`, `config.py` |
| Uplink data cloud-centric vs edge-filtered (8.3, Table 6) | `bandwidth.py` |
| Architecture of Figure 1: wearable, gateway/UE, network, edge pre-processing, detector, alert manager (priority, de-dup), clinician dashboard | `pipeline.py` |
| Figures 1-4 | `plots.py` |
| All parameters (Tables 2 and 3) | `config.py` |

## What is real and what is modelled (say this in the viva)
- Real code: the vitals generator, both detectors, the queueing simulation, the alert manager, the edge summaries and the dashboard all execute.
- Modelled: the 5G network itself. Radio, transport and processing delays are assumed values in `config.py`, not measurements from a live 5G network. Vitals are synthetic.
- Not implemented: a real 5G core/RAN, real patient data, security and clinical validation (listed as limitations and future scope).
