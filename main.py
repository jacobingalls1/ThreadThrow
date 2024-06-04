import time

import cv2

from drawing import Drawing

invertImage = False
invertTwine = False
xDim = 400
pins = 96
lines = 1000
file = "/home/ophiuchus/Desktop/C++/gram/graycutout.png"


def doDrawing(fName):
    d = Drawing(fName, pins, invertImage, invertTwine, xDim)
    d.doDraw(lines)
    # d.doDrawList(moves)
    d.show('drawing')
    # d.walkthrough('drawing', moves)
    cv2.destroyAllWindows()


doDrawing(file)
