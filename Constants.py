import os
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
#Gets the directory of where the file is being run from
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
#Joins any input path to the working directory
def getPath(path):
    return os.path.join(WORKING_DIRECTORY, path)