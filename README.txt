markcontour.py:
	- iterate through a set of images and mark the positive images with 4 coordinates

	-> python markcontour.py -i image_path/ -j json_file_name

orientation.py:
	- rotate the image to the corresponding "correct" orientation
	- to accomodate the cv2.imread function for OpenCV 2.4.13.2, which does not account for EXIF information

	-> python orientation.py -i image_path/ -d destination_path/ 

mergejson.py:
	- merge 2+ json files into one

	-> python mergejson.py destination_json_file_name source1 source2 source...

mergeimage.py:
	- copy the images from 1+ image folders into a destination folder

	-> python mergeimage.py destination_path/ path1/ path2/ ..

jsontool.py:
	- used to delete all images that don't have a corresponding JSON object
	- changes the path to the image to the desired path
	- counts JSON objects

	-> python jsontool.py -i image_path/ -j json_file

	   OPTIONAL: -n ("new") newpath/ (modifies all JSON image_path values to newpath)
	   			 -d ("delete") path/image_to_delete.JPG (deletes a specific image + its corresponding JSON object)

	   			 