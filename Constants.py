import os
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
def getPath(path):
    return os.path.join(WORKING_DIRECTORY, path)