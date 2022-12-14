import os

import cv2 as cv
import filelister as fs
from joblib import Parallel, delayed
from tqdm import tqdm

EXTENSIONS = ("jpg", "JPG", "jpeg", "JPEG", "png", "PNG")


def detect(image_path, outdir="./cropped", crop=False, square=True):

    img = cv.imread(image_path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sift = cv.SIFT_create(edgeThreshold=8)
    kp = sift.detect(gray, None)

    all_points = [i.pt for i in kp]
    x_points = [z[0] for z in all_points]
    y_points = [z[1] for z in all_points]
    thresh = 0
    x_min, y_min = int(min(x_points)) - thresh, int(min(y_points) - thresh)
    x_max, y_max = int(max(x_points)) + thresh, int(max(y_points) + thresh)
    min_side = min((x_max - x_min), (y_max - y_min))
    max_side = max((x_max - x_min), (y_max - y_min))
    x_mean, y_mean = int((x_max + x_min) / 2), int((y_max + y_min) / 2)
    # img = cv.drawKeypoints(img, kp, img)
    squared_x_min, squared_x_max = x_mean - int(min_side / 2), x_mean + int(
        min_side / 2
    )
    squared_y_min, squared_y_max = y_mean - int(min_side / 2), y_mean + int(
        min_side / 2
    )

    if crop and not square:
        cropped_image = img[y_min:y_max, x_min:x_max]

        image_relative = image_path.split("/")[-1]
        cv.imwrite(os.path.join(outdir, image_relative), cropped_image)
        # print(f"cropped/{image_relative}_out.jpeg")

    elif crop and square:

        cropped_image = img[squared_y_min:squared_y_max, squared_x_min:squared_x_max]

        image_relative = image_path.split("/")[-1]
        cv.imwrite(os.path.join(outdir, image_relative), cropped_image)
        # print(f"Square cropped/{image_relative}_out.jpeg")

    else:
        cv.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
        cv.rectangle(
            img,
            (squared_x_min, squared_y_min),
            (squared_x_max, squared_y_max),
            (0, 0, 255),
            2,
        )

        image_relative = image_path.split("/")[-1]
        cv.imwrite(os.path.join(outdir, image_relative), img)
        # print(f"results/{image_relative}_out.jpeg")


def main(filelist, outdir, crop, square):
    flist = fs.read_filelist(filelist)
    Parallel(n_jobs=-1)(
        delayed(detect)(image, outdir, crop, square) for image in tqdm(flist)
    )
