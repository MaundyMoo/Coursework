import Constants, Image
from pygame import transform
class Tile:
    def __init__(self, gridPos: tuple, sprite, collision: bool):
        self.sprite = sprite
        self.sprite = transform.scale(self.sprite, (Constants.TILESIZE, Constants.TILESIZE))
        self.x, self.y = gridPos[0], gridPos[1]
    def isCollidable(self) -> bool:
        return collision
    def Render(self, screen):
        screen.blit(self.sprite, (self.x * Constants.TILESIZE, self.y * Constants.TILESIZE))