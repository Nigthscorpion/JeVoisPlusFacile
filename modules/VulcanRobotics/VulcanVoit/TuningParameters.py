class TuningParameters:

    binMethod = "binMethod"
    binErIter = "binErodeIterations"
    binDiIter = "binDilateIterations"
    hueMin = "hueMin"
    hueMax = "hueMax"
    satMin = "satMin"
    satMax = "satMax"
    valMin = "valMin"
    valMax = "valMax"
    fullnessMin = "fullnessMin"
    fullnessMax = "fullnessMax"
    areaMin = "areaMin"
    areaMax = "areaMax"
    aspectMin = "aspectMin" # aspect ratio, width/height
    aspectMax = "aspectMax"

    visionParams = {binMethod:0.0,binErIter:0.0,binDiIter:0.0,hueMin:0.0,hueMax:0.0,satMin:0.0,
                    satMax:0.0,valMin:0.0,valMax:0.0,fullnessMin:0.0,fullnessMax:0.0,
                    areaMin:0.0,areaMax:0.0,aspectMin:0.0,aspectMax:0.0}
    camControls = {}

