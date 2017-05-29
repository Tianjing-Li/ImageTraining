import cv2
import subprocess
import sys 
import imutils
import argparse
import glob

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True) #image source
ap.add_argument("-d", "--destination", required=True) #rotated image destination

# parse arguments given in cmd
args = vars(ap.parse_args())

images = []
# get all paths to images
for ext in ('*.jpg', '*.jpeg', '*.JPG'):
	# if there is a valid path to an image, append it
	for path in glob.glob(args["image"] + "/" + ext):
		images.append(path)

# for each path to an image
for imagePath in images:

	# get EXIF orientation, stored in rotate
	ls = subprocess.check_output(['exiftool', '-orientation', imagePath]).rstrip('\n').split(':')
	rotate = ls[1][1:]

	# read image
	image = cv2.imread(imagePath)

	# get name of image
	ls2 = imagePath.split("/")
	name = ls2[len(ls2) - 1] 

	dstPath = args["destination"] + "/" + name

	if rotate == "Rotate 90 CW":
		image = imutils.rotate_bound(image, 90)
		cv2.imwrite(dstPath, image)

	if rotate == "Rotate 180":
		image = imutils.rotate_bound(image, 180)
		cv2.imwrite(dstPath, image)




