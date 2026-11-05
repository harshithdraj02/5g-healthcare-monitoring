import os, sys

target_script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "gui_app.py")
if __name__ == "__main__":
    exec(open(target_script).read())
