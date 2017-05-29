import argparse
import glob
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True)
ap.add_argument("-s", "--save", required=True)

args = vars(ap.parse_args())

images = []
for type in ("*.jpg", "*.JPG"):
	for path in glob.glob(args["image"] + "/" + type):
		images.append(path)


for path in images:
	image = cv2.imread(path)

	res = cv2.resize(image, (608, 608))

	picname = path.split("/")[-1]

	cv2.imwrite(args["save"] + "/" + picname, res)



