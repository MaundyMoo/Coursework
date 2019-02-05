from pygame import image, transform
from PIL import Image as Img
import Constants, os
def ReadImage(path: str):
    path = Constants.getPath(path)
    #Boiler plate code
    #Changes the slashes of the path string to all be the same which should
    #prevent any issues finding files
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    image = image.load(path)
    return image

class SpriteSheet:
    def __init__(self, path: str, spriteSize: int):
        self.spriteSize = spriteSize
        path = Constants.getPath(path)
        #Open as an image to allow for cropping and selecting individual parts of it later
        self.sheet = Img.open(path)
        #Allows me to access the alpha channel which will be necessary later for when I need to remove colours
        self.sheet = self.sheet.convert('RGBA')
        self.removeColour(list(self.sheet.getdata()))
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
        for y in range(0, int(len(pixelmap) / self.spriteSize) + 1):
            row = []
            for x in range(0, int(len(pixelmap[0]) / self.spriteSize) + 1):
                sprite = self.sheet.crop((x * self.spriteSize,y * self.spriteSize,(x * self.spriteSize)+self.spriteSize,(y * self.spriteSize)+self.spriteSize))
                row.append(sprite)
            sprites.append(row)
        return sprites

    # Removes certain colours from the spritesheet #FF00FF, #880088 are removed
    def removeColour(self, image):
        width, height = self.sheet.size
        image = [image[i * width:
            (i + 1) * width] for i in range(height)]
        for y in range(0,len(image)):
            for x in range(0, len(image[0])):
                #If the detected colour is #FF00FF or #880088, replace it with a transparent white pixel
                if image[y][x] == (255, 0, 255, 255) or image[y][x] == (136, 0, 136, 255):
                    self.sheet.putpixel((x,y), (255, 255, 255, 0))

    def  returnSprite(self, x: int, y: int):
        return self.ImageToSprite(self.spriteMap[y][x])

    def ImageToSprite(self, sprite):
        sprite = image.fromstring(sprite.tobytes(), sprite.size, sprite.mode)
        sprite = transform.scale(sprite, (Constants.TILESIZE, Constants.TILESIZE))
        return sprite