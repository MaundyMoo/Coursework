import Constants, Image
class Tile:
    def __init__(self, gridPos: tuple, spritePath: str, collision: bool):
        spritePath = Constants.getPath(spritePath) 
        self.sprite = Image.ReadImage(spritePath) 
        self.x, self.y = gridPos[0], gridPos[1]
    def isCollidable(self) -> bool:
        return collision
    def Render(self, screen):
        screen.blit(self.sprite, (self.x * Constants.TILESIZE, self.y * Constants.TILESIZE))