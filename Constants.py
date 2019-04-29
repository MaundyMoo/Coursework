import os

SCREEN_WIDTH = 64 * 17
SCREEN_HEIGHT = 64 * 11
LOG_WIDTH = 64 * 4
GAME_WIDTH = SCREEN_WIDTH - LOG_WIDTH

TILESIZE = 32

PlayerControls = [273, 274, 276, 275]
playerName = 'Default'

# Gets the directory of where the file is being run from
WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


# Joins any input path to the working directory
def getPath(path) -> str:
    return os.path.join(WORKING_DIRECTORY, path)
