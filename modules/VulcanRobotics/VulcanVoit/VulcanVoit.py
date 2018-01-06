import libjevois as jv
import numpy
import os
import cv2
import json
import time
from TuningParameters import TuningParameters as p
import Pipeline as pipeline

class VulcanVoit:

    sendTargets = False

    # Constructor
    def __init__(self):
        self.framecount = 0
        jv.LINFO("VulcanVoit ctor, sendTargets {}".format(VulcanVoit.sendTargets))
        jv.LINFO("VulcanVoit ctor, curDir {}".format(os.getcwd()))

    def process(self, inframe, outframe = None):
        inimg = inframe.getCvBGR()
        targets, rejTargets, binImg = pipeline.process(inimg)

        if outframe is not None:
            #cv2.putText(inimg, "Frame {}".format(self.framecount), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
            #outframe.sendCvBGR(inimg)
            #outframe.sendCvGRAY(pipeline.binarize(inimg))
            binout = cv2.cvtColor(binImg, cv2.COLOR_GRAY2BGR)
            for t in targets:
                cx, cy, width, height, hull = t
                cv2.drawContours(binout, [hull], 0, (0,255,0), 2)
                cv2.line(binout,(cx-5,cy),(cx+5,cy),(0,255,0))
                cv2.line(binout,(cx,cy-5),(cx,cy+5),(0,255,0))
            for rt in rejTargets:
                cv2.drawContours(binout, [rt[4]], 0, (0,0,255), 2)
            #dispimg = numpy.zeros((outimg.width, outimg.height, 3), dtype="uint8")
            dispimg = numpy.concatenate((inimg,binout),axis=1)
            outframe.sendCvBGR(dispimg)

        if VulcanVoit.sendTargets:
            jv.sendSerial(json.dumps({'Frame':self.framecount}))
        self.framecount += 1

    def parseSerial(self, str):
        cmd = str.split(" ")
        if cmd[0] == "sendtargets":
            if len(cmd) != 2:
                return "sendtargets usage: sendtargets <on|off>"
            if cmd[1] == "on":
                VulcanVoit.sendTargets = True
                return "sendtargets: turned on"
            else:
                if cmd[1] == "off":
                    VulcanVoit.sendTargets = False
                    return "sendtargets: turned off"
                else:
                    return "sendtargets: unknown option {}".format(cmd[1])

        # save camera control setting in a dict, so we can write out to script later
        # that module can run on startup, thereby setting camera controls to the
        # values we've tuned and saved
        # example: "storcam brightness 2"
        if cmd[0] == "storcam":
            if len(cmd) != 3:
                return "storcam usage: storcam <camctrl> <value>"
            p.camControls[cmd[1]] = cmd[2]
            #VulcanVoit.camControls[cmd[1]] = cmd[2]
            return "storcam: saved {0} {1}".format(cmd[1],cmd[2])

        # serialize the camera control dict to a series of setcam commands in script
        # so they can be loaded via a runscript command
        #   can also load upon module startup by placing a runscript command in script.cfg
        #       actually with v1.6 that doesn't work - runscript throws error if you try to run from script.cfg
        if cmd[0] == "savecamctrls":
            with open("/jevois/data/camControls.cfg","wt") as cfgFile:
                for k in p.camControls.keys(): #VulcanVoit.camControls.keys():
                    cfgFile.write("".join(["setcam ",k," ",p.camControls[k],"\n"]))
                cfgFile.flush()
            return "savecamctrls: saved to /jevois/data/camControls.cfg"

        # read previously serialized vision parameters from file
        # load into dictionary for module use
        # return as json to caller
        if cmd[0] == "readvisionparams":
            with open("/jevois/data/visionParams.json","rt") as paramFile:
                p.visionParams = json.load(paramFile)
            return json.dumps(p.visionParams)

        # set vision parameter value in dictionary for module use
        if cmd[0] == "setvisionparam":
            if len(cmd) != 3:
                return "setvisionparam usage: setvisionparam <param> <value>"
            p.visionParams[cmd[1]] = float(cmd[2])
            return "setvisionparam: saved {0} {1}".format(cmd[1],cmd[2])

        # save vision parameters to file
        if cmd[0] == "savevisionparams":
            with open("/jevois/data/visionParams.json","wt") as paramFile:
                json.dump(paramFile, p.visionParams)
                paramFile.flush()
            return "savevisionparams: saved to /jevois/data/visionParams.json"

        return "ERR parseSerial({})".format(str)