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
  <title>5G-Enabled Intelligent Healthcare Monitoring | Clinical Operations Center</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #0a0f1d;
      --bg-surface: #111a2e;
      --bg-surface-elevated: #17233d;
      --border-color: #1e2d4a;
      --border-highlight: #2c4168;
      --primary: #0ea5e9;
      --primary-glow: rgba(14, 165, 233, 0.20);
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --ecg-green: #22c55e;
      --spo2-cyan: #06b6d4;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Inter', sans-serif;
      background: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }}

    /* =========================================================================
       ORIGINAL SLEEK TOP NAVIGATION BAR (Clean, Single Row, Perfectly Aligned)
       ========================================================================= */
    header {{
      background: rgba(17, 26, 46, 0.90);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-color);
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .brand-logo {{
      width: 38px;
      height: 38px;
      background: linear-gradient(135deg, #0ea5e9, #3b82f6);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 10px rgba(14, 165, 233, 0.3);
    }}
    .brand-logo svg {{ width: 22px; height: 22px; fill: white; }}
    .brand-text h1 {{
      font-size: 16px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--text-main);
    }}
    .brand-text p {{
      font-size: 11px;
      color: var(--text-muted);
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Architecture Switcher */
    .arch-switch-container {{
      display: flex;
      align-items: center;
      background: var(--bg-base);
      padding: 4px;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      gap: 4px;
    }}
    .arch-btn {{
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      border: none;
      cursor: pointer;
      background: transparent;
      color: var(--text-muted);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .arch-btn:hover {{ color: var(--text-main); }}
    .arch-btn.active {{
      background: var(--bg-surface-elevated);
      color: var(--text-main);
    }}
    .arch-btn.active.arch-c {{
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: white;
    }}
    .arch-btn.active.arch-a {{
      background: linear-gradient(135deg, #dc2626, #b91c1c);
      color: white;
    }}
    .arch-btn.active.arch-b {{
      background: linear-gradient(135deg, #d97706, #b45309);
      color: white;
    }}

    /* Live Telemetry Ticker */
    .top-stats {{
      display: flex;
      gap: 14px;
      align-items: center;
    }}
    .stat-pill {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      padding: 6px 12px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      align-items: flex-end;
    }}
    .stat-pill .label {{ font-size: 9px; color: var(--text-dim); text-transform: uppercase; font-weight: 700; }}
    .stat-pill .val {{ font-size: 14px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }}
    .stat-pill .val.latency-good {{ color: var(--success); }}
    .stat-pill .val.latency-bad {{ color: var(--danger); }}
    .stat-pill .val.latency-med {{ color: var(--warning); }}

    #audio-toggle {{
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.2s;
    }}
    #audio-toggle:hover {{
      color: var(--text-main);
      border-color: var(--primary);
    }}

    /* Main Container */
    main {{
      padding: 20px;
      display: grid;
      grid-template-columns: 2.3fr 1fr;
      gap: 20px;
      flex: 1;
    }}

    @media (max-width: 1080px) {{
      main {{ grid-template-columns: 1fr; }}
    }}

    /* Tabs Bar */
    .tabs-header {{
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 16px;
      padding-bottom: 8px;
      overflow-x: auto;
    }}
    .tab-link {{
      padding: 8px 14px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      border-radius: 6px;
      transition: 0.2s;
      white-space: nowrap;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .tab-link:hover {{ color: var(--text-main); background: var(--bg-surface); }}
    .tab-link.active {{
      color: var(--primary);
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
    }}

    /* Card Panels */
    .panel {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      position: relative;
    }}
    .panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }}
    .panel-title {{
      font-size: 14px;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--success);
    }}

    /* Patient Beds Grid */
    .beds-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px;
    }}
    @media (max-width: 680px) {{
      .beds-grid {{ grid-template-columns: 1fr; }}
    }}

    .bed-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      transition: all 0.2s ease;
      position: relative;
      overflow: hidden;
    }}
    .bed-card.alarm-critical {{
      border-color: var(--danger);
      background: rgba(239, 68, 68, 0.05);
    }}
    .bed-card.alarm-false {{
      border-color: var(--warning);
      background: rgba(245, 158, 11, 0.05);
    }}
    .bed-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .bed-id {{
      font-size: 12.5px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .bed-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      background: rgba(16, 185, 129, 0.15);
      color: var(--success);
    }}
    .bed-badge.critical {{ background: rgba(239, 68, 68, 0.25); color: #fca5a5; }}
    .bed-badge.warning {{ background: rgba(245, 158, 11, 0.25); color: #fde68a; }}

    .vitals-strip {{
      display: flex;
      gap: 10px;
      background: rgba(10, 15, 29, 0.6);
      padding: 8px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
    }}
    .vital-box {{
      flex: 1;
      text-align: center;
    }}
    .vital-box .v-label {{ font-size: 9px; color: var(--text-dim); text-transform: uppercase; font-weight: 600; }}
    .vital-box .v-val {{ font-size: 16px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }}
    .vital-box.hr .v-val {{ color: var(--ecg-green); }}
    .vital-box.spo2 .v-val {{ color: var(--spo2-cyan); }}
    .vital-box.temp .v-val {{ color: #38bdf8; font-size: 14px; }}

    /* Canvas Oscilloscope */
    .canvas-container {{
      background: #060b14;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      position: relative;
      height: 72px;
      overflow: hidden;
    }}
    canvas {{ width: 100%; height: 100%; display: block; }}

    /* Simulation Control Buttons */
    .sim-controls {{
      display: flex;
      gap: 8px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--border-color);
      flex-wrap: wrap;
    }}
    .action-btn {{
      padding: 7px 12px;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: var(--bg-surface-elevated);
      color: var(--text-main);
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}
    .action-btn:hover {{ background: var(--border-highlight); }}
    .action-btn.btn-danger {{ background: rgba(239, 68, 68, 0.15); border-color: #991b1b; color: #fca5a5; }}
    .action-btn.btn-danger:hover {{ background: rgba(239, 68, 68, 0.25); }}
    .action-btn.btn-warning {{ background: rgba(245, 158, 11, 0.15); border-color: #92400e; color: #fde68a; }}
    .action-btn.btn-warning:hover {{ background: rgba(245, 158, 11, 0.25); }}
    .action-btn.btn-primary {{ background: rgba(14, 165, 233, 0.15); border-color: #0284c7; color: #7dd3fc; }}
    .action-btn.btn-primary:hover {{ background: rgba(14, 165, 233, 0.25); }}

    /* Right Column: Live Alert Log & Comparison Feed */
    .alerts-panel {{
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .alert-feed {{
      max-height: 480px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 8px;
      padding-right: 4px;
    }}
    .alert-feed::-webkit-scrollbar {{ width: 4px; }}
    .alert-feed::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 4px; }}

    .alert-item {{
      background: var(--bg-surface-elevated);
      border-left: 3px solid var(--primary);
      padding: 10px;
      border-radius: 0 6px 6px 0;
      font-size: 11.5px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .alert-item.critical {{ border-left-color: var(--danger); background: rgba(239, 68, 68, 0.08); }}
    .alert-item.warning {{ border-left-color: var(--warning); background: rgba(245, 158, 11, 0.08); }}
    .alert-item.false-alarm {{ border-left-color: #8b5cf6; background: rgba(139, 92, 246, 0.08); }}

    .alert-top-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10.5px;
    }}
    .alert-time {{ font-family: 'JetBrains Mono', monospace; color: var(--text-dim); }}
    .alert-badge {{ font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 3px; }}
    .alert-desc {{ font-weight: 600; color: var(--text-main); }}
    .alert-meta {{ font-size: 10px; color: var(--text-muted); font-family: 'JetBrains Mono', monospace; }}

    /* Comparison Gauge Card */
    .comparison-card {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 14px;
    }}
    .metric-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      font-size: 12px;
    }}
    .metric-bar-bg {{
      background: var(--bg-base);
      height: 7px;
      border-radius: 4px;
      overflow: hidden;
      margin-top: 4px;
      border: 1px solid var(--border-color);
    }}
    .metric-bar-fill {{
      height: 100%;
      border-radius: 4px;
      transition: width 0.3s ease;
    }}

    /* Tab Content Visibility */
    .tab-content {{ display: none; }}
    .tab-content.active {{ display: block; }}

    /* Benchmark Tables */
    table.benchmark-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
      font-size: 12px;
    }}
    table.benchmark-table th, table.benchmark-table td {{
      border: 1px solid var(--border-color);
      padding: 8px 12px;
      text-align: left;
    }}
    table.benchmark-table th {{
      background: var(--bg-surface-elevated);
      color: var(--text-muted);
      font-weight: 600;
    }}
    table.benchmark-table tr:hover {{ background: rgba(255,255,255,0.02); }}

    /* Figures Grid */
    .figures-grid {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
      margin-top: 14px;
    }}
    @media (max-width: 900px) {{
      .figures-grid {{ grid-template-columns: 1fr; }}
    }}
    .figure-card {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .figure-card img {{
      width: 100%;
      border-radius: 6px;
      border: 1px solid var(--border-color);
      background: #ffffff;
    }}
    .figure-title {{
      font-size: 13px;
      font-weight: 700;
      color: var(--primary);
    }}
    .figure-caption {{
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.5;
    }}

    /* Documentation Section */
    .doc-section {{
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 14px;
      line-height: 1.6;
      font-size: 13px;
    }}
    .doc-section h3 {{
      color: var(--primary);
      font-size: 15px;
      margin-bottom: 10px;
    }}
    .formula-box {{
      background: var(--bg-base);
      border: 1px solid var(--border-color);
      padding: 10px 14px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      color: #ffd166;
      font-size: 12px;
      margin: 10px 0;
    }}
    .q-a-box {{
      border-left: 3px solid var(--primary);
      padding: 10px 14px;
      background: var(--bg-base);
      margin-bottom: 12px;
      border-radius: 0 6px 6px 0;
      border: 1px solid var(--border-color);
      border-left-width: 3px;
    }}
    .q-a-box strong {{
      color: var(--text-main);
      display: block;
      margin-bottom: 4px;
    }}
  </style>
</head>
<body>

  <!-- Top Header Navigation (Exact Original Layout Restored) -->
  <header>
    <div class="brand">
      <div class="brand-logo">
        <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      </div>
      <div class="brand-text">
        <h1>5G-Enabled Intelligent Healthcare Monitoring</h1>
        <p>URLLC Slice + Edge MEC Operations Control Center</p>
      </div>
    </div>

    <!-- Active Architecture Selector -->
    <div class="arch-switch-container">
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

    <!-- Live Telemetry Counters -->
    <div class="top-stats">
      <button id="audio-toggle" onclick="toggleAudio()">🔔 Sound: OFF</button>
      <div class="stat-pill">
        <span class="label">End-to-End Latency</span>
        <span class="val latency-good" id="top-latency">10.2 ms</span>
      </div>
      <div class="stat-pill">
        <span class="label">Uplink Offload</span>
        <span class="val" id="top-offload" style="color: var(--primary);">99.5%</span>
      </div>
      <div class="stat-pill">
        <span class="label">False Alarms</span>
        <span class="val" id="top-false-alarms" style="color: var(--success);">0</span>
      </div>
    </div>
  </header>

  <!-- Main Content Layout -->
  <main>
    <!-- Left Column: Tabs & Clinical Bed Monitors -->
    <div class="left-col">
      <div class="tabs-header">
        <div class="tab-link active" onclick="switchTab('ward-view', this)">🏥 Real-Time ICU Ward (Beds 1–4)</div>
        <div class="tab-link" onclick="switchTab('slicing-math-view', this)">📡 5G Slicing & Queue Model</div>
        <div class="tab-link" onclick="switchTab('analytics-view', this)">📊 Benchmark Tables (4, 5, 6)</div>
        <div class="tab-link" onclick="switchTab('figures-view', this)">🖼️ Publication Figures (1–4)</div>
        <div class="tab-link" onclick="switchTab('report-doc-view', this)">📑 Project Report & Viva Guide</div>
      </div>

      <!-- TAB 1: Ward View -->
      <div id="ward-view" class="tab-content active">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">
              <span class="pulse-dot"></span>
              Live Telemetry Stream — Hospital Ward A (Continuous Monitoring)
            </div>
            <div style="font-size: 11px; color: var(--text-dim); font-family: 'JetBrains Mono', monospace;">
              Sampling Rate: 1 Hz Vitals | 250 Hz ECG Sub-Channel
            </div>
          </div>

          <!-- Beds Grid -->
          <div class="beds-grid">
            <!-- Bed 1 -->
            <div class="bed-card" id="bed-card-1">
              <div class="bed-top">
                <div class="bed-id">🛏️ Bed 01 — Patient 1 (Post-Op)</div>
                <div class="bed-badge" id="badge-1">STABLE</div>
              </div>
              <div class="vitals-strip">
                <div class="vital-box hr">
                  <div class="v-label">Heart Rate</div>
                  <div class="v-val" id="hr-1">74 <span style="font-size: 10px;">bpm</span></div>
                </div>
                <div class="vital-box spo2">
                  <div class="v-label">SpO₂</div>
                  <div class="v-val" id="spo2-1">98 <span style="font-size: 10px;">%</span></div>
                </div>
                <div class="vital-box temp">
                  <div class="v-label">Latency</div>
                  <div class="v-val" id="lat-1">10.4 ms</div>
                </div>
              </div>
              <div class="canvas-container">
                <canvas id="ecg-canvas-1"></canvas>
              </div>
            </div>

            <!-- Bed 2 -->
            <div class="bed-card" id="bed-card-2">
              <div class="bed-top">
                <div class="bed-id">🛏️ Bed 02 — Patient 2 (Cardiac Care)</div>
                <div class="bed-badge" id="badge-2">STABLE</div>
              </div>
              <div class="vitals-strip">
                <div class="vital-box hr">
                  <div class="v-label">Heart Rate</div>
                  <div class="v-val" id="hr-2">82 <span style="font-size: 10px;">bpm</span></div>
                </div>
                <div class="vital-box spo2">
                  <div class="v-label">SpO₂</div>
                  <div class="v-val" id="spo2-2">97 <span style="font-size: 10px;">%</span></div>
                </div>
                <div class="vital-box temp">
                  <div class="v-label">Latency</div>
                  <div class="v-val" id="lat-2">9.8 ms</div>
                </div>
              </div>
              <div class="canvas-container">
                <canvas id="ecg-canvas-2"></canvas>
              </div>
            </div>

            <!-- Bed 3 -->
            <div class="bed-card" id="bed-card-3">
              <div class="bed-top">
                <div class="bed-id">🛏️ Bed 03 — Patient 3 (Pulmonary)</div>
                <div class="bed-badge" id="badge-3">STABLE</div>
              </div>
              <div class="vitals-strip">
                <div class="vital-box hr">
                  <div class="v-label">Heart Rate</div>
                  <div class="v-val" id="hr-3">78 <span style="font-size: 10px;">bpm</span></div>
                </div>
                <div class="vital-box spo2">
                  <div class="v-label">SpO₂</div>
                  <div class="v-val" id="spo2-3">96 <span style="font-size: 10px;">%</span></div>
                </div>
                <div class="vital-box temp">
                  <div class="v-label">Latency</div>
                  <div class="v-val" id="lat-3">10.1 ms</div>
                </div>
              </div>
              <div class="canvas-container">
                <canvas id="ecg-canvas-3"></canvas>
              </div>
            </div>

            <!-- Bed 4 -->
            <div class="bed-card" id="bed-card-4">
              <div class="bed-top">
                <div class="bed-id">🛏️ Bed 04 — Patient 4 (General Ward)</div>
                <div class="bed-badge" id="badge-4">STABLE</div>
              </div>
              <div class="vitals-strip">
                <div class="vital-box hr">
                  <div class="v-label">Heart Rate</div>
                  <div class="v-val" id="hr-4">71 <span style="font-size: 10px;">bpm</span></div>
                </div>
                <div class="vital-box spo2">
                  <div class="v-label">SpO₂</div>
                  <div class="v-val" id="spo2-4">99 <span style="font-size: 10px;">%</span></div>
                </div>
                <div class="vital-box temp">
                  <div class="v-label">Latency</div>
                  <div class="v-val" id="lat-4">10.5 ms</div>
                </div>
              </div>
              <div class="canvas-container">
                <canvas id="ecg-canvas-4"></canvas>
              </div>
            </div>
          </div>

          <!-- Interactive Simulation Injections -->
          <div class="sim-controls">
            <span style="font-size: 11px; font-weight: 700; color: var(--text-dim); align-self: center; margin-right: 4px;">
              DEMO SIMULATOR INJECTIONS:
            </span>
            <button class="action-btn btn-warning" onclick="triggerMotionArtefact(1)">
              👋 Inject Motion Artefact (Bed 1)
            </button>
            <button class="action-btn btn-danger" onclick="triggerAcuteTachycardia(2)">
              ❤️ Trigger Tachycardia (Bed 2)
            </button>
            <button class="action-btn btn-danger" onclick="triggerDesaturation(3)">
              🫁 Trigger Desaturation (Bed 3)
            </button>
            <button class="action-btn btn-primary" onclick="resetAllBeds()">
              🔄 Reset to Baselines
            </button>
          </div>
        </div>
      </div>

      <!-- TAB 2: 5G Network Slicing & Queue Model -->
      <div id="slicing-math-view" class="tab-content">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📡 5G End-to-End Latency Model & Network Slicing Queue Formulation</div>
          </div>

          <div class="doc-section">
            <h3>1. End-to-End Latency Model (Section 5.1 of Report)</h3>
            <p>For an alert packet travelling from the patient wearable gateway to the clinician screen, end-to-end latency is formulated as the sum of its deterministic and stochastic components:</p>
            <div class="formula-box">
              L = L_q + L_radio + L_transport + L_proc + L_dl + 1[lost] · L_retx
            </div>
            <p>Where:</p>
            <ul style="margin-left: 20px; margin-top: 6px;">
              <li><strong>L_q</strong>: Queueing delay at the shared cell radio resource (discrete M/G/1 queue model).</li>
              <li><strong>L_radio</strong>: Air-interface transmission time interval (TTI): 10 ms (4G) vs 5 ms (5G eMBB) vs 1.5 ms (5G URLLC).</li>
              <li><strong>L_transport</strong>: Transport network backhaul delay, modeled as log-normal: Median 30 ms (4G) vs 22 ms (eMBB) vs 2 ms (MEC edge).</li>
              <li><strong>L_proc</strong>: Server processing delay: 5 ms + Exp(mean 8 ms) in Cloud vs 3 ms + Exp(mean 2 ms) on MEC Edge.</li>
              <li><strong>L_dl</strong>: Downlink alert delivery to clinician device.</li>
              <li><strong>1[lost] · L_retx</strong>: Retransmission penalty upon packet loss (1% in 4G vs 0.001% in 5G URLLC).</li>
            </ul>
          </div>

          <div class="doc-section">
            <h3>2. 3GPP TS 23.501 Network Slicing & Scheduling Algorithm</h3>
            <p><strong>4G / 5G eMBB Baseline (FIFO):</strong> Emergency medical packets share a single queue with ordinary user background traffic (λ_bg = 1500 pkts/s). When 400 patients join, the 4G cell approaches 95% saturation, triggering queue explosion where <strong>7.68% of packets miss the 100 ms deadline</strong>.</p>
            <p style="margin-top: 8px;"><strong>5G URLLC (Dedicated Priority Slice):</strong> Medical packets obtain a dedicated logical slice. The gNodeB radio scheduler inspects the buffer and serves medical telemetry ahead of waiting background packets, eliminating queue build-up completely:</p>
            <div class="formula-box">
              // Core scheduling loop implemented in healthcare5g/network.py:
              while im < nm:
                  if med[im] <= t:
                      t += svm[im]; d[im] = t - med[im]; im += 1
                  elif ib < nb and bg[ib] <= t:
                      t += svb[ib]; ib += 1
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 3: Experimental Benchmarks -->
      <div id="analytics-view" class="tab-content">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📈 5G Performance Metrics (Reproduction of Report Tables 4, 5, 6)</div>
          </div>

          <!-- Table 4 Display -->
          <h4 style="font-size: 13px; color: var(--primary); margin-top: 6px;">Table 4: Anomaly Detection Quality (100 Patients × 12 Hours, 361 True Events)</h4>
          <table class="benchmark-table">
            <thead>
              <tr>
                <th>Detection Scheme</th>
                <th>Events Detected</th>
                <th>Recall</th>
                <th>Alarms Raised</th>
                <th>False Alarms</th>
                <th>FA / Patient-Day</th>
                <th>Mean Delay</th>
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
                <td>7.0 s (Persistence)</td>
              </tr>
            </tbody>
          </table>
          <p style="font-size: 11px; color: var(--text-muted); margin-top: 6px;">
            * <strong>Takeaway:</strong> Fixed limits generate catastrophic alarm fatigue (281 false alarms/day) caused by benign motion artefacts. The proposed EWMA filter with 8/10 sample persistence completely eliminated false alarms (0 false alarms).
          </p>

          <!-- Table 5 Display -->
          <h4 style="font-size: 13px; color: var(--primary); margin-top: 18px;">Table 5: End-to-End Latency Under Busy-Hour Congestion (400 Monitored Patients)</h4>
          <table class="benchmark-table">
            <thead>
              <tr>
                <th>Architecture</th>
                <th>Mean Latency</th>
                <th>95th Percentile</th>
                <th>99th Percentile</th>
                <th>Miss &gt; 100 ms Target</th>
                <th>Miss &gt; 20 ms Target</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>A: 4G + Cloud (FIFO, Shared Cell)</td>
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
              <tr style="background: rgba(14, 165, 233, 0.08);">
                <td style="color: var(--primary); font-weight: 700;">C: 5G URLLC + MEC (Proposed Priority Slice)</td>
                <td>10.2 ms</td>
                <td>14.3 ms</td>
                <td style="color: var(--success); font-weight: 700;">17.5 ms</td>
                <td style="color: var(--success); font-weight: 700;">0.00%</td>
                <td>0.28%</td>
              </tr>
            </tbody>
          </table>
          <p style="font-size: 11px; color: var(--text-muted); margin-top: 6px;">
            * <strong>Takeaway:</strong> 4G fails under busy-hour load. 5G eMBB cannot satisfy a 20 ms strict target due to cloud WAN transit. Only 5G URLLC + MEC guarantees deterministic delivery (P99 = 17.5 ms).
          </p>

          <!-- Table 6 Display -->
          <h4 style="font-size: 13px; color: var(--primary); margin-top: 18px;">Table 6: Uplink Data Minimization (Edge Pre-Processing)</h4>
          <table class="benchmark-table">
            <thead>
              <tr>
                <th>Transmission Approach</th>
                <th>Daily Uplink Data / Patient</th>
                <th>Relative Uplink Bandwidth</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Cloud-Centric (Continuous 250 Hz Raw Stream)</td>
                <td>53.9 MB</td>
                <td>100%</td>
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

      <!-- TAB 4: Publication Figures (High-Res Base64 Embedded) -->
      <div id="figures-view" class="tab-content">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">🖼️ Official Publication Figures (Embedded High-Resolution)</div>
          </div>

          <div class="figures-grid">
            <!-- Figure 1 -->
            <div class="figure-card">
              <div class="figure-title">Figure 1: Proposed 5G System Topology (3GPP TS 23.501)</div>
              <img src="data:image/png;base64,{fig1_b64}" alt="Figure 1: 5G System Architecture">
              <div class="figure-caption">
                Wearable sensors stream to patient gateway (5G UE) over URLLC dedicated priority slice. The packet terminates directly at co-located UPF and hospital MEC host, avoiding public cloud transit.
              </div>
            </div>

            <!-- Figure 2 -->
            <div class="figure-card">
              <div class="figure-title">Figure 2: Fixed vs Adaptive Anomaly Detection Trace</div>
              <img src="data:image/png;base64,{fig2_b64}" alt="Figure 2: Detection Comparison">
              <div class="figure-caption">
                Demonstrates how a 2-second motion artefact triggers a false alarm in the fixed limit detector, whereas the proposed EWMA baseline filter with 8/10 persistence correctly suppresses it.
              </div>
            </div>

            <!-- Figure 3 -->
            <div class="figure-card">
              <div class="figure-title">Figure 3: Cumulative Distribution Function (CDF) of Latency</div>
              <img src="data:image/png;base64,{fig3_b64}" alt="Figure 3: Latency CDF">
              <div class="figure-caption">
                Empirical CDF for 400 patients in the busy hour. Demonstrates the steep deterministic profile of 5G URLLC+MEC (all packets &lt; 25 ms) compared to the long tail of 4G (+120 ms).
              </div>
            </div>

            <!-- Figure 4 -->
            <div class="figure-card">
              <div class="figure-title">Figure 4: 99th-Percentile Latency vs. Patient Scale</div>
              <img src="data:image/png;base64,{fig4_b64}" alt="Figure 4: P99 Tail Latency vs Monitored Patients">
              <div class="figure-caption">
                P99 tail latency plotted against cell density (50 to 400 patients). 5G curves remain flat, while 4G degrades towards saturation.
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB 5: Project Report & Academic Credentials -->
      <div id="report-doc-view" class="tab-content">
        <div class="panel">
          <div class="panel-header">
            <div class="panel-title">📑 Academic Project Report & Viva Defense Guide</div>
          </div>

          <div class="doc-section">
            <h3>Academic Credentials & Project Overview</h3>
            <p><strong>Project Title:</strong> 5G-Enabled Intelligent Healthcare Monitoring</p>
            <p><strong>Students:</strong> Dudekula Sai Charan (1NT24CS091) & Harshith D Raj (1NT24CS103)</p>
            <p><strong>Project Guide:</strong> Mr. Shivaputra Panchal, Assistant Professor, Dept. of CSE</p>
            <p><strong>Institution:</strong> Nitte Meenakshi Institute of Technology, Yelahanka, Bengaluru - 560064</p>
            <p><strong>Academic Year:</strong> 2026–2027 (Bachelor of Engineering in Computer Science and Engineering)</p>
            <p style="margin-top: 10px;"><strong>Abstract:</strong> Remote patient monitoring requires reliable, ultra-low-latency alert delivery while avoiding clinician alarm fatigue. Traditional 4G and cloud backbones experience unpredictable queueing delays and long WAN round-trips. This project designs, evaluates, and demonstrates an end-to-end monitoring pipeline combining a 3GPP TS 23.501 5G URLLC priority slice, co-located Multi-access Edge Computing (MEC), and a patient-specific adaptive EWMA anomaly detector. Across 100 simulated patients over 12 hours, the proposed architecture delivers alerts in 10.2 ms mean (17.5 ms P99) with 0% deadline misses, reduces false alarms from 281 to 0 per patient-day, and cuts daily uplink data volume by 99.5%.</p>
          </div>

          <div class="doc-section">
            <h3>Top 5 Viva Defense Questions & Answers</h3>

            <div class="q-a-box">
              <strong>Q1: Why is 5G URLLC required instead of standard 4G or 5G eMBB?</strong>
              <em>Answer:</em> 4G operates with shared FIFO queues that degrade under congestion (Table 5 shows 7.68% packets miss the 100 ms target at 400 patients). 5G eMBB offers high bandwidth but routes over the public internet to distant clouds (median 22 ms transport), causing 100% of packets to miss strict 20 ms URLLC deadlines. Only 5G URLLC with priority slicing and edge MEC achieves deterministic sub-20ms delivery.
            </div>

            <div class="q-a-box">
              <strong>Q2: How does the network slicing prioritize healthcare traffic?</strong>
              <em>Answer:</em> Under 3GPP TS 23.501, healthcare traffic is assigned a dedicated logical slice configured for non-preemptive priority queueing at the gNodeB radio scheduler. As implemented in <code>healthcare5g/network.py</code>, medical packets jump to the head of the radio buffer ahead of background broadband packets, making alert delivery independent of cell load.
            </div>

            <div class="q-a-box">
              <strong>Q3: How does your adaptive anomaly detector eliminate false alarms?</strong>
              <em>Answer:</em> It maintains personal baselines using Exponentially Weighted Moving Averages (EWMA) with memory α = 1/1800 (~30 min). Alerts require both a z-score deviation (|z| &gt; 4.0) and an 8-out-of-10 sample persistence filter. Brief sensor motion artefacts (1–3s spikes) fail the persistence filter and are suppressed, avoiding alarm fatigue.
            </div>

            <div class="q-a-box">
              <strong>Q4: Why does MEC provide a 99.5% uplink bandwidth reduction?</strong>
              <em>Answer:</em> In cloud-centric systems, continuous 250 Hz raw ECG must be streamed outside the hospital (53.9 MB/patient-day). With MEC, feature extraction happens on-premise at the edge node; only 1-minute summaries and 30-second clips around confirmed alerts are sent out (0.25 MB/patient-day), saving bandwidth and preserving patient privacy under DPDP 2023.
            </div>

            <div class="q-a-box">
              <strong>Q5: What are the limitations and future scope of this project?</strong>
              <em>Answer:</em> Current validation uses synthetic vitals, representative delay distributions, and a single cell without user mobility. Future work includes evaluating on PhysioNet clinical databases, protocol-level ns-3/5G-LENA simulations, and hardware SDR testbeds (Open5GS + srsRAN).
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Column: Live Clinical Alert Feed & Slicing Comparison -->
    <div class="alerts-panel">
      <!-- Live Comparison Card -->
      <div class="comparison-card">
        <div style="font-size: 11px; font-weight: 700; color: var(--text-dim); text-transform: uppercase; margin-bottom: 6px;">
          Active Network Profile: <span id="current-arch-name" style="color: var(--primary);">5G URLLC Slice + MEC</span>
        </div>

        <div class="metric-row">
          <span style="color: var(--text-muted);">Mean Radio+Transport Latency</span>
          <span id="metric-lat" style="font-weight: 700; font-family: 'JetBrains Mono', monospace; color: var(--success);">10.2 ms</span>
        </div>
        <div class="metric-bar-bg">
          <div id="bar-lat" class="metric-bar-fill" style="width: 14%; background: var(--success);"></div>
        </div>

        <div class="metric-row" style="margin-top: 10px;">
          <span style="color: var(--text-muted);">Queueing Discipline</span>
          <span id="metric-queue" style="font-weight: 700; color: var(--primary);">Priority Slice</span>
        </div>

        <div class="metric-row" style="margin-top: 6px;">
          <span style="color: var(--text-muted);">Uplink Bandwidth Saved</span>
          <span id="metric-bw" style="font-weight: 700; color: var(--success);">99.5%</span>
        </div>
      </div>

      <!-- Real-Time Alerts Feed -->
      <div class="panel" style="flex: 1; display: flex; flex-direction: column;">
        <div class="panel-header" style="margin-bottom: 8px;">
          <div class="panel-title">🚨 Clinical Alert Feed</div>
          <button style="background: none; border: none; color: var(--text-dim); font-size: 11px; cursor: pointer;" onclick="clearAlerts()">Clear</button>
        </div>
        <div class="alert-feed" id="alert-feed">
          <div class="alert-item">
            <div class="alert-top-row">
              <span class="alert-time">ONLINE</span>
              <span class="alert-badge" style="background: rgba(14, 165, 233, 0.2); color: var(--primary);">SYSTEM READY</span>
            </div>
            <div class="alert-desc">5G URLLC Medical Slice Connected</div>
            <div class="alert-meta">MEC Anomaly Detector Active • EWMA α=1/1800</div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    // Audio synthesizer for clinical alarms
    let audioCtx = null;
    let audioEnabled = false;

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

    // Architecture State
    let currentArch = 'C';
    const ARCH_SPECS = {{
      'A': {{ name: '4G + Cloud', latMean: '74.7 ms', p99: '123.4 ms', latVal: 74.7, color: 'var(--danger)', queue: 'FIFO (Shared 4G)', offload: '0% (Raw Stream)' }},
      'B': {{ name: '5G eMBB + Cloud', latMean: '46.2 ms', p99: '79.4 ms', latVal: 46.2, color: 'var(--warning)', queue: 'FIFO (5G Radio)', offload: '0% (Raw Stream)' }},
      'C': {{ name: '5G URLLC Slice + MEC', latMean: '10.2 ms', p99: '17.5 ms', latVal: 10.2, color: 'var(--success)', queue: 'Non-Preemptive Priority Slice', offload: '99.5% (Summaries Only)' }}
    }};

    function setArchitecture(key) {{
      currentArch = key;
      document.querySelectorAll('.arch-btn').forEach(btn => btn.classList.remove('active'));
      const activeBtn = document.querySelector(`.arch-${{key.toLowerCase()}}`);
      if (activeBtn) activeBtn.classList.add('active');

      const spec = ARCH_SPECS[key];
      document.getElementById('current-arch-name').innerText = spec.name;
      document.getElementById('current-arch-name').style.color = spec.color;
      document.getElementById('top-latency').innerText = spec.latMean;
      document.getElementById('top-latency').className = `val ${{key === 'C' ? 'latency-good' : (key === 'B' ? 'latency-med' : 'latency-bad')}}`;
      document.getElementById('metric-lat').innerText = spec.latMean;
      document.getElementById('metric-lat').style.color = spec.color;
      document.getElementById('metric-queue').innerText = spec.queue;
      document.getElementById('metric-bw').innerText = spec.offload;

      const barPct = Math.min(100, (spec.latVal / 125) * 100);
      document.getElementById('bar-lat').style.width = `${{barPct}}%`;
      document.getElementById('bar-lat').style.background = spec.color;

      for (let i = 1; i <= 4; i++) {{
        const jitter = (Math.random() * 2 - 1).toFixed(1);
        document.getElementById(`lat-${{i}}`).innerText = `${{(spec.latVal + parseFloat(jitter)).toFixed(1)}} ms`;
        document.getElementById(`lat-${{i}}`).style.color = spec.color;
      }}

      addAlert('INFO', `Switched network architecture to ${{spec.name}}`, `Radio queue discipline: ${{spec.queue}}`);
    }}

    // Tab Navigation
    function switchTab(tabId, tabElem) {{
      document.querySelectorAll('.tab-link').forEach(l => l.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      if (tabElem) tabElem.classList.add('active');
      const target = document.getElementById(tabId);
      if (target) target.classList.add('active');
    }}

    // Patient State Simulator
    const patients = {{
      1: {{ hr: 74, spo2: 98, status: 'STABLE', baselineHr: 74, baselineSpo2: 98 }},
      2: {{ hr: 82, spo2: 97, status: 'STABLE', baselineHr: 82, baselineSpo2: 97 }},
      3: {{ hr: 78, spo2: 96, status: 'STABLE', baselineHr: 78, baselineSpo2: 96 }},
      4: {{ hr: 71, spo2: 99, status: 'STABLE', baselineHr: 71, baselineSpo2: 99 }}
    }};

    // Authentic Clinical ECG Canvas
    const canvases = [1, 2, 3, 4].map(id => {{
      const c = document.getElementById(`ecg-canvas-${{id}}`);
      c.width = c.parentElement.clientWidth;
      c.height = c.parentElement.clientHeight;
      return {{ id, canvas: c, ctx: c.getContext('2d'), points: [] }};
    }});

    let tick = 0;
    function renderECG() {{
      tick++;
      canvases.forEach(obj => {{
        const p = patients[obj.id];
        const ctx = obj.ctx;
        const w = obj.canvas.width;
        const h = obj.canvas.height;

        const heartRate = p.hr;
        const period = Math.max(15, Math.floor(60 / (heartRate / 60)));
        const phase = tick % period;

        let yOffset = 0;
        if (phase === 0) yOffset = -5;
        else if (phase === 2) yOffset = 4;
        else if (phase === 3) yOffset = -26;
        else if (phase === 4) yOffset = 8;
        else if (phase === 7) yOffset = -7;

        yOffset += (Math.random() - 0.5) * 1.5;

        const currentY = (h / 2) + yOffset;
        obj.points.push(currentY);
        if (obj.points.length > w) obj.points.shift();

        // Background & subtle grid
        ctx.fillStyle = '#060b14';
        ctx.fillRect(0, 0, w, h);

        ctx.lineWidth = 0.5;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
        ctx.beginPath();
        for (let x = 0; x < w; x += 15) {{
          ctx.moveTo(x, 0);
          ctx.lineTo(x, h);
        }}
        for (let y = 0; y < h; y += 15) {{
          ctx.moveTo(0, y);
          ctx.lineTo(w, y);
        }}
        ctx.stroke();

        ctx.fillStyle = 'rgba(148, 163, 184, 0.4)';
        ctx.font = '8px "JetBrains Mono", monospace';
        ctx.fillText('LEAD II · 25mm/s', 8, 12);

        // ECG Trace
        ctx.strokeStyle = p.status === 'CRITICAL' ? '#ef4444' : '#22c55e';
        ctx.lineWidth = 1.4;
        ctx.beginPath();
        for (let i = 0; i < obj.points.length; i++) {{
          if (i === 0) ctx.moveTo(i, obj.points[i]);
          else ctx.lineTo(i, obj.points[i]);
        }}
        ctx.stroke();

        // Cursor
        const headX = obj.points.length - 1;
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(headX, currentY, 2, 0, Math.PI * 2);
        ctx.fill();
      }});

      requestAnimationFrame(renderECG);
    }}
    requestAnimationFrame(renderECG);

    // Alert Logger
    let falseAlarmCount = 0;
    function addAlert(priority, title, meta) {{
      const feed = document.getElementById('alert-feed');
      const item = document.createElement('div');
      item.className = `alert-item ${{priority.toLowerCase()}}`;
      const now = new Date();
      const timeStr = now.toTimeString().split(' ')[0];

      let badgeBg = 'rgba(14, 165, 233, 0.2)';
      let badgeColor = 'var(--primary)';
      if (priority === 'CRITICAL') {{
        badgeBg = 'rgba(239, 68, 68, 0.25)';
        badgeColor = '#fca5a5';
        playBeep(920, 0.25);
      }} else if (priority === 'WARNING') {{
        badgeBg = 'rgba(245, 158, 11, 0.25)';
        badgeColor = '#fde68a';
        playBeep(660, 0.15);
      }} else if (priority === 'FALSE') {{
        badgeBg = 'rgba(139, 92, 246, 0.2)';
        badgeColor = '#a78bfa';
        falseAlarmCount++;
        document.getElementById('top-false-alarms').innerText = falseAlarmCount;
      }}

      item.innerHTML = `
        <div class="alert-top-row">
          <span class="alert-time">${{timeStr}}</span>
          <span class="alert-badge" style="background: ${{badgeBg}}; color: ${{badgeColor}};">${{priority}}</span>
        </div>
        <div class="alert-desc">${{title}}</div>
        <div class="alert-meta">${{meta}}</div>
      `;
      feed.insertBefore(item, feed.firstChild);
    }}

    function clearAlerts() {{
      document.getElementById('alert-feed').innerHTML = '';
      falseAlarmCount = 0;
      document.getElementById('top-false-alarms').innerText = '0';
    }}

    function triggerMotionArtefact(bedId) {{
      const p = patients[bedId];
      const origHr = p.hr;
      p.hr = 138;
      document.getElementById(`hr-${{bedId}}`).innerText = `${{p.hr}} bpm`;
      document.getElementById(`bed-card-${{bedId}}`).classList.add('alarm-false');

      addAlert('FALSE', `Fixed Limit Alarm: Bed ${{bedId}} HR Spike (${{p.hr}} bpm)`, 
               `Fixed detector tripped on 2s motion artefact. Adaptive EWMA detector: SUPPRESSED (persistence 2/10 &lt; 8).`);

      setTimeout(() => {{
        p.hr = origHr;
        document.getElementById(`hr-${{bedId}}`).innerText = `${{p.hr}} bpm`;
        document.getElementById(`bed-card-${{bedId}}`).classList.remove('alarm-false');
      }}, 2500);
    }}

    function triggerAcuteTachycardia(bedId) {{
      const p = patients[bedId];
      p.status = 'CRITICAL';
      p.hr = 142;
      document.getElementById(`hr-${{bedId}}`).innerText = `${{p.hr}} bpm`;
      document.getElementById(`badge-${{bedId}}`).innerText = 'CRITICAL TACHYCARDIA';
      document.getElementById(`badge-${{bedId}}`).className = 'bed-badge critical';
      document.getElementById(`bed-card-${{bedId}}`).classList.add('alarm-critical');

      addAlert('CRITICAL', `EMERGENCY ALERT: Bed ${{bedId}} Acute Tachycardia (${{p.hr}} bpm)`, 
               `Confirmed by 8/10 persistence rule! Delivered over ${{ARCH_SPECS[currentArch].name}} in ${{document.getElementById(`lat-${{bedId}}`).innerText}}`);
    }}

    function triggerDesaturation(bedId) {{
      const p = patients[bedId];
      p.status = 'CRITICAL';
      p.spo2 = 86;
      document.getElementById(`spo2-${{bedId}}`).innerText = `${{p.spo2}} %`;
      document.getElementById(`badge-${{bedId}}`).innerText = 'HYPOXEMIC DESATURATION';
      document.getElementById(`badge-${{bedId}}`).className = 'bed-badge critical';
      document.getElementById(`bed-card-${{bedId}}`).classList.add('alarm-critical');

      addAlert('CRITICAL', `EMERGENCY ALERT: Bed ${{bedId}} SpO2 Desaturation (${{p.spo2}}%)`, 
               `Confirmed by z-score deviation &lt; -4.0. Delivered over ${{ARCH_SPECS[currentArch].name}} in ${{document.getElementById(`lat-${{bedId}}`).innerText}}`);
    }}

    function resetAllBeds() {{
      for (let i = 1; i <= 4; i++) {{
        const p = patients[i];
        p.status = 'STABLE';
        p.hr = p.baselineHr;
        p.spo2 = p.baselineSpo2;
        document.getElementById(`hr-${{i}}`).innerText = `${{p.hr}} bpm`;
        document.getElementById(`spo2-${{i}}`).innerText = `${{p.spo2}} %`;
        document.getElementById(`badge-${{i}}`).innerText = 'STABLE';
        document.getElementById(`badge-${{i}}`).className = 'bed-badge';
        document.getElementById(`bed-card-${{i}}`).classList.remove('alarm-critical', 'alarm-false');
      }}
      addAlert('INFO', 'All hospital beds restored to normal baseline', 'Continuous EWMA monitoring active.');
    }}
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

print(f"Restored sleek top bar successfully:")
print(f"1. {sub_path} ({len(html_content)} bytes)")
print(f"2. {index_path} ({len(html_content)} bytes)")
