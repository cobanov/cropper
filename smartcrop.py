import numpy as np
import cv2 as cv
import os


def detect(folder_path):
    for path, subdirs, files in os.walk("test_images"):
        for filename in files:
            if filename.endswith(".jpeg"):
                p = os.path.join(path, filename)

                img = cv.imread(p)
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
                cv.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv.rectangle(
                    img,
                    (x_mean - int(min_side / 2), y_mean - int(min_side / 2)),
                    (x_mean + int(min_side / 2), y_mean + int(min_side / 2)),
                    (0, 0, 255),
                    2,
                )
                # cv.rectangle(
                #     img,
                #     (x_mean - int(max_side / 2), y_mean - int(max_side / 2)),
                #     (x_mean + int(max_side / 2), y_mean + int(max_side / 2)),
                #     (0, 255, 0),
                #     0,
                # )

                cv.imwrite(f"results/out_{filename}", img)
                print(f"results/out_{filename}")


detect("./test_images")


# def combineBoundingBox(box1, box2):
#     x = min(box1[0], box2[0])
#     y = min(box1[1], box2[1])
#     w = box2[0] + box2[2] - box1[0]
#     h = max(box1[1] + box1[3], box2[1] + box2[3]) - y
#     return (x, y, w, h)
