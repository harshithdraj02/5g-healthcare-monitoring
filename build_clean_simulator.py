import os, base64

def get_base64_img(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", filename)
    if not os.path.exists(path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "healthcare5g", "results", filename)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

fig1_b64 = get_base64_img("fig1_architecture.png")
fig2_b64 = get_base64_img("fig2_detection.png")
fig3_b64 = get_base64_img("fig3_cdf.png")
fig4_b64 = get_base64_img("fig4_p99.png")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>5G Intelligent Healthcare Monitoring | Interactive Clinical & Telemetry Simulator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* =========================================================================
       CLEAN, MODERN CLINICAL WORKSTATION THEME
       Professional, high-contrast, uncluttered, no neon glow slop.
       ========================================================================= */
    :root {{
      --bg-base: #0a0f1d;
      --bg-surface: #111a2e;
      --bg-surface-elevated: #16223b;
      --border-color: #202f4d;
      --border-subtle: #17243c;
      --border-focus: #38bdf8;
      --primary: #0284c7;
      --primary-light: #38bdf8;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --ecg-green: #10b981;
      --spo2-cyan: #06b6d4;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      font-size: 13px;
      line-height: 1.5;
    }}

    /* =========================================================================
       CLEAN TOP NAVIGATION BAR (NO PERSONAL / MENTOR DETAILS)
       ========================================================================= */
    header {{
      background: var(--bg-surface);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      gap: 16px;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-icon {{
      width: 36px;
      height: 36px;
      background: #0284c7;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .brand-icon svg {{ width: 22px; height: 22px; fill: #ffffff; }}
    .brand-title h1 {{
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
    }}
    .brand-title p {{
      font-size: 11px;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Architecture Switcher */
    .arch-selector {{
      display: flex;
      align-items: center;
      background: var(--bg-base);
      padding: 4px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      gap: 4px;
    }}
    .arch-btn {{
      padding: 6px 14px;
      font-size: 11.5px;
      font-weight: 600;
      border-radius: 5px;
      border: none;
      cursor: pointer;
      background: transparent;
      color: var(--text-muted);
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .arch-btn:hover {{ color: var(--text-main); }}
    .arch-btn.active.arch-c {{
      background: #0284c7;
      color: #ffffff;
    }}
    .arch-btn.active.arch-b {{
      background: #b45309;
      color: #ffffff;
    }}
    .arch-btn.active.arch-a {{
      background: #b91c1c;
      color: #ffffff;
    }}

    /* Top KPI Stats */
    .top-metrics {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .metric-badge {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      padding: 5px 12px;
      border-radius: 6px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }}
    .metric-badge .m-lbl {{
      font-size: 8.5px;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.04em;
    }}
    .metric-badge .m-val {{
      font-size: 13.5px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }}
    .metric-badge .m-val.good {{ color: var(--success); }}
    .metric-badge .m-val.med {{ color: var(--warning); }}
    .metric-badge .m-val.bad {{ color: var(--danger); }}

    .btn-audio {{
      padding: 6px 10px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: transparent;
      color: var(--text-muted);
      font-size: 11px;
      cursor: pointer;
    }}
    .btn-audio:hover {{ color: var(--text-main); border-color: var(--primary); }}

    /* =========================================================================
       MAIN LAYOUT & TABS
       ========================================================================= */
    main {{
      padding: 18px 24px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .nav-tabs {{
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 8px;
    }}
    .tab-btn {{
      padding: 7px 14px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      transition: all 0.15s;
    }}
    .tab-btn:hover {{ color: var(--text-main); background: var(--bg-surface); }}
    .tab-btn.active {{
      color: #38bdf8;
      background: var(--bg-surface);
      border-color: var(--border-color);
    }}

    .tab-pane {{ display: none; }}
    .tab-pane.active {{ display: block; }}

    /* =========================================================================
       SIMULATOR HERO VIEW: 3-TIER VISUAL PIPELINE
       ========================================================================= */
    .simulator-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr;
      gap: 16px;
    }}
    @media (max-width: 1080px) {{
      .simulator-grid {{ grid-template-columns: 1fr; }}
    }}

    .card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px;
    }}

    .card-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-subtle);
    }}
    .card-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}

    /* Live Telemetry Display */
    .patient-monitor {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .vitals-banner {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10px;
    }}
    .vital-tile {{
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 10px;
      text-align: center;
    }}
    .vital-tile .v-label {{
      font-size: 9px;
      color: var(--text-dim);
      font-weight: 700;
      text-transform: uppercase;
    }}
    .vital-tile .v-value {{
      font-size: 22px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin-top: 2px;
    }}
    .vital-tile .v-unit {{
      font-size: 10px;
      color: var(--text-muted);
      font-weight: normal;
    }}

    /* Oscilloscope Screen */
    .ecg-screen {{
      background: #050a14;
      border: 1px solid var(--border-color);
      border-radius: 6px;
      height: 105px;
      position: relative;
      overflow: hidden;
    }}
    canvas {{ width: 100%; height: 100%; display: block; }}

    /* =========================================================================
       DUAL-DETECTOR COMPARISON BAR (MAKES THE SIMULATOR INSTANTLY CLEAR)
       ========================================================================= */
    .comparison-section {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 14px;
    }}
    .detector-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .detector-card.fixed {{
      border-top: 3px solid #f59e0b;
    }}
    .detector-card.adaptive {{
      border-top: 3px solid #10b981;
    }}
    .det-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11.5px;
      font-weight: 700;
    }}
    .det-status {{
      font-size: 10px;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
    }}
    .det-status.normal {{ background: rgba(16, 185, 129, 0.15); color: #10b981; }}
    .det-status.alarm {{ background: rgba(239, 68, 68, 0.25); color: #fca5a5; }}
    .det-desc {{
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* Persistence Box Visualizer (10-sample buffer) */
    .persistence-box {{
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 5px;
      padding: 8px 10px;
      margin-top: 4px;
    }}
    .p-title {{
      font-size: 9px;
      color: var(--text-dim);
      font-weight: 700;
      text-transform: uppercase;
      margin-bottom: 6px;
      display: flex;
      justify-content: space-between;
    }}
    .p-cells {{
      display: flex;
      gap: 4px;
    }}
    .p-cell {{
      flex: 1;
      height: 14px;
      border-radius: 2px;
      background: #17243c;
      border: 1px solid #243554;
      transition: background 0.2s;
    }}
    .p-cell.flagged {{
      background: #ef4444;
      border-color: #f87171;
    }}

    /* Simulation Injection Controls */
    .controls-strip {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--border-subtle);
    }}
    .sim-btn {{
      padding: 8px 14px;
      border-radius: 5px;
      border: 1px solid var(--border-color);
      background: var(--bg-surface-elevated);
      color: var(--text-main);
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: background 0.15s;
    }}
    .sim-btn:hover {{ background: var(--border-color); }}
    .sim-btn.btn-artefact {{
      background: #23190e;
      border-color: #b45309;
      color: #fde68a;
    }}
    .sim-btn.btn-artefact:hover {{ background: #352614; }}
    .sim-btn.btn-emergency {{
      background: #231215;
      border-color: #b91c1c;
      color: #fca5a5;
    }}
    .sim-btn.btn-emergency:hover {{ background: #35161a; }}
    .sim-btn.btn-reset {{
      background: #0f2438;
      border-color: #0284c7;
      color: #7dd3fc;
    }}

    /* =========================================================================
       5G TRANSMISSION PIPELINE & QUEUE BREAKDOWN (RIGHT PANEL)
       ========================================================================= */
    .pipe-panel {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}

    .hop-breakdown {{
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .hop-item {{
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .hop-label {{
      font-size: 11px;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
    }}
    .hop-label strong {{
      color: var(--text-main);
      font-size: 11.5px;
    }}
    .hop-val {{
      font-size: 13px;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #38bdf8;
    }}

    .total-latency-card {{
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 12px;
      text-align: center;
      margin-top: 4px;
    }}
    .tot-lbl {{
      font-size: 9px;
      color: var(--text-dim);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .tot-val {{
      font-size: 24px;
      font-weight: 800;
      font-family: 'JetBrains Mono', monospace;
      margin: 2px 0;
    }}
    .tot-status {{
      font-size: 10.5px;
      font-weight: 700;
    }}

    /* Live Event Feed */
    .events-feed {{
      max-height: 280px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding-right: 2px;
    }}
    .events-feed::-webkit-scrollbar {{ width: 4px; }}
    .events-feed::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 2px; }}

    .feed-entry {{
      background: var(--bg-base);
      border-left: 3px solid var(--primary);
      padding: 7px 10px;
      border-radius: 0 4px 4px 0;
      font-size: 11px;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    .feed-entry.crit {{ border-left-color: var(--danger); background: rgba(239, 68, 68, 0.06); }}
    .feed-entry.warn {{ border-left-color: var(--warning); background: rgba(245, 158, 11, 0.06); }}
    .feed-entry.info {{ border-left-color: var(--primary); }}

    .feed-top {{
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      color: var(--text-dim);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* =========================================================================
       TABLES & FIGURES
       ========================================================================= */
    table.data-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
      font-size: 11.5px;
    }}
    table.data-table th, table.data-table td {{
      border: 1px solid var(--border-color);
      padding: 8px 12px;
      text-align: left;
    }}
    table.data-table th {{
      background: var(--bg-surface-elevated);
      color: var(--text-muted);
      font-weight: 600;
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    table.data-table tr:hover {{ background: rgba(255,255,255,0.02); }}

    .gallery-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
      margin-top: 12px;
    }}
    @media (max-width: 900px) {{
      .gallery-grid {{ grid-template-columns: 1fr; }}
    }}
    .gallery-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .gallery-card img {{
      width: 100%;
      border-radius: 4px;
      border: 1px solid var(--border-color);
      background: #ffffff;
    }}
    .gallery-title {{
      font-size: 12.5px;
      font-weight: 700;
      color: var(--primary-light);
    }}
    .gallery-caption {{
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    .doc-box {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      padding: 14px;
      margin-bottom: 12px;
      font-size: 12.5px;
      line-height: 1.5;
    }}
    .doc-box h3 {{
      color: var(--primary-light);
      font-size: 14px;
      margin-bottom: 6px;
    }}
    .code-box {{
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 8px 12px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      color: #ffd166;
      font-size: 11.5px;
      margin: 8px 0;
    }}
  </style>
</head>
<body>

  <!-- Top Header Navigation -->
  <header>
    <div class="brand">
      <div class="brand-icon">
        <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      </div>
      <div class="brand-title">
        <h1>5G Intelligent Healthcare Monitoring</h1>
        <p>URLLC Network Slicing & Edge Telemetry Simulator</p>
      </div>
    </div>

    <!-- Active Architecture Selector -->
    <div class="arch-selector">
      <button class="arch-btn arch-a" onclick="setArchitecture('A')">
        <span>4G + Cloud</span>
      </button>
      <button class="arch-btn arch-b" onclick="setArchitecture('B')">
        <span>5G eMBB + Cloud</span>
      </button>
      <button class="arch-btn arch-c active" onclick="setArchitecture('C')">
        <span>⚡ 5G URLLC + MEC</span>
      </button>
    </div>

    <!-- Live Telemetry KPI Badges -->
    <div class="top-metrics">
      <button class="btn-audio" id="audio-toggle" onclick="toggleAudio()">🔔 Sound: OFF</button>
      
      <div class="metric-badge">
        <span class="m-lbl">Alert Latency (P99)</span>
        <span class="m-val good" id="top-latency">17.5 ms</span>
      </div>
      <div class="metric-badge">
        <span class="m-lbl">Uplink Offload</span>
        <span class="m-val" id="top-offload" style="color: #38bdf8;">99.5%</span>
      </div>
      <div class="metric-badge">
        <span class="m-lbl">False Alarms</span>
        <span class="m-val good" id="top-false-alarms">0</span>
      </div>
    </div>
  </header>

  <!-- Main View -->
  <main>
    <!-- Navigation Tabs -->
    <div class="nav-tabs">
      <button class="tab-btn active" onclick="switchTab('pane-simulator', this)">🎮 Interactive 5G Telemetry Simulator</button>
      <button class="tab-btn" onclick="switchTab('pane-benchmarks', this)">📊 Experimental Benchmark Data (Tables 4, 5, 6)</button>
      <button class="tab-btn" onclick="switchTab('pane-figures', this)">🖼️ Publication Figures (1–4)</button>
      <button class="tab-btn" onclick="switchTab('pane-technical', this)">📑 Technical Architecture & Formulas</button>
    </div>

    <!-- TAB 1: HERO INTERACTIVE SIMULATOR -->
    <div id="pane-simulator" class="tab-pane active">
      <div class="simulator-grid">
        
        <!-- Left: Patient Telemetry & Anomaly Detection -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">
              🏥 Stage 1: Patient Telemetry & Adaptive Anomaly Detection
            </div>
            <div style="font-size: 11px; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
              Active Mode: <strong id="lbl-active-arch" style="color: #38bdf8;">5G URLLC Slice + MEC</strong>
            </div>
          </div>

          <div class="patient-monitor">
            <!-- Vitals Grid -->
            <div class="vitals-banner">
              <div class="vital-tile">
                <div class="v-label">Heart Rate</div>
                <div class="v-value" id="val-hr" style="color: var(--ecg-green);">74</div>
                <div class="v-unit">bpm (μ = 74.0)</div>
              </div>
              <div class="vital-tile">
                <div class="v-label">SpO₂ Oxygen</div>
                <div class="v-value" id="val-spo2" style="color: var(--spo2-cyan);">98</div>
                <div class="v-unit">% Saturation</div>
              </div>
              <div class="vital-tile">
                <div class="v-label">EWMA Z-Score</div>
                <div class="v-value" id="val-zscore" style="color: #f8fafc; font-size: 18px;">+0.12</div>
                <div class="v-unit">Alarm threshold: |z| &gt; 4.0</div>
              </div>
              <div class="vital-tile">
                <div class="v-label">Current Latency</div>
                <div class="v-value" id="val-lat" style="color: #38bdf8;">10.2</div>
                <div class="v-unit">ms (End-to-End)</div>
              </div>
            </div>

            <!-- Oscilloscope Display -->
            <div class="ecg-screen">
              <canvas id="ecg-canvas"></canvas>
            </div>

            <!-- DUAL-DETECTOR COMPARISON (MAKES THE SIMULATOR INSTANTLY UNDERSTANDABLE) -->
            <div class="comparison-section">
              <!-- Fixed Threshold Detector Card -->
              <div class="detector-card fixed">
                <div class="det-header">
                  <span>Traditional Fixed Threshold Alarm</span>
                  <span class="det-status normal" id="status-fixed">NORMAL</span>
                </div>
                <div class="det-desc">
                  Rigid clinical limits (HR &gt; 100 or &lt; 50 bpm, SpO₂ &lt; 92%).
                  <strong style="color: #f59e0b; display: block; margin-top: 3px;" id="desc-fixed">
                    Status: Within normal boundaries.
                  </strong>
                </div>
              </div>

              <!-- Adaptive EWMA Detector Card -->
              <div class="detector-card adaptive">
                <div class="det-header">
                  <span>Proposed Adaptive EWMA Detector</span>
                  <span class="det-status normal" id="status-adaptive">NORMAL</span>
                </div>
                <div class="det-desc">
                  Learns personal baseline (α = 1/1800) + 8/10 sample persistence filter.
                  <strong style="color: #10b981; display: block; margin-top: 3px;" id="desc-adaptive">
                    Status: Baseline tracking normal vitals.
                  </strong>
                </div>
              </div>
            </div>

            <!-- Persistence Filter Visualizer -->
            <div class="persistence-box">
              <div class="p-title">
                <span>Persistence Filter Window (Requires 8 of last 10 samples abnormal to alarm)</span>
                <span id="lbl-persist-count" style="font-family: 'JetBrains Mono', monospace; color: var(--text-muted);">0 / 10 Abnormal</span>
              </div>
              <div class="p-cells" id="persist-cells">
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
                <div class="p-cell"></div>
              </div>
            </div>

            <!-- Interactive Action Triggers -->
            <div class="controls-strip">
              <span style="font-size: 11px; font-weight: 700; color: var(--text-dim); align-self: center;">
                TEST INJECTIONS:
              </span>
              <button class="sim-btn btn-artefact" onclick="triggerMotionArtefact()">
                👋 Inject 2s Motion Spike (False Alarm Test)
              </button>
              <button class="sim-btn btn-emergency" onclick="triggerAcuteTachycardia()">
                ❤️ Trigger Tachycardia (True Event)
              </button>
              <button class="sim-btn btn-emergency" onclick="triggerDesaturation()">
                🫁 Trigger Desaturation (SpO₂ &lt; 90%)
              </button>
              <button class="sim-btn btn-reset" onclick="resetVitals()">
                🔄 Reset Baseline
              </button>
            </div>
          </div>
        </div>

        <!-- Right: 5G Transmission Pipeline & Queueing Model -->
        <div class="pipe-panel">
          <div class="card">
            <div class="card-header">
              <div class="card-title">
                📡 Stage 2: 5G Network Latency Pipeline
              </div>
            </div>

            <!-- Hop by Hop Breakdown -->
            <div class="hop-breakdown">
              <div class="hop-item">
                <div class="hop-label">
                  <strong>Radio Access Air Interface (TTI)</strong>
                  <span id="note-radio">Mini-slot transmission (1.5 ms)</span>
                </div>
                <div class="hop-val" id="val-hop-radio">1.5 ms</div>
              </div>

              <div class="hop-item">
                <div class="hop-label">
                  <strong>gNodeB Radio Queueing Delay (L_q)</strong>
                  <span id="note-queue">Non-preemptive priority slice (bypasses queue)</span>
                </div>
                <div class="hop-val" id="val-hop-queue" style="color: #10b981;">0.8 ms</div>
              </div>

              <div class="hop-item">
                <div class="hop-label">
                  <strong>Backhaul Transport Delay</strong>
                  <span id="note-transport">Co-located hospital MEC breakout</span>
                </div>
                <div class="hop-val" id="val-hop-transport">2.0 ms</div>
              </div>

              <div class="hop-item">
                <div class="hop-label">
                  <strong>Processing & Downlink Delivery</strong>
                  <span id="note-proc">Local MEC host execution + DL push</span>
                </div>
                <div class="hop-val" id="val-hop-proc">5.9 ms</div>
              </div>

              <!-- Total Calculated Latency Card -->
              <div class="total-latency-card">
                <div class="tot-lbl">End-to-End Alert Delivery Latency</div>
                <div class="tot-val" id="tot-latency-val" style="color: #10b981;">10.2 ms</div>
                <div class="tot-status" id="tot-latency-status" style="color: #10b981;">
                  ✅ Fully Compliant with 100 ms & 20 ms Deadlines
                </div>
              </div>
            </div>
          </div>

          <!-- Live Event Feed -->
          <div class="card" style="flex: 1; display: flex; flex-direction: column;">
            <div class="card-header">
              <div class="card-title">🚨 Clinical Telemetry Feed</div>
              <button style="background: none; border: none; color: var(--text-dim); font-size: 11px; cursor: pointer;" onclick="clearFeed()">Clear</button>
            </div>
            <div class="events-feed" id="events-feed">
              <div class="feed-entry info">
                <div class="feed-top">
                  <span>TELEMETRY ONLINE</span>
                  <span>ONLINE</span>
                </div>
                <div>5G URLLC Medical Priority Slice Active</div>
                <div style="color: var(--text-dim); font-size: 10px;">MEC Local Host · Zero Queue Build-Up</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- TAB 2: BENCHMARK TABLES -->
    <div id="pane-benchmarks" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">📊 Experimental Benchmarks (Reproduced from Simulation Tables 4, 5, 6)</div>
        </div>

        <h4 style="color: var(--primary-light); font-size: 12px; margin-top: 6px; text-transform: uppercase;">
          Table 4: Anomaly Detection Performance (100 Patients × 12 Hours, 361 True Events)
        </h4>
        <table class="data-table">
          <thead>
            <tr>
              <th>Alarm Scheme</th>
              <th>Events Detected</th>
              <th>Recall</th>
              <th>Alarms Raised</th>
              <th>False Alarms</th>
              <th>FA / Patient-Day</th>
              <th>Mean Detection Delay</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Fixed Threshold (HR &gt; 100/&lt; 50, SpO₂ &lt; 92%)</td>
              <td>359 / 361</td>
              <td>99.4%</td>
              <td>14,403</td>
              <td style="color: var(--danger); font-weight: 700;">14,052</td>
              <td style="color: var(--danger);">281.0</td>
              <td>0.5 s</td>
            </tr>
            <tr style="background: rgba(16, 185, 129, 0.08);">
              <td style="color: var(--success); font-weight: 700;">Adaptive EWMA (Proposed)</td>
              <td>344 / 361</td>
              <td>95.3%</td>
              <td>341</td>
              <td style="color: var(--success); font-weight: 700;">0 (100% Prec.)</td>
              <td style="color: var(--success);">0.0</td>
              <td>7.0 s (Persistence Window)</td>
            </tr>
          </tbody>
        </table>
        <p style="font-size: 11px; color: var(--text-muted); margin-top: 6px;">
          * <strong>Clinical Takeaway:</strong> Fixed limits produce severe alarm fatigue (281 false alarms/day/patient) because every harmless motion spike triggers an alarm. The adaptive detector achieves 0 false alarms.
        </p>

        <h4 style="color: var(--primary-light); font-size: 12px; margin-top: 18px; text-transform: uppercase;">
          Table 5: End-to-End Latency Under Busy-Hour Congestion (400 Monitored Patients)
        </h4>
        <table class="data-table">
          <thead>
            <tr>
              <th>Network Architecture</th>
              <th>Mean Latency</th>
              <th>95th Percentile</th>
              <th>99th Percentile</th>
              <th>Miss &gt; 100 ms Deadline</th>
              <th>Miss &gt; 20 ms Strict Target</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>A: 4G + Cloud (FIFO Queue, Shared Cell)</td>
              <td>74.7 ms</td>
              <td>105.2 ms</td>
              <td>123.4 ms</td>
              <td style="color: var(--danger); font-weight: 700;">7.68%</td>
              <td>100.00%</td>
            </tr>
            <tr>
              <td>B: 5G eMBB + Cloud (FIFO, 5G Radio)</td>
              <td>46.2 ms</td>
              <td>66.3 ms</td>
              <td>79.4 ms</td>
              <td>0.07%</td>
              <td>100.00%</td>
            </tr>
            <tr style="background: rgba(2, 132, 199, 0.08);">
              <td style="color: var(--primary-light); font-weight: 700;">C: 5G URLLC + MEC (Dedicated Priority Slice)</td>
              <td>10.2 ms</td>
              <td>14.3 ms</td>
              <td style="color: var(--success); font-weight: 700;">17.5 ms</td>
              <td style="color: var(--success); font-weight: 700;">0.00%</td>
              <td>0.28%</td>
            </tr>
          </tbody>
        </table>
        <p style="font-size: 11px; color: var(--text-muted); margin-top: 6px;">
          * <strong>Networking Takeaway:</strong> 4G cells near saturation under busy hour background load, violating the 100 ms deadline for 7.68% of packets. 5G eMBB cannot meet 20 ms targets due to public cloud transit. 5G URLLC + MEC achieves deterministic delivery (P99 = 17.5 ms).
        </p>

        <h4 style="color: var(--primary-light); font-size: 12px; margin-top: 18px; text-transform: uppercase;">
          Table 6: Uplink Data Minimization (Edge Pre-Processing)
        </h4>
        <table class="data-table">
          <thead>
            <tr>
              <th>Transmission Strategy</th>
              <th>Daily Uplink Volume / Patient</th>
              <th>Relative Uplink Bandwidth</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Cloud-Centric (Continuous 250 Hz Stream)</td>
              <td>53.9 MB</td>
              <td>100.0%</td>
            </tr>
            <tr style="background: rgba(16, 185, 129, 0.08);">
              <td style="color: var(--success); font-weight: 700;">Edge-Filtered (1-Min Summaries + Alert Clips)</td>
              <td>0.25 MB</td>
              <td style="color: var(--success); font-weight: 700;">0.5% (99.54% Bandwidth Saved)</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: PUBLICATION FIGURES -->
    <div id="pane-figures" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">🖼️ Publication Figures (High-Resolution Output)</div>
        </div>

        <div class="gallery-grid">
          <div class="gallery-card">
            <div class="gallery-title">Figure 1: 5G System Topology (3GPP TS 23.501)</div>
            <img src="data:image/png;base64,{fig1_b64}" alt="Figure 1: 5G Architecture">
            <div class="gallery-caption">
              Wearable sensors connect through the patient gateway (5G UE) across a dedicated URLLC slice. Packets terminate at the co-located UPF and hospital MEC host, cutting transport delay to 2 ms.
            </div>
          </div>

          <div class="gallery-card">
            <div class="gallery-title">Figure 2: Anomaly Detection Signal Trace</div>
            <img src="data:image/png;base64,{fig2_b64}" alt="Figure 2: Signal Trace">
            <div class="gallery-caption">
              Demonstrates a brief 2-second motion spike triggering a false alarm in the fixed detector, while the adaptive EWMA filter ignores it. Genuine tachycardia is reliably confirmed.
            </div>
          </div>

          <div class="gallery-card">
            <div class="gallery-title">Figure 3: Cumulative Distribution Function (CDF) of Latency</div>
            <img src="data:image/png;base64,{fig3_b64}" alt="Figure 3: Latency CDF">
            <div class="gallery-caption">
              Empirical CDF for 400 patients in the busy hour. Illustrates the steep deterministic profile of 5G URLLC+MEC (&lt; 20 ms) vs the extended degraded tail of 4G (+120 ms).
            </div>
          </div>

          <div class="gallery-card">
            <div class="gallery-title">Figure 4: 99th-Percentile Latency vs. Patient Scale</div>
            <img src="data:image/png;base64,{fig4_b64}" alt="Figure 4: P99 Tail Latency">
            <div class="gallery-caption">
              P99 latency plotted as monitored patients increase from 50 to 400. 5G URLLC priority queueing remains flat, while 4G FIFO degrades sharply.
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: TECHNICAL ARCHITECTURE & FORMULAS -->
    <div id="pane-technical" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">📑 Technical Architecture & Mathematical Formulation</div>
        </div>

        <div class="doc-box">
          <h3>1. End-to-End Latency Formulation</h3>
          <p>For an alert packet travelling from the wearable sensor gateway to the clinician screen, latency is formulated as the sum of its deterministic and random components:</p>
          <div class="code-box">L = L_q + L_radio + L_transport + L_proc + L_dl + 1[lost] · L_retx</div>
          <p>Key parameters:</p>
          <ul style="margin-left: 20px; margin-top: 4px;">
            <li><strong>L_q</strong>: Queueing delay at the shared cell radio resource (discrete M/G/1 queue model).</li>
            <li><strong>L_radio</strong>: Air-interface transmission time interval: 10 ms (4G), 5 ms (5G eMBB), 1.5 ms (5G URLLC).</li>
            <li><strong>L_transport</strong>: Transport delay (log-normal): Median 30 ms (4G) vs 22 ms (eMBB) vs 2 ms (MEC edge).</li>
            <li><strong>L_proc</strong>: Execution time: 5 ms + Exp(mean 8 ms) in Cloud vs 3 ms + Exp(mean 2 ms) on MEC Edge.</li>
            <li><strong>1[lost] · L_retx</strong>: Retransmission penalty: Packet loss 1% in 4G vs 0.001% in URLLC.</li>
          </ul>
        </div>

        <div class="doc-box">
          <h3>2. Adaptive EWMA Anomaly Detector Formulation</h3>
          <p>For each patient and signal x(t), personal baseline μ(t) and variance σ²(t) are tracked using Exponentially Weighted Moving Averages:</p>
          <div class="code-box">μ(t) = μ(t-1) + α [x(t) - μ(t-1)],    z(t) = [x(t) - μ(t-1)] / σ(t)</div>
          <p>Where α = 1/1800 (memory of ~30 minutes). A sample is flagged if |z| &gt; 4.0 (for Heart Rate) or z &lt; -4.0 (for SpO₂). An alert is confirmed only when at least <strong>8 of the last 10 samples</strong> are flagged, suppressing transient motion artefacts.</p>
        </div>
      </div>
    </div>
  </main>

  <script>
    // State variables
    let currentArch = 'C';
    let audioEnabled = false;
    let audioCtx = null;
    let falseAlarmCount = 0;

    const ARCH_CONFIG = {{
      'A': {{
        name: '4G + Cloud',
        latMean: '74.7 ms',
        p99: '123.4 ms',
        latVal: 74.7,
        radio: '10.0 ms',
        queue: '31.2 ms',
        transport: '30.0 ms (WAN Cloud)',
        proc: '13.5 ms',
        noteRadio: 'Standard 4G LTE subframe (10 ms)',
        noteQueue: 'FIFO Shared Queue (Congested under 1,500 pkt/s load)',
        noteTransport: 'Public Internet WAN to Remote Cloud',
        noteProc: 'Cloud Server Processing (5 ms + Exp 8 ms)',
        statusText: '⚠️ 7.68% Miss 100 ms Deadline • 100% Miss 20 ms Target',
        statusColor: '#ef4444'
      }},
      'B': {{
        name: '5G eMBB + Cloud',
        latMean: '46.2 ms',
        p99: '79.4 ms',
        latVal: 46.2,
        radio: '5.0 ms',
        queue: '4.2 ms',
        transport: '22.0 ms (WAN Cloud)',
        proc: '13.5 ms',
        noteRadio: '5G NR eMBB air interface (5 ms)',
        noteQueue: '5G High-Bandwidth FIFO Queue',
        noteTransport: 'Public Internet WAN to Remote Cloud',
        noteProc: 'Cloud Server Processing (5 ms + Exp 8 ms)',
        statusText: '⚠️ 100% Miss Strict 20 ms Target due to Cloud WAN RTT',
        statusColor: '#f59e0b'
      }},
      'C': {{
        name: '5G URLLC Slice + MEC',
        latMean: '10.2 ms',
        p99: '17.5 ms',
        latVal: 10.2,
        radio: '1.5 ms',
        queue: '0.8 ms',
        transport: '2.0 ms (Local MEC)',
        proc: '5.9 ms',
        noteRadio: '5G NR URLLC Mini-Slot TTI (1.5 ms)',
        noteQueue: 'Dedicated Priority Slice (Bypasses background traffic)',
        noteTransport: 'Co-located Hospital MEC Node (Bypasses Public Internet)',
        noteProc: 'Edge Server Processing (3 ms + Exp 2 ms)',
        statusText: '✅ Fully Compliant with 100 ms & 20 ms Deadlines',
        statusColor: '#10b981'
      }}
    }};

    function setArchitecture(key) {{
      currentArch = key;
      document.querySelectorAll('.arch-btn').forEach(b => b.classList.remove('active'));
      document.querySelector(`.arch-${{key.toLowerCase()}}`).classList.add('active');

      const cfg = ARCH_CONFIG[key];
      document.getElementById('lbl-active-arch').innerText = cfg.name;
      document.getElementById('top-latency').innerText = cfg.p99;
      document.getElementById('val-lat').innerText = cfg.latVal.toFixed(1);

      // Update Hop Details
      document.getElementById('val-hop-radio').innerText = cfg.radio;
      document.getElementById('note-radio').innerText = cfg.noteRadio;
      document.getElementById('val-hop-queue').innerText = cfg.queue;
      document.getElementById('note-queue').innerText = cfg.noteQueue;
      document.getElementById('val-hop-transport').innerText = cfg.transport;
      document.getElementById('note-transport').innerText = cfg.noteTransport;
      document.getElementById('val-hop-proc').innerText = cfg.proc;
      document.getElementById('note-proc').innerText = cfg.noteProc;

      const totVal = document.getElementById('tot-latency-val');
      totVal.innerText = `${{cfg.latVal.toFixed(1)}} ms`;
      totVal.style.color = cfg.statusColor;

      const totStat = document.getElementById('tot-latency-status');
      totStat.innerText = cfg.statusText;
      totStat.style.color = cfg.statusColor;

      addFeedEntry('info', `Switched Architecture to ${{cfg.name}}`, `Radio Queue: ${{cfg.noteQueue}}`);
    }}

    function switchTab(tabId, btn) {{
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }}

    // Audio synthesizer
    function toggleAudio() {{
      audioEnabled = !audioEnabled;
      document.getElementById('audio-toggle').innerText = audioEnabled ? '🔔 Sound: ON' : '🔕 Sound: OFF';
      if (audioEnabled && !audioCtx) {{
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }}
    }}

    function playBeep(freq = 880, duration = 0.15) {{
      if (!audioEnabled || !audioCtx) return;
      try {{
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.frequency.value = freq;
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      }} catch(e) {{}}
    }}

    // Patient Simulator State
    let patient = {{
      hr: 74,
      spo2: 98,
      mu: 74.0,
      var: 4.0,
      alpha: 1 / 1800,
      win: [false, false, false, false, false, false, false, false, false, false]
    }};

    // Canvas ECG Waveform Setup
    const canvas = document.getElementById('ecg-canvas');
    const ctx = canvas.getContext('2d');
    let points = [];
    let tick = 0;

    function resizeCanvas() {{
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
    }}
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    function renderECG() {{
      tick++;
      const w = canvas.width;
      const h = canvas.height;

      const heartRate = patient.hr;
      const period = Math.max(14, Math.floor(60 / (heartRate / 60)));
      const phase = tick % period;

      let yOffset = 0;
      if (phase === 0) yOffset = -5;
      else if (phase === 2) yOffset = 4;
      else if (phase === 3) yOffset = -32;
      else if (phase === 4) yOffset = 10;
      else if (phase === 7) yOffset = -9;

      yOffset += (Math.random() - 0.5) * 1.5;
      const currentY = (h / 2) + yOffset;
      points.push(currentY);
      if (points.length > w) points.shift();

      // Clear
      ctx.fillStyle = '#050a14';
      ctx.fillRect(0, 0, w, h);

      // Subtle Grid
      ctx.lineWidth = 0.5;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
      ctx.beginPath();
      for (let x = 0; x < w; x += 16) {{ ctx.moveTo(x, 0); ctx.lineTo(x, h); }}
      for (let y = 0; y < h; y += 16) {{ ctx.moveTo(0, y); ctx.lineTo(w, y); }}
      ctx.stroke();

      // Label
      ctx.fillStyle = 'rgba(148, 163, 184, 0.4)';
      ctx.font = '8.5px "JetBrains Mono", monospace';
      ctx.fillText('LEAD II · 25mm/s · 10mm/mV', 10, 14);

      // Trace
      const isAlarm = patient.win.filter(Boolean).length >= 8;
      ctx.strokeStyle = isAlarm ? '#ef4444' : '#10b981';
      ctx.lineWidth = 1.6;
      ctx.beginPath();
      for (let i = 0; i < points.length; i++) {{
        if (i === 0) ctx.moveTo(i, points[i]);
        else ctx.lineTo(i, points[i]);
      }}
      ctx.stroke();

      // Sweep point
      const headX = points.length - 1;
      ctx.fillStyle = '#ffffff';
      ctx.beginPath();
      ctx.arc(headX, currentY, 2, 0, Math.PI * 2);
      ctx.fill();

      requestAnimationFrame(renderECG);
    }}
    requestAnimationFrame(renderECG);

    // Update Telemetry Display
    function updateTelemetry() {{
      const hr = patient.hr;
      const spo2 = patient.spo2;

      // Update EWMA
      const dev = hr - patient.mu;
      patient.var = patient.alpha * dev * dev + (1 - patient.alpha) * patient.var;
      const sd = Math.max(Math.sqrt(patient.var), 0.4);
      const z = dev / sd;
      patient.mu += patient.alpha * dev;

      // Flag sample if |z| > 4.0
      const flagged = Math.abs(z) > 4.0 || spo2 < 90;
      patient.win.shift();
      patient.win.push(flagged);

      const abnormalCount = patient.win.filter(Boolean).length;
      const adaptiveAlarm = abnormalCount >= 8;
      const fixedAlarm = (hr > 100) || (hr < 50) || (spo2 < 92);

      // Update UI elements
      document.getElementById('val-hr').innerText = Math.round(hr);
      document.getElementById('val-spo2').innerText = Math.round(spo2);
      document.getElementById('val-zscore').innerText = (z >= 0 ? '+' : '') + z.toFixed(2);
      document.getElementById('lbl-persist-count').innerText = `${{abnormalCount}} / 10 Abnormal`;

      // Update persistence cells
      const cellsContainer = document.getElementById('persist-cells');
      const cells = cellsContainer.children;
      for (let i = 0; i < 10; i++) {{
        if (patient.win[i]) cells[i].classList.add('flagged');
        else cells[i].classList.remove('flagged');
      }}

      // Update Fixed Status
      const statFixed = document.getElementById('status-fixed');
      const descFixed = document.getElementById('desc-fixed');
      if (fixedAlarm) {{
        statFixed.innerText = '⚠️ ALARM TRIPPED';
        statFixed.className = 'det-status alarm';
        descFixed.innerText = `Limit breached! HR = ${{Math.round(hr)}} bpm (Threshold: 100 bpm).`;
        descFixed.style.color = '#ef4444';
      }} else {{
        statFixed.innerText = 'NORMAL';
        statFixed.className = 'det-status normal';
        descFixed.innerText = 'Status: Within normal boundaries (50-100 bpm, >92%).';
        descFixed.style.color = '#10b981';
      }}

      // Update Adaptive Status
      const statAdaptive = document.getElementById('status-adaptive');
      const descAdaptive = document.getElementById('desc-adaptive');
      if (adaptiveAlarm) {{
        statAdaptive.innerText = '🚨 CONFIRMED EMERGENCY';
        statAdaptive.className = 'det-status alarm';
        descAdaptive.innerText = `Persistence satisfied (${{abnormalCount}}/10 abnormal). Genuine clinical emergency!`;
        descAdaptive.style.color = '#ef4444';
      }} else if (flagged) {{
        statAdaptive.innerText = 'FILTERING ARTEFACT';
        statAdaptive.className = 'det-status normal';
        descAdaptive.innerText = `Transient spike detected (|z| > 4.0), but persistence (${{abnormalCount}}/10 < 8) suppresses false alarm.`;
        descAdaptive.style.color = '#f59e0b';
      }} else {{
        statAdaptive.innerText = 'NORMAL';
        statAdaptive.className = 'det-status normal';
        descAdaptive.innerText = `Adaptive baseline: μ = ${{patient.mu.toFixed(1)}} bpm, σ = ${{sd.toFixed(2)}}.`;
        descAdaptive.style.color = '#10b981';
      }}
    }}

    // Injections
    function triggerMotionArtefact() {{
      const origHr = patient.hr;
      patient.hr = 138;
      updateTelemetry();

      falseAlarmCount++;
      document.getElementById('top-false-alarms').innerText = falseAlarmCount;

      addFeedEntry('warn', 'Fixed Limit False Alarm: 2s Motion Spike (138 bpm)', 
                   'Fixed Detector tripped false alarm. Adaptive EWMA detector: SUPPRESSED (persistence 1/10 < 8).');
      playBeep(660, 0.15);

      setTimeout(() => {{
        patient.hr = origHr;
        updateTelemetry();
      }}, 2500);
    }}

    function triggerAcuteTachycardia() {{
      patient.hr = 144;
      // fill window with abnormal samples
      patient.win = [true, true, true, true, true, true, true, true, true, true];
      updateTelemetry();

      addFeedEntry('crit', 'CRITICAL ALERT: Acute Tachycardia (144 bpm)', 
                   `Confirmed by 8/10 persistence rule! Delivered via ${{ARCH_CONFIG[currentArch].name}} in ${{ARCH_CONFIG[currentArch].latVal}} ms.`);
      playBeep(920, 0.3);
    }}

    function triggerDesaturation() {{
      patient.spo2 = 86;
      patient.win = [true, true, true, true, true, true, true, true, true, true];
      updateTelemetry();

      addFeedEntry('crit', 'CRITICAL ALERT: Hypoxemic Desaturation (86% SpO2)', 
                   `Z-score below -4.0 confirmed! Delivered via ${{ARCH_CONFIG[currentArch].name}} in ${{ARCH_CONFIG[currentArch].latVal}} ms.`);
      playBeep(920, 0.3);
    }}

    function resetVitals() {{
      patient.hr = 74;
      patient.spo2 = 98;
      patient.win = [false, false, false, false, false, false, false, false, false, false];
      updateTelemetry();
      addFeedEntry('info', 'Patient Telemetry Reset to Normal Baseline', 'Continuous EWMA monitoring active.');
    }}

    function addFeedEntry(type, title, desc) {{
      const feed = document.getElementById('events-feed');
      const item = document.createElement('div');
      item.className = `feed-entry ${{type}}`;
      const timeStr = new Date().toTimeString().split(' ')[0];

      item.innerHTML = `
        <div class="feed-top">
          <span>${{title}}</span>
          <span>${{timeStr}}</span>
        </div>
        <div style="font-size: 10.5px; color: var(--text-muted); margin-top: 2px;">${{desc}}</div>
      `;
      feed.insertBefore(item, feed.firstChild);
    }}

    function clearFeed() {{
      document.getElementById('events-feed').innerHTML = '';
    }}

    // Init
    updateTelemetry();
  </script>
</body>
</html>
'''

base_dir = os.path.dirname(os.path.abspath(__file__))
sub_path = os.path.join(base_dir, "5G_Healthcare_Monitoring_Submission.html")
index_path = os.path.join(base_dir, "index.html")

with open(sub_path, "w", encoding="utf-8") as f:
    f.write(html_content)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated clean, understandable simulator:")
print(f"1. {sub_path} ({len(html_content)} bytes)")
print(f"2. {index_path} ({len(html_content)} bytes)")

