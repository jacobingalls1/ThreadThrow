import math
from copy import copy

from board import Board
import cv2
import numpy as np


class Drawing:
    def __init__(self, image_name, pins, invert_im, invert_twine, x_dim):
        self.invert_twine = invert_twine
        print(image_name)
        image = cv2.imread(image_name)
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if invert_im:
            self.image = (255-self.image)
        self.w, self.h = self.image.shape
        scale = x_dim / self.w
        self.image = cv2.resize(self.image, (int(scale * self.h), int(x_dim)))
        self.w, self.h = self.image.shape
        self.imageCopy = copy(self.image)
        self.image_walkthrough = np.zeros((self.w, self.h, 3), np.uint8)
        self.image_walkthrough[:] = 255
        print(self.w, self.h)
        self.final_image = np.zeros((self.w, self.h, 1), np.uint8)
        if not self.invert_twine:
            self.final_image += 255
        self.board = Board(pins, self.h, self.w)
        self.pins = self.board.getPins()
        self.peg_order = []
        self.paths = {p: {} for p in range(len(self.pins))}

    def pathPixels(self, pin1, pin2):
        if pin2 in self.paths[pin1]:
            return self.paths[pin1][pin2]
        if pin1 == pin2:
            return []
        a = self.pins[pin1]
        b = self.pins[pin2]
        Dx = b[0] - a[0]
        Dy = b[1] - a[1]
        span = max(abs(Dx), abs(Dy))
        dx, dy = Dx/span, Dy/span
        path = []
        for i in range(span):
            path.append((int(a[0] + dx * i), int(a[1] + dy * i)))
        self.paths[pin1][pin2] = path
        self.paths[pin2][pin1] = path
        return path

    def stringScore(self, path):
        score = 0
        if not len(path):
            return score
        for p in path:
            if self.invert_twine:
                score += self.image[p[0]][p[1]]
            else:
                score += 255 - self.image[p[0]][p[1]]
        return score / (len(path))

    def bestScore(self, start):
        return max([p for p in range(len(self.pins)) if p != start],
                   key=lambda x: self.stringScore(self.pathPixels(x, start)))

    def bestStart(self):
        return max(range(len(self.pins)),
                   key=lambda x: self.bestScore(x))

    def drawLine(self, pin1, pin2):
        for p in self.pathPixels(pin1, pin2):
            if self.invert_twine:
                self.image[p[0]][p[1]] = 0
                self.final_image[p[0]][p[1]] = 255
            else:
                self.image[p[0]][p[1]] = 255
                self.final_image[p[0]][p[1]] = 0
        return len(self.pathPixels(pin1, pin2))

    def drawLineWalkthrough(self, pin1, pin2, red=False):
        for p in self.pathPixels(pin1, pin2):
            if red:
                self.image_walkthrough[p[0]][p[1]] = (0, 0, 255)
            else:
                self.image_walkthrough[p[0]][p[1]] = (0, 0, 0)
        return len(self.pathPixels(pin1, pin2))

    def doDraw(self, steps):
        self.peg_order = [self.bestStart()]
        for i in range(steps):
            self.peg_order.append(self.bestScore(self.peg_order[-1]))
            print(self.peg_order[-2:])
            self.drawLine(self.peg_order[-2], self.peg_order[-1])

    def doDrawList(self, pins):
        self.peg_order = pins
        length = 0
        for i in range(len(pins) - 1):
            length += self.drawLine(pins[i], pins[i+1])
        print(length / self.w)

    def show(self, window_name):
        print(self.peg_order)
        cv2.imshow(window_name, self.final_image)
        while cv2.waitKey(0) != 27:
            continue

    def walkthrough(self, window_name, pins):
        self.peg_order = pins
        length = 0
        for i in range(len(pins) - 1):
            text = "%i -> %i #%i"%(pins[i], pins[i+1], i)
            print(text)
            self.drawLineWalkthrough(pins[i], pins[i+1], True)
            toDraw = self.image_walkthrough.copy()
            scale = 2
            toDraw = cv2.resize(toDraw, (int(scale * self.h), int(scale * self.w)))

            cv2.putText(toDraw, text, (0, 25), cv2.FONT_HERSHEY_SIMPLEX, .95, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow(window_name, toDraw)
            while cv2.waitKey(0) != 32:
                continue
            length += self.drawLineWalkthrough(pins[i], pins[i+1], False)
            print(length / self.w)
