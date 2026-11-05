import sys, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    DARK_NAVY = RGBColor(11, 27, 63)      # #0B1B3F
    ACCENT_BLUE = RGBColor(31, 78, 168)   # #1F4EA8
    TEAL = RGBColor(14, 165, 160)         # #0EA5A0
    LIGHT_BG = RGBColor(246, 248, 252)    # #F6F8FC
    WHITE = RGBColor(255, 255, 255)
    TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    CARD_BG = RGBColor(255, 255, 255)
    CARD_BORDER = RGBColor(226, 232, 240)
    ALERT_RED = RGBColor(225, 29, 72)
    GREEN = RGBColor(22, 163, 74)

    def add_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = LIGHT_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="5G-ENABLED INTELLIGENT HEALTHCARE MONITORING"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.4))
        p = cat_box.text_frame.paragraphs[0]
        p.text = category_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEAL

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        p2 = title_box.text_frame.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = DARK_NAVY

    # ==================== SLIDE 1: TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_NAVY
    bg1.line.fill.background()

    # Title Banner Box
    t_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "5G-Enabled Intelligent Healthcare Monitoring"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT

    p_sub = tf.add_paragraph()
    p_sub.text = "End-to-End Latency Guarantees, Edge Anomaly Detection & Network Slicing"
    p_sub.font.size = Pt(18)
    p_sub.font.color.rgb = TEAL
    p_sub.space_before = Pt(12)

    # Details Cards
    def add_meta_card(slide, x, y, w, h, header, lines):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(19, 39, 87)
        card.line.color.rgb = RGBColor(45, 75, 140)
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = header
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL
        for l in lines:
            pl = tf.add_paragraph()
            pl.text = l
            pl.font.size = Pt(12)
            pl.font.color.rgb = WHITE
            pl.space_before = Pt(4)

    add_meta_card(s1, Inches(1.0), Inches(4.3), Inches(3.6), Inches(2.2), "PRESENTED BY", 
                  ["Dudekula Sai Charan (1NT24CS091)", "Harshith D Raj (1NT24CS103)", "B.E. Computer Science & Engg."])
    add_meta_card(s1, Inches(4.8), Inches(4.3), Inches(3.6), Inches(2.2), "UNDER THE GUIDANCE OF", 
                  ["Mr. Shivaputra Panchal", "Assistant Professor", "Dept. of CSE, NMIT, Bengaluru"])
    add_meta_card(s1, Inches(8.6), Inches(4.3), Inches(3.7), Inches(2.2), "ACADEMIC YEAR & DOMAIN", 
                  ["Academic Year: 2026-27", "Core Subject: 5G & Mobile Networks", "Focus: URLLC, MEC & Edge AI"])

    # ==================== SLIDE 2: PROBLEM STATEMENT ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "The Remote Patient Monitoring Dilemma")

    def add_card(slide, x, y, w, h, title, items, tag=""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        tf = card.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        if tag:
            p_tag = tf.add_paragraph()
            p_tag.text = tag
            p_tag.font.size = Pt(10)
            p_tag.font.bold = True
            p_tag.font.color.rgb = TEAL
            p_tag.space_before = Pt(2)
        for it in items:
            p2 = tf.add_paragraph()
            p2.text = "• " + it
            p2.font.size = Pt(11)
            p2.font.color.rgb = TEXT_DARK
            p2.space_before = Pt(6)

    add_card(s2, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "1. Strict Latency Bottleneck",
             ["Critical cardiac/hypoxemic alerts must reach medical staff within a strict deadline (<100 ms target, <20 ms strict).",
              "Traditional 4G links route every packet across public internet backbones to distant cloud servers.",
              "Latency fluctuates unpredictably with public cell traffic and congestion."],
             "NETWORK CHALLENGE")

    add_card(s2, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "2. Clinical Alarm Fatigue",
             ["Standard monitors use fixed thresholds (e.g., HR > 100 bpm, SpO2 < 92%).",
              "Harmless motion artefacts (wrist movement, shifting) produce massive false alarms.",
              "In clinical wards, ~281 false alarms per patient-day desensitize nursing staff to real emergencies."],
             "ANALYTICS CHALLENGE")

    add_card(s2, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "3. Cloud Bandwidth & Privacy",
             ["Streaming continuous raw waveforms (250 Hz ECG + vitals) consumes ~54 MB per patient-day.",
              "Hundreds of patients saturate hospital uplink capacity.",
              "Transmitting uncurated raw physiological signals across public networks poses regulatory & privacy concerns."],
             "ARCHITECTURAL CHALLENGE")

    # ==================== SLIDE 3: 5G ENABLERS ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "How 5G Enablers Address the Challenges")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "URLLC Air Interface",
             ["Mini-slot scheduling and sub-1 ms transmission time intervals (TTIs).",
              "Dedicated 5G radio resource configuration guarantees sub-2 ms radio access delay.",
              "Essential for zero-deadline-miss delivery of critical medical alarms."],
             "3GPP SERVICE CLASS")

    add_card(s3, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "Network Slicing",
             ["Logical isolation on shared physical RAN infrastructure.",
              "Medical telemetry is assigned a Non-Preemptive Priority Slice.",
              "Protects patient traffic from queuing delays caused by high-bandwidth public mobile traffic."],
             "CORE VIRTUALIZATION")

    add_card(s3, Inches(8.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "Edge Computing (MEC)",
             ["UPF (User Plane Function) co-located at hospital edge server.",
              "Eliminates 30+ ms cloud transport round-trip.",
              "Runs adaptive analytics locally; only 1-minute summaries & alert clips leave the hospital."],
             "TOPOLOGY SHIFT")

    # ==================== SLIDE 4: ARCHITECTURE ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "Proposed End-to-End System Architecture (Figure 1)")

    # Architecture stages visual
    stages = [
        ("Tier 1: Patient Hub", "Wearable Sensors\n(ECG, HR, SpO2)\n+\n5G Gateway UE", Inches(0.8)),
        ("Tier 2: 5G RAN", "gNodeB Base Station\nURLLC Priority Slice\n(Dedicated QoS)", Inches(3.8)),
        ("Tier 3: Hospital Edge", "UPF + MEC Server\n• Pre-processing\n• Adaptive Detector\n• Alert Manager", Inches(6.8)),
        ("Tier 4: Clinical Interface", "Hospital EHR\n+\nClinician Web Dashboard\n(Real-Time Pushes)", Inches(9.8))
    ]
    for title, desc, x in stages:
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.7), Inches(2.7), Inches(2.3))
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = ACCENT_BLUE
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(8)

    # Explanation card below
    add_card(s4, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5),
             "Key Architectural Differentiators (4G Cloud vs 5G URLLC+MEC)",
             ["4G Baseline: Packets wait in a shared FIFO queue with 1,500 pkt/s background traffic, followed by 30 ms cloud transport jitter.",
              "5G Proposed: Medical packets jump to the head of the radio queue (Non-preemptive priority slice) and terminate at the local hospital MEC node (2 ms median transport).",
              "Data Reduction: MEC edge filters reduce raw stream from 53.9 MB/patient-day to 0.25 MB/patient-day (>99.5% reduction)."])

    # ==================== SLIDE 5: METHODOLOGY - ADAPTIVE DETECTOR ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "Adaptive Anomaly Detection Algorithm")

    add_card(s5, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Mathematical Formulation",
             ["1. Personal Baseline Tracking (EWMA):\n   μ(t) = μ(t−1) + α · [ x(t) − μ(t−1) ]\n   (Memory window ~30 minutes with α = 1/1800)",
              "2. Personal Noise Normalization:\n   σ²(t) = (1−α)·σ²(t−1) + α·[x(t) − μ(t−1)]²\n   z(t) = [ x(t) − μ(t−1) ] / σ(t)",
              "3. Anomaly Z-Score Scoring:\n   Flagged if |z| > 4.0 (HR) or z < −4.0 (SpO2)",
              "4. Persistence Filter (The Artefact Killer):\n   Alert raised ONLY if 8 of the last 10 samples are abnormal!"],
             "FORMULATION (SEC 5.2)")

    add_card(s5, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Why It Eliminates False Alarms",
             ["Patient-Centric: Evaluates deviations relative to the individual's baseline, not an arbitrary population cut-off.",
              "Motion Resistance: A 2-second movement spike triggers at most 2 flagged samples; the 8-of-10 persistence filter completely ignores it.",
              "Clinical Trade-off: Introduces a modest ~7 second evaluation delay in exchange for wiping out 14,052 false alarms.",
              "Dual Implementation: Verified via both vectorized batch processing and sample-by-sample StreamingAdaptive edge classes."],
             "CLINICAL ADVANTAGE")

    # ==================== SLIDE 6: RESULTS - TABLE 4 ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "Experimental Results: Anomaly Detection (Table 4)")

    # Table creation
    rows, cols = 3, 7
    left, top, width, height = Inches(0.8), Inches(1.7), Inches(11.7), Inches(2.2)
    tbl_shape = s6.shapes.add_table(rows, cols, left, top, width, height)
    tbl = tbl_shape.table

    headers = ["Alarm Scheme", "Events Detected", "Recall", "Alarms Raised", "False Alarms", "FA / Pt-Day", "Mean Delay"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    data = [
        ["Fixed Threshold", "359 / 361", "99.4 %", "14,403", "14,052", "281.0", "0.5 s"],
        ["Adaptive (Proposed)", "344 / 361", "95.3 %", "341", "0", "0.0", "7.0 s"]
    ]
    for r_idx, r_data in enumerate(data):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx == 0 else RGBColor(235, 248, 245)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(12)
            p.font.color.rgb = ALERT_RED if (r_idx==0 and c_idx==4) else (GREEN if (r_idx==1 and c_idx==4) else TEXT_DARK)
            p.font.bold = (c_idx == 0 or c_idx == 4)

    add_card(s6, Inches(0.8), Inches(4.3), Inches(11.7), Inches(2.5),
             "Key Takeaways from Table 4",
             ["Fixed Thresholds generate catastrophic alarm fatigue: 281 false alarms per patient-day would overwhelm hospital staff.",
              "The Proposed Adaptive Detector achieved 100% Precision (0 false alarms) on the 100-patient, 12-hour cohort.",
              "High Clinical Sensitivity: Caught 95.3% of all genuine acute events (both tachycardia and hypoxemic desaturation).",
              "Demonstrates Figure 2 in practice: Spikes from motion are suppressed, while prolonged clinical deteriorations are confirmed."])

    # ==================== SLIDE 7: RESULTS - TABLE 5 ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "Experimental Results: Alert Latency (Table 5)")

    rows, cols = 4, 6
    tbl_shape2 = s7.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(11.7), Inches(2.5))
    tbl2 = tbl_shape2.table

    headers2 = ["Architecture", "Mean Latency", "95th Percentile", "99th Percentile", "Miss >100 ms Target", "Miss >20 ms Target"]
    for i, h in enumerate(headers2):
        cell = tbl2.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE

    data2 = [
        ["A: 4G + Cloud", "74.7 ms", "105.2 ms", "123.4 ms", "7.68 %", "100.00 %"],
        ["B: 5G eMBB + Cloud", "46.2 ms", "66.3 ms", "79.4 ms", "0.07 %", "100.00 %"],
        ["C: 5G URLLC + MEC (Proposed)", "10.2 ms", "14.3 ms", "17.5 ms", "0.00 %", "0.28 %"]
    ]
    for r_idx, r_data in enumerate(data2):
        for c_idx, val in enumerate(r_data):
            cell = tbl2.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(254, 242, 242) if r_idx==0 else (WHITE if r_idx==1 else RGBColor(236, 253, 245))
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(12)
            p.font.color.rgb = GREEN if (r_idx==2 and c_idx>=1) else (ALERT_RED if (r_idx==0 and c_idx==4) else TEXT_DARK)
            p.font.bold = (r_idx == 2 or c_idx == 0)

    add_card(s7, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.3),
             "Latency Analysis Under Peak Busy-Hour Load (400 Monitored Patients)",
             ["4G Failure: Under heavy cell traffic, 4G p99 latency climbs to 123.4 ms, violating the 100 ms emergency deadline for 7.68% of packets.",
              "5G eMBB Insufficiency: While faster radio helps average delay, cloud round-trip prevents eMBB from ever hitting strict 20 ms targets (100% miss).",
              "5G URLLC + MEC Dominance: Delivers a p99 latency of 17.5 ms with ZERO misses of the 100 ms target, guaranteeing deterministic QoS."])

    # ==================== SLIDE 8: RESULTS - TABLE 6 ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "Bandwidth Optimization & Edge Filtering (Table 6)")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Uplink Data Volume Comparison",
             ["Cloud-Centric (Continuous Streaming):\n   • 250 Hz ECG (2 bytes/sample) + vitals\n   • 53.9 MB per patient per day\n   • Saturates hospital internet uplinks when scaling to wards with 100+ beds.",
              "Edge-Filtered (5G URLLC + MEC):\n   • 1-minute summary packets (100 bytes)\n   • 30-second full ECG clips ONLY when alarm triggers\n   • 0.25 MB per patient per day",
              "Overall Reduction: 99.54% saving in external network transmission."],
             "TABLE 6 BENCHMARK")

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Clinical & Economic Implications",
             ["Cost Efficiency: Over 99% reduction in recurring cloud ingress data transfer and storage costs.",
              "Bandwidth Conservation: Frees up cellular radio capacity for other life-critical devices and telemedicine video consultations.",
              "Data Sovereignty & Security: Raw biometric waveforms never leave the hospital premises, directly complying with India's DPDP Act 2023 & HIPAA.",
              "Fast Retrieval: Clinicians receive high-resolution waveforms precisely when an anomaly occurs."],
             "SYSTEM BENEFITS")

    # ==================== SLIDE 9: LIVE PROTOTYPE WALKTHROUGH ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "Live Prototype & Clinician Dashboard Demonstration")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Software Implementation Details",
             ["100% Python Architecture (NumPy, SciPy, Matplotlib).",
              "Fully Reproducible: Fixed random seeds allow complete mathematical verification via check.py.",
              "Modular Subsystems:\n  • vitals.py: Cohort synthesis with AR(1) drift\n  • detectors.py: Dual EWMA & streaming state machine\n  • network.py: Discrete-event M/M/1 priority queue\n  • pipeline.py: End-to-end multi-tier pipeline simulator",
              "Outputs interactive clinician dashboards and publication figures."],
             "ARCHITECTURE CODEBASE")

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Live Dashboard Features (HTML / Web App)",
             ["Multi-Patient ECG & Vital Trace View: Displays live waveform telemetry across hospital beds.",
              "Real-Time Alert Feed: Highlights event time, patient ID, abnormal parameter, priority level, and transmission latency.",
              "Ground Truth Cross-Check: Automatically cross-references alerts against simulated true clinical events.",
              "Dynamic Architecture Comparison: Instantly inspect telemetry under 4G, 5G eMBB, and 5G URLLC configurations."],
             "DEMO UI OVERVIEW")

    # ==================== SLIDE 10: VIVA DEFENSE FAQ ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "Critical Technical & Viva Defense Points")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Real Implementation vs Simulation Scope",
             ["Question: Is this running on physical 5G base stations?",
              "Answer: No. As explicitly documented in Section 7.1 and 12, physical 5G gNodeBs require carrier-grade telecom hardware.",
              "Our prototype is a calibrated discrete-event network queueing and signal processing simulation based on 3GPP TS 23.501 and TS 38.300 latency profiles.",
              "The signal generation, EWMA anomaly detector, queue model, alert manager, and dashboard are 100% real executing code."],
             "FAQ 1: HARDWARE SCOPE")

    add_card(s10, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Algorithmic Trade-Offs",
             ["Question: Why is adaptive detector latency 7.0 s vs 0.5 s for fixed?",
              "Answer: The 7-second window is the intentional persistence filter (8-of-10 samples) required to distinguish true clinical events from motion artefacts.",
              "Question: How does 5G help if detector takes 7 seconds?",
              "Answer: Network latency is in milliseconds, while clinical decision windows are in seconds. 5G URLLC guarantees that once an alert is decided, it is delivered deterministically without queue congestion."],
             "FAQ 2: ALGORITHM & QUEUEING")

    # ==================== SLIDE 11: CONCLUSION ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "Conclusion & Future Research Directions")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Key Project Outcomes",
             ["Demonstrated that 5G benefits in healthcare arise from combining the URLLC radio, network slicing, and edge computing.",
              "Reduced alert latency from 123.4 ms (4G busy hour p99) to 17.5 ms (5G URLLC+MEC), achieving 0% deadline miss.",
              "Eliminated 14,052 false alarms using patient-specific EWMA baselines and persistence filtering.",
              "Reduced daily uplink data by 99.5%, preserving hospital network bandwidth and patient privacy."],
             "PROJECT SUMMARY")

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Future Scope (Roadmap for 2026-27)",
             ["Evaluation on Clinical Datasets: Benchmark against PhysioNet real-world intensive care ECG databases.",
              "Deep Learning Integration: Expand from EWMA to lightweight edge LSTM/Autoencoder models.",
              "5G RedCap Integration: Optimize transmission for battery-constrained wearable IoT sensors.",
              "Testbed Deployment: Emulate RAN protocols using open-source stacks like Open5GS and srsRAN."],
             "FUTURE ENHANCEMENTS")

    out_path = r"C:\Users\harsh\OneDrive\Documents\healthcare5g_project\5G_Healthcare_Monitoring_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path}")

if __name__ == "__main__":
    create_deck()
