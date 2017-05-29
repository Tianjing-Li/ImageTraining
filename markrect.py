# USAGE
# python markrect.py -i imagefolder/ -j jsonfile.json
# 'S' - 'Save' key to save JSON
# 'N' - 'Next' key to next image
# 'P' - 'Previous' key to backtrack image
# 'Q' - 'Quit' key to quit

from Tkinter import *

import argparse
import cv2
import numpy as np
import json 
import glob
import os

# list of reference points
refPt = []
# list of elements in an image
elements = []
# name of current label
label = ""

chose = False

def printn(n):
	global root, label, chose

	if n == 1:
		label = "lonely"
	elif n == 2:
		label = "love"
	elif n == 3:
		label = "meeting"
	elif n == 4:
		label = "team"
	elif n == 5:
		label = "party"
	elif n == 6:
		label = "fighting"
	elif n == 7:
		label = "singers"

	print "Current label is {0}".format(label)

	chose = True

	# make window invisible
	root.withdraw()

	# make window visible
	# root.deiconify

	# destroy window
	# root.destroy()

# logic to center the Tkinter button frame onto screen
def center(toplevel):
	toplevel.update_idletasks()
	w = toplevel.winfo_screenwidth()
	h = toplevel.winfo_screenheight()
	size = tuple(int(_) for _ in toplevel.geometry().split("+")[0].split('x'))

	x = w/2 - size[0]/2
	y = h/2 - size[1]/2

	toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

# logic for displaying the images one after the other
def slideshow(images, json_name):
	global refPt, elements, label, image, clean, prev, root, chose

	global root
	root = Tk()
	root.wm_title("Choose a button")
	root.minsize(width=200, height=200)

	frame = Frame(root)

	frame.pack()

	button1 = Button(frame, text="Lonely", command= lambda: printn(1),  width= 20)
	button2 = Button(frame, text="Love", command= lambda: printn(2), width= 20)
	button3 = Button(frame, text="Meeting", command= lambda: printn(3), width= 20)
	button4 = Button(frame, text="Team", command= lambda: printn(4),  width= 20)
	button5 = Button(frame, text="Party", command= lambda: printn(5), width= 20)
	button6 = Button(frame, text="Fighting", command= lambda: printn(6), width= 20)
	button7 = Button(frame, text="Singers", command= lambda: printn(7),  width= 20)


	button1.pack()
	button2.pack()
	button3.pack()
	button4.pack()
	button5.pack()
	button6.pack()
	button7.pack()

	center(root)

	# star

	index = 0

	image = cv2.imread(images[index])

	# CLONE FOR RESETS
	prev = image.copy()
	clean = image.copy()

	cv2.namedWindow("Image")

	cv2.setMouseCallback("Image", mark_poly)

	#buttonPack()

	# loops until "Q" pressed
	while True:
		#root.update_idletasks()

		if not chose:
			root.update()

		# display image and wait for key
		cv2.imshow("Image", image)

		key = cv2.waitKey(1) & 0xFF

		# go to next image
		if key == ord("n") or key == ord("N"):
			save_json(images[index]) # saves current 
			if index < len(images) - 1:
				index = index + 1
				image = cv2.imread(images[index])
				# prepare frame for new image
				clean = image.copy()
				prev = image.copy()
				resetImage()
				# RESET CLICKER FOR NEW IMAGE
			else:
				os.system("say 'No more pictures'")

		# go to previous image
		elif key == ord("p") or key == ord("P"):
			if index > 0:
				index = index - 1
				image = cv2.imread(images[index])
				# prepare frame for new image
				clean = image.copy()
				prev = image.copy()
				resetImage()
				# RESET CLICKER FOR NEW IMAGE
			else:
				os.system("say 'No previous pictures")

		# save rectangle and label it
		elif key == ord("s") or key == ord("S"):
			if len(refPt) == 4:
				element = {}
				print refPt
				element["contours"] = order_coords_clockwise(refPt)
				element["label"] = label
				elements.append(element)
				
				prev = image.copy()

				del refPt[:]
				label = ""
				chose = False
				root.deiconify()
			else:
				os.system("say 'You don't have 4 coordinates")
				return

		# reset elements list for the current image
		elif key == ord("r") or key == ord("R"):
			resetImage()
			image = clean.copy()


		# finish marking and dump JSON
		elif key == ord("f") or key == ord("F"):
			with open(json_name, 'w') as js:
				json.dump(JSON, js)
			os.system("say 'All saved'")

		# quit
		elif key == ord("q") or key == ord("Q"):
			break
	root.mainloop()



def resetImage():
	global refPt, elements, label, root
	del refPt[:]
	del elements[:]
	root.deiconify()
	label = ""

# mark 4 coordinates
def mark_poly(event, x, y, flags, param):
	global refPt, elements
	global clean, image, prev

	if event == cv2.EVENT_LBUTTONDOWN:
		# if length of current coordinates is already 4

		if len(refPt) == 4:
			del refPt[:]
			image = prev.copy()

		refPt.append((x, y))

		# draw a point
		cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

		if len(refPt) > 1:
			l = len(refPt)
			cv2.line(image, refPt[l-1], refPt[l-2], (0, 0, 255), 2)
		if len(refPt) == 4:
			cv2.line(image, refPt[0], refPt[3], (0, 0, 255), 2)

		cv2.imshow("Image", image)

		print elements


# takes as input a list of elements
# each item in the list is a dictionary with
# label: name of the element ("fighting", "love", "meeting", etc.)
# contours: coordinates of the 4-sided polygon
def order_coords_clockwise(refPt):

	pts = np.array(refPt)
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	contour = np.zeros((4, 2), dtype = "int32")	#"float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	contour[0] = pts[np.argmin(s)]
	contour[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	contour[1] = pts[np.argmin(diff)]
	contour[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return contour.tolist()

# takes as input an image path and pointers (a set of rectangle coordinates) to create a json item
def save_json(image_path):
	global JSON, elements

	# iterate through objects in JSON to see if current image was already appended
	for i in xrange(len(JSON)):
		if JSON[i]["image_path"] == image_path:
			JSON.pop(i)
			break

	# create JSON object
	# image_path: the path to a specific image
	# elements: the labels and coordinates for elements inside the image
	json_obj = {}
	json_obj["image_path"] = image_path
	el = list(elements)
	json_obj["elements"] = el

	JSON.append(json_obj)

def main():
	global JSON
	# parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True, help="Path to image files")
	ap.add_argument("-j", "--json", required=True, help="Path to JSON file")

	args = vars(ap.parse_args())

	# create list of images
	image_list = []
	for type in ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png"):
		for image_path in glob.glob(args["image"] + "/" + type):
			image_list.append(image_path)


	# get name of JSON output file
	json_name = args["json"]
	if not json_name.endswith(".json"):
		json_name = json_name + ".json"

	# create JSON
	JSON = []

	# slideshow of images to add rectangles
	slideshow(image_list, json_name)


	cv2.destroyAllWindows()
	root.destroy()

if __name__ == "__main__":
	main();