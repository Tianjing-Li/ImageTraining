# USAGE
# python jsontool.py -n newpath/ -i imagefolder/ -j jsonfile -d path/image_to_delete.JPG

import argparse
import json
import glob
import cv2
import subprocess
import os

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--new", nargs='?', const="", help="Path to change image path to")
ap.add_argument("-i", "--image", required=True, help="Path to images")
ap.add_argument("-j", "--json", required=True, help="Path to JSON file")
ap.add_argument("-d", "--delete", nargs='?', const="", help="Path to image to delete")

args = vars(ap.parse_args())

# read json file
with open(args["json"], "r") as json_read:
	js = json.load(json_read)

# if there exists a new path, change it
if args["new"] is not None:
	for i in js:
		cur = i['image_path']

		# get last item of list, which is the image file name
		picture = cur.split("/")[-1]

		# new path
		if args["new"][-1] == "/":
			toprint = args["new"]
			new = args["new"] + picture
		else:
			toprint = args["new"] + "/"
			new = args["new"] + "/" + picture

		i['image_path'] = new

	print "\nimage_path in JSON changed to " + toprint + "\n"

# delete an image + JSON
if (args["delete"] is not None):
	# delete image

	extensions = {".jpg", ".jpeg", ".JPG", ".JPEG"}

	isimage = False

	for ext in extensions:
		if args["delete"].endswith(ext):
			isimage = True

	if isimage:
		if (os.path.isfile(args["delete"])):
			cmd = "rm " + args["delete"]
			subprocess.call(cmd, shell=True)
		else:
			print "Not a valid path to an image\n"
	else:
		print "You have not specified an image file\n"

	# get image file name
	name = args["delete"].split("/")[-1]

	deleted = False

	# delete corresponding json object
	for i in xrange(len(js)):
		cur = js[i]['image_path']
		picture = cur.split("/")[-1]

		if picture == name:
			js.pop(i)
			deleted = True
			break

	if deleted:
		print "After deletion, there are now " + str(len(js)) + " JSON objects\n"
	else: 
		print "There was no JSON for the image, so nothing was deleted\n"

# get paths to all photos
images = []
for ext in ('*.jpg', '*.jpeg', '*.png', '*.JPG'):
	for path in glob.glob(args["image"] + "/" + ext):
		images.append(path)

# if there are more images than json objects
if len(images) > len(js):
	print "There are " + str(len(images)) + " images for " + str(len(js)) + " JSON objects\n"
	print "Would you like to delete the extra images?\n"

	ans = raw_input("(y/n): ")

	if ans[0] == "y" or ans[1] == "Y":
		# prune all images with no corresponding JSON objects
		for path in images:
			name = path.split("/")[-1]

			exists = False

			for i in xrange(len(js)):
				cur = js[i]['image_path']
				picture = cur.split("/")[-1]

				if picture == name:
					exists = True

			if not exists:
				cmd = "rm " + args["image"] + "/" + name
				subprocess.call(cmd, shell=True)

print "There are a total of " + str(len(js)) + " JSON objects\n"		

# write into json file
with open(args["json"], "w") as json_write:
	json.dump(js, json_write)

