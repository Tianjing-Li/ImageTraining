#usage: python mergejson.py destination sourc1 source2 ...

import sys
import numpy as np
import json
import os


if len(sys.argv) < 3:
	print "Usage: " + sys.argv[0] + " dest source1 source2 ..."


mergedjson = []


print 'arange', np.arange(2, len(sys.argv))

for i in np.arange(2, len(sys.argv)):
	with open(sys.argv[i]) as data_file:
		jsondata = json.load(data_file)

	print 'jsondata', jsondata
	mergedjson.extend(jsondata)


mergedjsonfile = sys.argv[1]
if not mergedjsonfile.endswith('.json'):
	mergedjsonfile = mergedjsonfile + '.json'

with open(mergedjsonfile, "w") as outfile:
	json.dump(mergedjson, outfile)




