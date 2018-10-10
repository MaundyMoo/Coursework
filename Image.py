from pygame import image
from PIL import Image as Img
import Constants
def ReadImage(path):
    path = CONSTANTS.getPath(path)
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pygame.image.load(path).convert()
    return image