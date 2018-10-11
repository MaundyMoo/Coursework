from pygame import image
from PIL import Image as Img
import Constants
def ReadImage(path):
    path = CONSTANTS.getPath(path)
    #Changes any incorrect slashes in the path to correct ones, 
    #which should allow the code to work on linux as well
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(path).convert()
    return image