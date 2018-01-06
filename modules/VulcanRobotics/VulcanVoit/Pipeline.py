import libjevois as jv
import cv2
import numpy
from collections import namedtuple
from TuningParameters import TuningParameters as p

#class TargetInfo:

#    def __init__(self,centroid_x=0.0,centroid_y=0.0,width=0.0,height=0.0,points=[]):
#        self.centroid_x = centroid_x
#        self.centroid_y = centroid_y
#        self.width = width
#        self.height = height
#        self.points = points

TargetInfo = namedtuple("TargetInfo",["centroid_x","centroid_y","width","height","hull"])

# input:  camera frame in CV_BGR format
def process(inCvBgr):
    # Step 1: binarize
    if p.visionParams[p.binMethod] == 0:
        binImg = binarizeSubt(inCvBgr)
    else:
        binImg = binarizeHSV(inCvBgr)

    # Step 2: find and filter contours
    final_targets = []
    rejected_targets = []
    for c in cv2.findContours(binImg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_TC89_KCOS)[1]:
        hull = cv2.convexHull(c,returnPoints=True)
        if (cv2.isContourConvex(hull)):
            x, y, w, h = cv2.boundingRect(hull)
            t = TargetInfo(centroid_x=x+int(w/2),centroid_y=y+int(h/2),width=w,height=h,hull=hull)

            # check target area vs image area
            hullArea = cv2.contourArea(hull)
            hullPct = hullArea / (binImg.shape[0] * binImg.shape[1])
            hullAreaCheckPassed = hullPct >= p.visionParams[p.areaMin] and hullPct <= p.visionParams[p.areaMax]

            # check target solidity (% of hull occupied by the actual contour)
            targetFullness = cv2.contourArea(c) / hullArea
            targetFullnessCheckPassed = targetFullness >= p.visionParams[p.fullnessMin] and targetFullness <= p.visionParams[p.fullnessMax]

            # check bounding rect aspect ratio (width / height)
            aspect = t.width / t.height
            aspectCheckPassed = aspect >= p.visionParams[p.aspectMin] and aspect <= p.visionParams[p.aspectMax]
            if hullAreaCheckPassed and targetFullnessCheckPassed and aspectCheckPassed:
                final_targets.append(t)
            else:
                rejected_targets.append(t)
    return final_targets, rejected_targets, binImg

# returns: binarized frame (green retroreflective target)
def binarizeSubt(inCvBgr):
    green = cv2.extractChannel(inCvBgr, 1)
    red = cv2.extractChannel(inCvBgr, 2)
    outCvGray = cv2.subtract(green, red)
    outCvGray = cv2.erode(outCvGray, None, iterations=int(p.visionParams[p.binErIter]))
    outCvGray = cv2.dilate(outCvGray, None, iterations=int(p.visionParams[p.binDiIter]))
    return cv2.threshold(outCvGray, 0, 255, cv2.THRESH_OTSU)[1]

# returns: binarized frame (green retroreflective target)
def binarizeHSV(inCvBGR):
    outCvGray = cv2.inrange(cv2.cvtcolor(inCvBGR, cv2.COLOR_BGR2HSV),
                            (int(p.visionParams[p.hueMin]),int(p.visionParams[p.satMin]),int(p.visionParams[p.valMin])),
                            (int(p.visionParams[p.hueMax]),int(p.visionParams[p.satMax]),int(p.visionParams[p.valMax])))
    outCvGray = cv2.erode(outCvGray, None, iterations=int(p.visionParams[p.binErIter]))
    return cv2.dilate(outCvGray, None, iterations=int(p.visionParams[p.binDiIter]))

