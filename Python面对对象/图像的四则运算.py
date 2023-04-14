import numpy as np
from PIL import Image


class ImageObject:
    def __init__(self, path=""):
        self.path = path
        try:
            self.data = np.array(Image.open(path))
        except:
            self.data = None

    def __add__(self, other):
        image = ImageObject()
        try:
            image.data = np.mod(self.data + other.date, 255)
        except:
            image.data = self.data
        return image

    def __sub__(self, other):
        image = ImageObject()
        try:
            image.data = np.mod(self.data - other.data, 255)
        except:
            image.data = self.data
        return image

    def __mul__(self, factor):
        image = ImageObject()
        try:
            image.data = np.mod(self.data * factor, 255)
        except:
            image.data = self.data
        return image

    def __truediv__(self, factor):
        image = ImageObject()
        try:
            image.data = np.mod(self.data // factor, 255)
        except:
            image.data = self.data
        return image

    def saveImage(self, path):
        try:
            im = Image.fromarray(self.data)
            im.save(path)
            return True
        except:
            return False


a = ImageObject("/Python object\\grwordcloud.png")
b = ImageObject("/Python object\\holland_radar.jpg")
(a + b).saveImage("F:\\python study\\project\\Python object\\result_add.png")
(a - b).saveImage("F:\\python study\\project\\Python object\\result_sub.png")
(a * b).saveImage("F:\\python study\\project\\Python object\\result_mul.png")
(a / b).saveImage("F:\\python study\\project\\Python object\\result_div.png")
