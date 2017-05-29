import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)

args = vars(ap.parse_args())

image = cv2.imread(args["image"])

coords = [938, 1275, 380, 560]

cv2.rectangle(image, (coords[0], coords[2]), (coords[1], coords[3]), (0, 255, 0), 2)

cv2.imshow("im", image)

cv2.waitKey(0)