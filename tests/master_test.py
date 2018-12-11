import sys
import os
import subprocess

filepath = sys.path[0] + "/../scripts/run_all_tests.sh"
#subprocess.call([filepath])
os.system(filepath)