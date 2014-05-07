import os
import sys
from PIL import Image

def resize(filePath, fileName, w, h):
    im = Image.open(filePath)
    newIm = im.resize((w, h))
    # i am saving a copy, you can overrider orginal, or save to other folder
    
    grey = newIm.convert('LA')
    grey = grey.convert('RGB')
    grey.save("..\\pos\\"+fileName)


if __name__ == "__main__":
    w = 24
    h = 24
    for root, _, files in os.walk("..\\detected_faces\\"):
        for f in files:
            resize(os.path.join(root, f), f, w, h)
