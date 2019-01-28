import Constants, Image
from pygame import transform, image
class Tile:
    def __init__(self, gridPos: tuple, sprite, collision: bool):
        self.sprite = self.ImageToSprite(sprite)
        self.x, self.y = gridPos[0], gridPos[1]
    def isCollidable(self) -> bool:
        return collision
    def Update(self):
        pass
    def Render(self, screen):
        screen.blit(self.sprite, (self.x * Constants.TILESIZE, self.y * Constants.TILESIZE))
    def ImageToSprite(self, sprite):
        sprite = image.fromstring(sprite.tobytes(), sprite.size, sprite.mode)
        sprite = transform.scale(sprite, (Constants.TILESIZE, Constants.TILESIZE))
        return sprite

class AnimTile(Tile):
    def __init__(self, gridPos: tuple, collision: bool, SpriteSheet, row: int, frames: int, interval: int):
        self.SpriteSheet = SpriteSheet
        self.row = row
        self.frames = frames
        self.interval = interval
        self.initialSprite = self.SpriteSheet.returnSprite(0, self.row)
        super().__init__(gridPos, self.initialSprite, collision)
        self.tick = 0
        #The total amount of frames the animation runs for
        self.animLength = frames * interval

    def Update(self):
        self.tick += 1
        if self.tick >= self.animLength:
            self.tick = 0
        temp = self.SpriteSheet.returnSprite(self.tick // self.interval, self.row)
        self.sprite = self.ImageToSprite(temp)