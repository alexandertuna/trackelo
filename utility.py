import os
import glob

import constants

def getDataFileNames():
    fpaths = os.path.join(os.path.dirname(__file__), constants.DATA_DIR, "*")
    return sorted(glob.glob(fpaths))

# def parseLineForName(line):
#     return line.split()[constants.LINE_INDEX_NAME]

def comparePlaces(place, otherplace):
    if place < otherplace:
        return constants.WIN
    elif place == otherplace:
        return constants.DRAW
    return constants.LOSS
