# USAGE
# python markcontour.py --image jurassic_park_kitchen.jpg --json json_file_name
# 's' key to save json file
# 'n' key to move to next image. Note: Even when reach the last image, still it needs to press '
#     n' key to add last image to the list
# 'p' key to move to previous image
# 'q' key to quit

# import the necessary packages
import argparse
import cv2
import numpy as np
import json
import glob
import os

# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False

jsondata = []

# order points as clockwise
def order_points_clockwise(refPt):
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


def enclosureRect(pts, x, y):
	inds_array = np.moveaxis(np.array(pts), -1, 0)
	xlist = np.append(inds_array[0], [x])

	ylist = np.append(inds_array[1], [y])
	x0 = min(xlist)
	y0 = min(ylist)
	x1 = max(xlist)
	y1 = max(ylist)
	return (x0, y0, x1, y1)


def redrawImage(ptsPrev, x, y):
	global image, clone, refPt
	
	h, w = image.shape[:2]
	
	(x0, y0, x1, y1) = enclosureRect(ptsPrev, x, y)
	if x0 > 5:
		x0 = x0 -5
	if y0 > 5:
		y0 = y0 -5

	if x1 < w -5:
		x1 = x1 + 5
	if y1 < h -5:
		y1 = y1 + 5

#image = clone.copy()
	redrawportion = clone[y0:y1, x0:x1]
	image[y0:y1, x0:x1] = redrawportion

	for i in np.arange(len(refPt)):
		(x, y) = refPt[i]
		cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

	for i in np.arange(1, len(refPt) +1):
		cv2.line(image, refPt[i-1], refPt[i%4], (0, 0, 255), 1)

	cv2.imshow("image", image)



# return index of refPt or -1 for nothing
def isAtCorner(x, y):
	global refPt

	for i in np.arange(len(refPt)):
		(x0, y0) = refPt[i]
		if (x-x0)*(x-x0) + (y-y0)*(y-y0) < 100:
			return i
	return -1

def resetForNewImage():
	global dragPointIndex, refPt, image, clone
	del refPt[:]
	dragPointIndex = -1
	clone = image.copy()

def click_to_mark(event, x, y, flags, param):
	global refPt, cropping
	global dragPointIndex
	global clone, image
	
	if dragPointIndex != -1:
		refPtPrev = refPt[:]
		refPt[dragPointIndex] = (x, y)
		redrawImage(refPtPrev, x, y)
	
	if event == cv2.EVENT_LBUTTONUP:
		if dragPointIndex != -1:
			dragPointIndex = -1

			return
	
	if event == cv2.EVENT_LBUTTONDOWN:
		# if box is created and click at any corner of box, entern into dragPointIndex status
		if len(refPt) == 4:
			index = isAtCorner(x, y)
			print 'index=', index
			dragPointIndex = index
			if index == -1:
				image = clone
				resetForNewImage()
			return
	
		if len(refPt) == 4:
			del refPt[:]
		
		refPt.append((x, y))
		# draw a point
		cv2.circle(image, (x, y), 3, (0, 0, 255), -1)

		if len(refPt) > 1:
			l = len(refPt)
			cv2.line(image, refPt[l-1], refPt[l-2], (0, 0, 255), 1)
		if len(refPt) == 4:
			cv2.line(image, refPt[0], refPt[3], (0, 0, 255), 1)
		
		cv2.imshow("image", image)





# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="Path to folder of images ")
ap.add_argument("-j", "--json", required=True, help="Json file name")

args = vars(ap.parse_args())
# load the image, clone it, and setup the mouse callback function



#image = cv2.imread(args["image"])
#clone = image.copy()

imageslist = []
imageslistIndex = 0
for type in ('*.jpg', '*.jpeg', '*.png', '*.JPG'):
	for imagePath in glob.glob(args["images"] + "/" + type):
		imageslist.append(imagePath)

cv2.namedWindow("image")

jsonfilename = args["json"]
if not jsonfilename.endswith('.json'):
	jsonfilename = jsonfilename + '.json'
#jsonfile = open(jsonfilename, "w")

image = cv2.imread(imageslist[imageslistIndex])
resetForNewImage()

cv2.setMouseCallback("image", click_to_mark)	#click_and_crop)

def addToJsondata():
	global imageslist, imageslistIndex

	if len(refPt) != 4:
		return
	
	json_item = {}
	json_item['image_path'] = imageslist[imageslistIndex]
		
	json_item['contour'] = order_points_clockwise(refPt)
	jsondata.append(json_item)

# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("n") or key == ord("N"):
		addToJsondata()
		if imageslistIndex < len(imageslist)-1:
			imageslistIndex = imageslistIndex + 1
			image = cv2.imread(imageslist[imageslistIndex])
			resetForNewImage()
		else:
			os.system("say 'no more shit'")

	if key == ord("p") or key == ord("P"):
		if imageslistIndex > 0:
			imageslistIndex = imageslistIndex - 1
			image = cv2.imread(imageslist[imageslistIndex])
			resetForNewImage()
		else:
			os.system("say 'that is all shit'")

	# if the 'c' key is pressed, break from the loop
	if key == ord("q") or key == ord("Q"):
		break

	if key == ord("s") or key == ord("S"):
		with open(jsonfilename, 'w') as jsonfile:
			json.dump(jsondata, jsonfile)
		os.system("say 'your jay-son shit is saved'")


#	if clickcounter == 4:
#
#		pts = np.array(refPt)
#		print 'pts', pts
#		rect = order_points(pts)
#		print 'rect', rect
#		dst = np.array([[0,0], [899,0], [899, 1599], [0, 1599]], dtype="float32")
#		print 'dst', dst


		
#		warpedrect = cv2.perspectiveTransform(np.array([rect]), M)
#		print 'warpedrect', warpedrect




# if there are two reference points, then crop the region of interest
# from teh image and display it
if len(refPt) == 2:
	roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
	cv2.imshow("ROI", roi)
	cv2.waitKey(0)

# close all open windows
cv2.destroyAllWindows()