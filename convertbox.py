# USAGE:
# python convertbox.py -j jsonfile.json

import argparse
import json
from collections import OrderedDict



def box_json(contourjson):
	# list to contain box data
	json_data = []

	# load original json file
	with open(contourjson, "r") as js:
		jsonfile = json.load(js)

	for item in jsonfile:
		box_obj = {}

		box_obj["image_path"] = item["image_path"]
		box_obj["rects"] = []

		points = item["contour"]

		# store x's and y's in the same lists
		all_x = [x[0] for x in points]
		all_y = [x[1] for x in points]

		# create new dict for box coordinates 
		newcoords = {
		"x1":min(all_x), 
		"x2":max(all_x),
		"y1":min(all_y),
		"y2":max(all_y)}

		"""
		newcoords["x1"] = min(all_x)
		newcoords["x2"] = max(all_x)
		newcoords["y1"] = min(all_y)
		newcoords["y2"] = max(all_y)"""

		box_obj["rects"].append(newcoords)

		json_data.append(box_obj)

	return json_data

def main():
	# parse arguments
	ap = argparse.ArgumentParser() 
	ap.add_argument("-j", "--json", required=True)
	args = vars(ap.parse_args())

	# check if json argument ends with .json
	jsonname = args["json"]
	if not jsonname.endswith(".json"):
		jsonname = jsonname + ".json"

	# create the json with boxed coordinates
	boxjsondata = box_json(jsonname)

	# create new box json file nae
	boxjsonname = jsonname.split(".")[0] + "box.json"

	# load box json and dump data
	with open(boxjsonname, 'w') as boxfile:
		json.dump(boxjsondata, boxfile, sort_keys=False)

	print "Box data saved into " + boxjsonname


if __name__ == "__main__":
	main()
		