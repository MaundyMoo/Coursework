import os
SCREEN_WIDTH = 64 * 16
SCREEN_HEIGHT = 64 * 9

TILESIZE = 64

#Gets the directory of where the file is being run from
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
#Joins any input path to the working directory
def getPath(path):
    return os.path.join(WORKING_DIRECTORY, path)

testmap = [[0,0,0,0,0,0,0,0,0,1,1,1,0],
           [1,1,1,0,0,0,0,0,0,0,1,0,0],
           [1,1,1,1,0,0,0,0,0,0,0,0,0],
           [1,1,1,2,2,2,0,0,0,0,0,0,0],
           [0,0,0,2,2,2,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,0]]
