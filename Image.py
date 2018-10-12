from pygame import image as pyimg
from PIL import Image as Img
import Constants, os
def ReadImage(path: str):
    path = Constants.getPath(path)
    #Boiler plate code
    #Changes the slashes of the path string to all be the same which should
    #prevent any issues finding files
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = pyimg.load(path)
    return image