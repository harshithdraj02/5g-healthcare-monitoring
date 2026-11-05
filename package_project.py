import os, zipfile

base_dir = os.path.dirname(os.path.abspath(__file__))

# 1. Run build_clean_simulator.py
exec(open(os.path.join(base_dir, "build_clean_simulator.py"), encoding="utf-8").read())

# 2. Copy to healthcare5g/index.html
shutil_copy = True
try:
    import shutil
    shutil.copy2(os.path.join(base_dir, "5G_Healthcare_Monitoring_Submission.html"),
                 os.path.join(base_dir, "healthcare5g", "index.html"))
except Exception as e:
    print("Warning on copy:", e)

# 3. Create zip package
zip_path = os.path.join(base_dir, "5G_Healthcare_Monitoring_Complete_Project_Submission.zip")
print(f"Creating zip bundle: {zip_path}...")

files_to_include = [
    "5G_Healthcare_Monitoring_Prototype_Report.pdf",
    "gui_app.py",
    "run_demo.bat",
    "5G_Healthcare_Monitoring_Presentation.pptx",
    "5G_Healthcare_Monitoring_Submission.html",
    "index.html",
    "report_extracted.txt",
    "run_all.py",
    "pipeline.py",
    "check.py"
]

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in files_to_include:
        f_path = os.path.join(base_dir, f)
        if os.path.exists(f_path):
            zf.write(f_path, arcname=f)
            print(f"  Added {f}")
    
    # Add results directory
    res_dir = os.path.join(base_dir, "results")
    if os.path.exists(res_dir):
        for root, dirs, files in os.walk(res_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zf.write(full_path, arcname=rel_path)
        print("  Added results directory")

    # Add healthcare5g directory
    hc_dir = os.path.join(base_dir, "healthcare5g")
    if os.path.exists(hc_dir):
        for root, dirs, files in os.walk(hc_dir):
            if "__pycache__" in root:
                continue
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                zf.write(full_path, arcname=rel_path)
        print("  Added healthcare5g directory")

print(f"\nDone! Zip file size: {os.path.getsize(zip_path):,} bytes")
print(f"Zip path: {zip_path}")
