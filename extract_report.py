import zipfile
import xml.etree.ElementTree as ET
import os

path = r"C:\Users\harsh\OneDrive\Documents\5G_Healthcare_Monitoring_Mini_Project_Report.docx"
print(f"Reading {path}...")

with zipfile.ZipFile(path, 'r') as z:
    names = z.namelist()
    print("Files in docx:", [n for n in names if 'document' in n or 'table' in n])
    xml_content = z.read('word/document.xml')

root = ET.fromstring(xml_content)
w_namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Extract both paragraphs and tables systematically
output_lines = []

body = root.find(f"{{{w_namespace}}}body")
if body is not None:
    for child in body:
        tag = child.tag.replace(f"{{{w_namespace}}}", "")
        if tag == "p":
            texts = [node.text for node in child.iter(f"{{{w_namespace}}}t") if node.text]
            if texts:
                output_lines.append("".join(texts))
            else:
                output_lines.append("")
        elif tag == "tbl":
            output_lines.append("\n--- TABLE START ---")
            for row in child.iter(f"{{{w_namespace}}}tr"):
                row_cells = []
                for cell in row.iter(f"{{{w_namespace}}}tc"):
                    cell_text = "".join(node.text for node in cell.iter(f"{{{w_namespace}}}t") if node.text)
                    row_cells.append(cell_text.strip())
                output_lines.append(" | ".join(row_cells))
            output_lines.append("--- TABLE END ---\n")

full_text = "\n".join(output_lines)
out_file = os.path.join(os.path.dirname(__file__), "report_extracted.txt")
with open(out_file, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"Successfully extracted report to {out_file} ({len(output_lines)} lines, {len(full_text)} chars).")
