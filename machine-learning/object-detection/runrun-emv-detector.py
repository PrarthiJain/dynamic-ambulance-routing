import sys, subprocess
from itertools import cycle
container = sys.argv[1]
while True:
    subprocess.check_call((sys.executable, 'yolo.py', container))