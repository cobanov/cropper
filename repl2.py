import os
import cv2 as cv
from PIL import Image

img = cv.imread("./assets/result_1.jpg")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
sift = cv.SIFT_create(edgeThreshold=8)
kp = sift.detect(gray, None)
all_points = [i.pt for i in kp]
 all_points]