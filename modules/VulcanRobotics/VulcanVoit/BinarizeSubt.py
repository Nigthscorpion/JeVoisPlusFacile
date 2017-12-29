import libjevois as jv
import cv2
import numpy

class BinarizeSubt:

    # input:  camera frame in CV_BGR format
    # returns: binarized frame (green retroreflective target)
    def binarize(self, inCvBgr):
        green = cv2.extractChannel(inCvBgr, 1)
        red = cv2.extractChannel(inCvBgr, 2)

        outCvGrey = cv2.subtract(green, red)
        outCvGrey = cv2.threshold(outCvGrey, 0, 255, cv2.THRESH_OTSU)