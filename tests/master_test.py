import sys
import os

for filename in os.listdir(sys.path[0]):
	if filename != "master_test.py" and filename.endswith(".py"):
		os.system("python3 " + sys.path[0] + "/" + filename)