import math
import random
from enum import Enum, auto


class Board:
    def __init__(self, pins, height, width, pinDist): #num pins and aspect ratio of width:height
        self.pins = pins
        self.h = height
        self.h2 = height / 2
        self.w = width
        self.w2 = width / 2
        self.pinPos = []
        for p in range(self.pins):
            self.pinPos.append(pinDist(self, p))

    def doPinPosEllipse(self, pin): #position of pinth pin as projected from even spacing on the director circle
        theta = 2 * math.pi * pin / self.pins
        e = math.sqrt(1 - (self.h2**2/ self.w2**2))
        r = (self.h2 / math.sqrt(1-(e * math.cos(theta))**2)) - 1
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return int(x + self.w2), int(y + self.h2)

    def doPinPosRandom(self, pin):
        randx = 10 + random.random() * (self.w - 20)
        randy = 10 + random.random() * (self.h - 20)
        return int(randx), int(randy)

    def doPinPosDensity(self, pin):
        pass

    def getPin(self, pin):
        return self.pinPos[pin]

    def getPins(self):
        return [self.getPin(i) for i in range(self.pins)]


class PinDist(Enum):
    ELLIPSE = Board.doPinPosEllipse
    RANDOM = Board.doPinPosRandom
    DENSITY = Board.doPinPosDensity