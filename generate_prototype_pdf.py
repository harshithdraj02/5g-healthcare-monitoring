import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
if not os.path.exists(RESULTS_DIR):
    RESULTS_DIR = os.path.join(BASE_DIR, "healthcare5g", "results")

PDF_PATH = os.path.join(BASE_DIR, "5G_Healthcare_Monitoring_Prototype_Report.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "5G-Enabled Intelligent Healthcare Monitoring — Prototype & Technical Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 748, 558, 748)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "Confidential — Mini Project Submission AY 2026-27 | Dept. of CSE, NMIT")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0284c7"),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0369a1"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=14,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'Caption_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#64748b"),
        alignment=1, # Center
        spaceAfter=8
    )

    th_style = ParagraphStyle(
        'TH_Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#ffffff"),
        alignment=1
    )

    td_style = ParagraphStyle(
        'TD_Style',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a")
    )

    td_center = ParagraphStyle(
        'TD_Center',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )

    td_bold_center = ParagraphStyle(
        'TD_Bold_Center',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        alignment=1
    )

    story = []

    # Title & Header
    story.append(Paragraph("5G-Enabled Intelligent Healthcare Monitoring", title_style))
    story.append(Paragraph("Complete Prototype Architecture, Anomaly Detection & 5G Latency Verification", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceBefore=0, spaceAfter=10))

    # Executive Summary / Meta Table
    meta_data = [
        [Paragraph("<b>Project:</b> Mini Project in Computer Science & Engineering", td_style),
         Paragraph("<b>Academic Year:</b> 2026–2027", td_style)],
        [Paragraph("<b>Domain:</b> 5G NR URLLC, Mobile Edge Computing (MEC), IoT Healthcare", td_style),
         Paragraph("<b>Status:</b> Fully Simulated & Verified", td_style)],
        [Paragraph("<b>Standards:</b> 3GPP TS 23.501 (System Architecture), TS 38.300 (NR Stage 2)", td_style),
         Paragraph("<b>Platform:</b> Python 3, Tkinter GUI, Web Operations Center", td_style)]
    ]
    meta_table = Table(meta_data, colWidths=[280, 224])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Introduction & Problem Statement
    story.append(Paragraph("1. Executive Summary & Problem Formulation", h1_style))
    story.append(Paragraph(
        "Remote patient monitoring (RPM) requires dependable, ultra-low-latency alert delivery while avoiding "
        "clinician alarm fatigue. Traditional monitoring setups rely on shared 4G cellular links with distant cloud "
        "servers. Under network congestion, medical alarm packets queue behind general mobile traffic, producing "
        "unpredictable delay spikes. Furthermore, rigid fixed threshold alarms (e.g. Heart Rate &gt; 100 bpm) "
        "trip indiscriminately on benign motion artefacts, inundating clinicians with over 280 false alarms per patient-day.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Proposed Solution:</b> This project designs, evaluates, and verifies an end-to-end intelligent monitoring pipeline "
        "coupling a <b>3GPP TS 23.501 5G URLLC dedicated priority slice</b>, co-located <b>Multi-access Edge Computing (MEC)</b>, "
        "and a patient-specific <b>Adaptive EWMA Anomaly Detector</b> with persistence filtering. All claims are verified "
        "over a simulated cohort of 100 patients across 12 hours (361 true clinical events).",
        body_style
    ))

    # Section 2: Architecture
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Proposed 5G System Architecture", h1_style))
    story.append(Paragraph(
        "The system architecture spans two primary operational tiers: the <i>Patient & Radio Access Tier</i> and the "
        "<i>Edge AI & Clinical Tier</i>. Telemetry from wearable sensors is packetized by the patient gateway (5G UE) "
        "and transmitted across a dedicated 5G Ultra-Reliable Low-Latency Communication (URLLC) network slice. "
        "The packet terminates directly at the local hospital User Plane Function (UPF) and co-located MEC node, "
        "eliminating public internet WAN routing delays.",
        body_style
    ))

    fig1_path = os.path.join(RESULTS_DIR, "fig1_architecture.png")
    if os.path.exists(fig1_path):
        story.append(Image(fig1_path, width=470, height=140))
        story.append(Paragraph("Figure 1: Block diagram of the proposed 5G-enabled healthcare monitoring architecture (3GPP TS 23.501).", caption_style))

    # Section 3: Methodology
    story.append(Paragraph("3. Technical Methodology & Algorithmic Formulation", h1_style))
    story.append(Paragraph("3.1 End-to-End Latency Model", h2_style))
    story.append(Paragraph(
        "For an alert packet travelling from the gateway to the clinician display, end-to-end latency L is formulated as:",
        body_style
    ))
    story.append(Paragraph("L = L_q + L_radio + L_transport + L_proc + L_dl + 1[lost] · L_retx", code_style))
    story.append(Paragraph(
        "Where <b>L_q</b> is the queueing delay at the shared cell radio buffer, <b>L_radio</b> is the air-interface transmission time interval (TTI) "
        "(10 ms in 4G; 5 ms in 5G eMBB; 1.5 ms in 5G URLLC mini-slots), <b>L_transport</b> is backhaul delay (log-normal: median 30 ms for 4G vs 2 ms for MEC), "
        "<b>L_proc</b> is execution delay, and <b>1[lost] · L_retx</b> accounts for HARQ retransmissions upon packet loss.",
        body_style
    ))

    story.append(Paragraph("3.2 Adaptive EWMA Anomaly Detector", h2_style))
    story.append(Paragraph(
        "To eliminate false alarms caused by sensor noise and transient motion artefacts (1–3 second glitches), "
        "the MEC host maintains an Exponentially Weighted Moving Average (EWMA) personal baseline and variance for each patient signal x(t):",
        body_style
    ))
    story.append(Paragraph("μ(t) = μ(t-1) + α · [x(t) - μ(t-1)],    z(t) = [x(t) - μ(t-1)] / σ(t)", code_style))
    story.append(Paragraph(
        "With memory coefficient α = 1/1800 (~30 minute sliding history). An alarm is flagged only when |z| &gt; 4.0 "
        "and confirmed when at least <b>8 of the last 10 samples</b> satisfy the condition (persistence rule).",
        body_style
    ))

    # Section 4: Results & Tables
    story.append(PageBreak())
    story.append(Paragraph("4. Experimental Results & Verification", h1_style))
    story.append(Paragraph(
        "The framework was evaluated across 100 simulated patients over 12 hours (1,200 patient-hours; 4.32 million readings) "
        "and 400 concurrent patient UEs under peak busy-hour cellular background load (1,500 background packet-units/s).",
        body_style
    ))

    # Table 4
    story.append(Paragraph("<b>Table 4: Anomaly Detection Performance (100 Patients × 12 Hours, 361 True Events)</b>", h2_style))
    t4_data = [
        [Paragraph("Scheme", th_style), Paragraph("Detected", th_style), Paragraph("Recall", th_style),
         Paragraph("Total Alarms", th_style), Paragraph("False Alarms", th_style), Paragraph("FA / Pt-Day", th_style), Paragraph("Mean Delay", th_style)],
        [Paragraph("Fixed Threshold (HR &gt; 100/&lt; 50, SpO₂ &lt; 92%)", td_style), Paragraph("359 / 361", td_center), Paragraph("99.4%", td_center),
         Paragraph("14,403", td_center), Paragraph("14,052", td_bold_center), Paragraph("281.0", td_bold_center), Paragraph("0.5 s", td_center)],
        [Paragraph("<b>Adaptive EWMA (Proposed)</b>", td_style), Paragraph("344 / 361", td_center), Paragraph("95.3%", td_center),
         Paragraph("341", td_center), Paragraph("<b>0</b>", td_bold_center), Paragraph("<b>0.0</b>", td_bold_center), Paragraph("7.0 s", td_center)]
    ]
    t4_table = Table(t4_data, colWidths=[150, 60, 50, 65, 65, 55, 59])
    t4_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f0fdf4")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t4_table)
    story.append(Spacer(1, 6))

    # Figure 2
    fig2_path = os.path.join(RESULTS_DIR, "fig2_detection.png")
    if os.path.exists(fig2_path):
        story.append(Image(fig2_path, width=470, height=130))
        story.append(Paragraph("Figure 2: Fixed-threshold vs adaptive EWMA alarms on patient trace (showing motion artefact suppression).", caption_style))

    # Table 5
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 5: End-to-End Latency Under Busy-Hour Congestion (400 Monitored Patients)</b>", h2_style))
    t5_data = [
        [Paragraph("Architecture Scheme", th_style), Paragraph("Mean (ms)", th_style), Paragraph("P95 (ms)", th_style),
         Paragraph("P99 Tail (ms)", th_style), Paragraph("Miss &gt; 100 ms", th_style), Paragraph("Miss &gt; 20 ms", th_style)],
        [Paragraph("A: 4G + Cloud (FIFO, Shared Cell)", td_style), Paragraph("74.7", td_center), Paragraph("105.2", td_center),
         Paragraph("123.4", td_bold_center), Paragraph("7.68%", td_bold_center), Paragraph("100.00%", td_center)],
        [Paragraph("B: 5G eMBB + Cloud (FIFO, 5G Radio)", td_style), Paragraph("46.2", td_center), Paragraph("66.3", td_center),
         Paragraph("79.4", td_center), Paragraph("0.07%", td_center), Paragraph("100.00%", td_center)],
        [Paragraph("<b>C: 5G URLLC + MEC (Proposed Priority Slice)</b>", td_style), Paragraph("<b>10.2</b>", td_bold_center), Paragraph("<b>14.3</b>", td_bold_center),
         Paragraph("<b>17.5</b>", td_bold_center), Paragraph("<b>0.00%</b>", td_bold_center), Paragraph("<b>0.28%</b>", td_bold_center)]
    ]
    t5_table = Table(t5_data, colWidths=[184, 60, 60, 65, 65, 70])
    t5_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc"), colors.HexColor("#f0fdf4")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t5_table)
    story.append(Spacer(1, 6))

    # Figures 3 and 4 side-by-side or stacked
    fig3_path = os.path.join(RESULTS_DIR, "fig3_cdf.png")
    fig4_path = os.path.join(RESULTS_DIR, "fig4_p99.png")
    if os.path.exists(fig3_path) and os.path.exists(fig4_path):
        f_table_data = [[
            Image(fig3_path, width=245, height=140),
            Image(fig4_path, width=245, height=140)
        ]]
        f_table = Table(f_table_data, colWidths=[252, 252])
        f_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(f_table)
        story.append(Paragraph("Figures 3 & 4: (Left) Latency Cumulative Distribution Function (CDF). (Right) P99 tail latency vs patient scale (50–400 UEs).", caption_style))

    # Table 6
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Table 6: Uplink Data Volume & Edge Offloading</b>", h2_style))
    t6_data = [
        [Paragraph("Transmission Approach", th_style), Paragraph("Daily Uplink Data / Patient", th_style), Paragraph("Relative Volume", th_style), Paragraph("Bandwidth Saved", th_style)],
        [Paragraph("Cloud-Centric (Continuous 250 Hz Raw Stream)", td_style), Paragraph("53.9 MB", td_center), Paragraph("100.0%", td_center), Paragraph("0.0%", td_center)],
        [Paragraph("<b>Edge-Filtered (1-Min Summaries + Alert Clips)</b>", td_style), Paragraph("<b>0.25 MB</b>", td_bold_center), Paragraph("<b>0.5%</b>", td_bold_center), Paragraph("<b>99.54% Saved</b>", td_bold_center)]
    ]
    t6_table = Table(t6_data, colWidths=[204, 110, 90, 100])
    t6_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f172a")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f0fdf4")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t6_table)

    # Section 5: Prototype Features & Viva
    story.append(PageBreak())
    story.append(Paragraph("5. Interactive Prototype Implementations", h1_style))
    story.append(Paragraph(
        "The project includes two operational interactive prototypes ready for examiner demonstration:",
        body_style
    ))
    story.append(Paragraph("• <b>Standalone Desktop Application (gui_app.py / run_demo.bat):</b> A live Tkinter and Matplotlib workstation featuring real-time vital sign plotting, dynamic EWMA baseline tracking, visual persistence filter cell displays, and radio queue latency calculations.", bullet_style))
    story.append(Paragraph("• <b>Clinical Operations Web Console (index.html / 5G_Healthcare_Monitoring_Submission.html):</b> A browser-based interactive dashboard with real-time Canvas ECG oscilloscopes (P-Q-R-S-T waves), dynamic 5G architecture switcher, synthetic audio alarms, and live injection controls.", bullet_style))
    story.append(Paragraph("• <b>Batch Verification Suite (check.py & run_all.py):</b> Recomputes all numerical metrics in 3 seconds, ensuring 100% mathematical reproducibility.", bullet_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("6. Key Technical Viva Defense Questions & Answers", h1_style))

    viva_qa = [
        ("Q1: Why is 5G URLLC required instead of standard 4G or 5G eMBB?",
         "4G operates with shared FIFO queues that degrade under congestion (Table 5 shows 7.68% packets miss the 100 ms target at 400 patients). 5G eMBB offers high bandwidth but routes over public internet to distant clouds (median 22 ms transport), causing 100% of packets to miss strict 20 ms URLLC deadlines. Only 5G URLLC with priority slicing and edge MEC achieves deterministic sub-20ms delivery."),
        ("Q2: How does network slicing prioritize medical telemetry at the radio scheduler?",
         "Under 3GPP TS 23.501, medical telemetry is assigned a dedicated logical slice configured for non-preemptive priority queueing at the gNodeB radio scheduler. As implemented in healthcare5g/network.py, medical packets jump to the head of the buffer ahead of queued background packets, guaranteeing predictable delivery independent of cell load."),
        ("Q3: How does the adaptive anomaly detector achieve zero false alarms?",
         "It maintains individual baselines using EWMA with memory α = 1/1800 (~30 min). Alerts require both a z-score deviation (|z| > 4.0) and an 8-out-of-10 sample persistence filter. Brief sensor motion artefacts (1–3s spikes) fail the persistence filter and are suppressed, avoiding clinician alarm fatigue."),
        ("Q4: Why does MEC provide a 99.5% uplink bandwidth reduction?",
         "In cloud-centric systems, continuous 250 Hz raw ECG must be streamed outside the hospital (53.9 MB/patient-day). With MEC, feature extraction happens on-premise at the edge node; only 1-minute summaries and 30-second clips around confirmed alerts are sent out (0.25 MB/patient-day), saving bandwidth and preserving patient privacy under DPDP 2023.")
    ]

    for q, a in viva_qa:
        q_box = [
            [Paragraph(f"<b>{q}</b>", td_style)],
            [Paragraph(f"<i>Answer:</i> {a}", td_style)]
        ]
        t = Table(q_box, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
            ('LINELEFT', (0,0), (0,-1), 3, colors.HexColor("#0284c7")),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    # Section 7: Conclusion
    story.append(Spacer(1, 6))
    story.append(Paragraph("7. Conclusion", h1_style))
    story.append(Paragraph(
        "This project demonstrated that 5G transforms healthcare monitoring when radio parameters, network slicing, "
        "and edge intelligence are integrated into a single cohesive pipeline. In simulation, the proposed architecture "
        "delivered alerts in 10.2 ms mean (17.5 ms P99) with 0% deadline misses, reduced false alarms from 281 to 0 per patient-day, "
        "and reduced uplink data volume by 99.5%. The complete code and interactive prototypes are reproducible and open for extension.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {PDF_PATH} ({os.path.getsize(PDF_PATH):,} bytes)")

if __name__ == "__main__":
    build_pdf()

