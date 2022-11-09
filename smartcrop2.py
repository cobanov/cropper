import os
import cv2 as cv
import numpy as np
from PIL import Image

EXTENSIONS = ("jpg", "JPG", "jpeg", "JPEG", "png", "PNG")


class cropper:
    def __init__(self) -> None:
        self.img = None
        self.kp = None

    def read(self, path):
        self.path = path
        self.img = cv.imread(self.path)
        return self.img

    def display(self):
        Image.fromarray(self.img).show()

    def _get_sift(self):
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        sift = cv.SIFT_create(edgeThreshold=8)
        kp = sift.detect(gray, None)
        return kp

    def detect(self):
        self.kp = self._get_sift()
        self.all_points = [i.pt for i in self.kp]

        x_points = [z[0] for z in self.all_points]
        y_points = [z[1] for z in self.all_points]

        thresh = 0

        self.x_min, self.y_min = int(min(x_points)) - thresh, int(
            min(y_points) - thresh
        )
        self.x_max, self.y_max = int(max(x_points)) + thresh, int(
            max(y_points) + thresh
        )

        self.min_side = min((self.x_max - self.x_min), (self.y_max - self.y_min))
        # max_side = max((self.x_max - self.x_min), (self.y_max - self.y_min))

        self.x_mean, self.y_mean = int((self.x_max + self.x_min) / 2), int(
            (self.y_max + self.y_min) / 2
        )

        # img = cv.drawKeypoints(img, kp, img)

        self.squared_x_min, self.squared_x_max = self.x_mean - int(
            self.min_side / 2
        ), self.x_mean + int(self.min_side / 2)
        self.squared_y_min, self.squared_y_max = self.y_mean - int(
            self.min_side / 2
        ), self.y_mean + int(self.min_side / 2)
        return (
            self.squared_x_min,
            self.squared_x_max,
            self.squared_y_min,
            self.squared_y_max,
        )

    def crop(self, outdir="./cropped", cropped=True, squared=True):
        self.detect()
        if cropped and not squared:
            cropped_image = self.img[self.y_min : self.y_max, self.x_min : self.x_max]
            image_relative = self.path.split("/")[-1]
            cv.imwrite(os.path.join(outdir, image_relative), cropped_image)
            # print(f"cropped/{image_relative}_out.jpeg")

        elif cropped and squared:

            cropped_image = self.img[
                self.squared_y_min : self.squared_y_max,
                self.squared_x_min : self.squared_x_max,
            ]

            image_relative = self.path.split("/")[-1]
            print(os.path.join(outdir, image_relative))
            cv.imwrite(os.path.join(outdir, image_relative), cropped_image)
            # print(f"Square cropped/{image_relative}_out.jpeg")

        else:
            cv.rectangle(
                self.img,
                (self.x_min, self.y_min),
                (self.x_max, self.y_max),
                (0, 255, 0),
                2,
            )
            cv.rectangle(
                self.img,
                (self.squared_x_min, self.squared_y_min),
                (self.squared_x_max, self.squared_y_max),
                (0, 0, 255),
                2,
            )

            image_relative = self.path.split("/")[-1]
            cv.imwrite(os.path.join(outdir, image_relative), self.img)
            # print(f"results/{image_relative}_out.jpeg")


img1 = cropper()
img1.read("./assets/result_2.jpeg")
# img1.detect()
img1.crop(squared=False)
