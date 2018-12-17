import sys
import os
import platform

call = 'python3 '
if 'Windows' in platform.platform():
	call = 'python '
	

for filename in os.listdir(sys.path[0]):
	if filename != "master_test.py" and filename.endswith(".py"):
		os.system(call + sys.path[0] + "/" + filename)