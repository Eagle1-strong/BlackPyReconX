# modules/reporting.py

import os
from datetime import datetime
from fpdf import FPDF

OUTPUT_DIR = "outputs"
SECTIONS = ["osint.txt", "scan_results.txt", "web_vulns.txt", "keylogs/keylog.txt"]
REPORT_HTML = os.path.join(OUTPUT_DIR, "rapport_final.html")
REPORT_PDF = os.path.join(OUTPUT_DIR, "rapport_final.pdf")

def generate_report():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    html = f"""<html><head><meta charset="utf-8">
    <title>Rapport BlackPyReconX</title></head><body>
    <h1>Rapport BlackPyReconX</h1>
    <em>Généré le : {datetime.now()}</em><br><br>
    """

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Rapport BlackPyReconX\nGénéré le : {datetime.now()}\n\n")

    for section in SECTIONS:
        path = os.path.join(OUTPUT_DIR, section)
        title = section.replace(".txt", "").capitalize()
        html += f"<h2>{title}</h2>\n"

        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
                html += f"<pre>{content}</pre>\n"
                pdf.multi_cell(0, 10, f"=== {title} ===\n{content}\n\n")
        else:
            html += "<p><em>Fichier non trouvé.</em></p>\n"
            pdf.multi_cell(0, 10, f"=== {title} ===\n[Fichier non trouvé]\n\n")

    html += "</body></html>"

    with open(REPORT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[+] Rapport HTML généré : {REPORT_HTML}")

    pdf.output(REPORT_PDF)
    print(f"[+] Rapport PDF généré : {REPORT_PDF}")
