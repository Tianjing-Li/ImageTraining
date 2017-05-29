#usage: python mergeimage.py dstpath src1 src2 ..

import sys
import numpy as np 
import subprocess

if len(sys.argv) < 3:
	print "Usage: " + sys.argv[0] + " dst src1 src2 .."

dest = sys.argv[1] + "/"

for i in np.arange(2, len(sys.argv)):
	src = sys.argv[i] + "/*"
	cmd = "cp " + src + " " + dest
	subprocess.call(cmd, shell=True)

	
