import os, sys

target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "healthcare5g")
os.chdir(target_dir)
sys.path.insert(0, target_dir)

if __name__ == "__main__":
    exec(open(os.path.join(target_dir, "pipeline.py")).read())
