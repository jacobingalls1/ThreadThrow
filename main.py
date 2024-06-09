import random
import time

import cv2

from drawing import Drawing
from board import PinDist

invertImage = False
invertTwine = False
xDim = 400
pins = 96
lines = 100
file = "/home/ophiuchus/Desktop/C++/gram/graycutout.png"
seed = 0
random.seed(0)
pinDist = PinDist.ELLIPSE


saved = [3, 89, 0]

doSaved = False
doWalkthrough = False

def doDrawing(fName):
    d = Drawing(fName, pins, invertImage, invertTwine, xDim, pinDist)
    if doSaved:
        moves = saved[:lines]
        d.doDrawList(moves)
        d.show('drawing')
        print("SCORE:", d.fullScore())
        if doWalkthrough:
            d.walkthrough('drawing', moves)
    else:
        d.doDraw(lines)
        print(d.show('drawing'))
        print("SCORE:", d.fullScore())
    cv2.destroyAllWindows()


doDrawing(file)
