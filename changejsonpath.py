# USAGE
# python changejsonpath.py -j jsonfile -n newpath/

import argparse
import json
import glob

ap = argparse.ArgumentParser()
ap.add_argument("-j", "--json", required=True, help="path to json")
ap.add_argument("-n", "--new", required=True, help="new image path in json")

args = vars(ap.parse_args())

# read json
with open(args["json"], "r") as json_read:
	js = json.load(json_read)

# replace paths
for i in js:
	cur = i['image_path']

	picture = cur.split("/")[-1]

	# new path
	if args["new"][-1] == "/":
		toprint = args["new"]
		new = args["new"] + picture
	else:
		toprint = args["new"] + "/"
		new = args["new"] + "/" + picture

	i['image_path'] = new

with open(args["json"], "w") as json_write:
	json.dump(js, json_write)

print "\nImage path changed to " + toprint