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

class SpriteSheet:
    def __init__(self, path: str, spriteSize: int):
        self.spriteSize = spriteSize
        path = Constants.getPath(path)
        #Open as an image to allow for cropping and selecting individual parts of it later
        self.sheet = Img.open(path)
        #Allows me to access the alpha channel which will be necessary later for when I need to remove colours
        self.sheet = self.sheet.convert('RGBA')
        self.spriteMap = self.getSpriteTiles()
        self.sheet.close()

    #Returns a list of every sprite on the sheet,
    # although probably could crop the sprites individually instead
    def getSpriteTiles(self) -> list:
        sprites = []
        #Gets a 1D list of pixels
        pixels = list(self.sheet.getdata())
        #converts the 1D list into a 2D list
        width, height = self.sheet.size
        pixelmap = [pixels[i * width:
            (i+1) * width] for i in range(height)]
        for y in range(0, (int(len(pixelmap)) / self.spriteSize)+1):
            row = []
            for x in range(0, (int(len(pixelmap[0])) / self.spriteSize)+1):
                sprite = self.sheet.crop((x * self.spriteSize,y * self.spriteSize, (x * (self.spriteSize+1)),(y * (self.spriteSize+1))))
                row.append(sprite)
            sprites.append(row)
        return sprites
    def  returnSprite(self, x: int, y: int):
        return self.spriteMap[y][x]