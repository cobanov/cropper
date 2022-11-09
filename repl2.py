import smartcrop2
import os

for root, dirs, files in os.walk("./assets"):
    files = [os.path.join(root, path) for path in files]

for i in files:
    img = smartcrop2.cropper()
    img.read(i)
    # img.display()
    img.crop()
