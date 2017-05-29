# USAGE
# This script takes in a path to a folder containing any number of images, and adds
# a transparent foreground to 4 coordinates on the image (usually a cropped picture of a window) to 
# simulate glare on a canvas 

# python addwindowNX.py -i image_path/ -w window_path/window.JPG -d destination_path/
import glob
import os
import argparse
import subprocess
from PIL import Image
from PIL import ImageDraw

# parse all arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to images to edit")
ap.add_argument("-w", "--window", required=True, help="Path to window to add into background layer")
ap.add_argument("-s", "--save", nargs="?", const="", help="Destination of modified images")

args = vars(ap.parse_args())

# create list of paths, by default appends the main folder in args["image"]
paths = []
paths.append(args["image"])
# appends all subfolders if they exist (only for one level)
for x in next(os.walk(args["image"]))[1]:
	paths.append(x)

for i in range(0, len(paths)):
	# current path
	if i == 0:
		curpath = args["image"] + "/"
	else:
		curpath = args["image"] + "/" + paths[i] + "/"

	# save path
	if args["save"] is not None:
		savepath = args["save"] + "/"
		# if a subfolder
		if i != 0:
			savepath = savepath + paths[i] + "/"

		# check if directory exists, if not, create it
		if not os.path.isdir(savepath):
			cmd = "mkdir " + savepath
			subprocess.call(cmd, shell=True)

	else:
		savepath = args["image"] + "/"
		# if a subfolder
		if i != 0:
			savepath = savepath + paths[i] + "/"

	# store paths to all images
	images = []

	# for all extensions (add more if needed)
	for ext in ('*.jpg', '*.JPG', '*.JPEG', '*.jpeg'):
		# for all valid paths, add them to the list of image paths
		for path in glob.glob(curpath + "/" + ext):
			images.append(path)

	for path in images:
		# open window image
		background = Image.open(path).convert('RGBA')
		foreground = Image.open(args["window"]).convert('RGBA')

		# dimensions of CANVAS
		width, height = background.size

		# dimensions of WINDOW
		w, h = foreground.size

		# resize WINDOW to fit CANVAS
		basewidth = int(width/1.5)
		wpercent = basewidth/float(w)
		hsize = int((float(h) * float(wpercent)))
		foreground = foreground.resize((basewidth, hsize), Image.ANTIALIAS)

		# create coordinates for WINDOW placement
		coords = []
		coords.append([100,100])
		coords.append([width/2, 100])
		coords.append([100, height/2])
		coords.append([width/2, height/2])

		picturename = path.split("/")[-1].split(".")[0]

		index = 1

		for coord in coords:
			x = coord[0]
			y = coord[1]

			# create new image of size of background
			newforeground = Image.new('RGBA', size = (width, height), color = (0, 0, 0, 0))
			newforeground.paste(foreground, (x, y))
			lol = Image.blend(newforeground, background, .85)

			save = savepath + picturename + "_" + str(index) + ".JPG"
			
			lol.save(save)

			index = index + 1





