import Constants
class Entity:
    def __init__(self, x: int, y: int, sprite: str):
        self.x, self.y = x, y
        self.sprite = sprite
    def Update(self):
        pass
    def Render(self, screen):
        screen.blit(screen, (self.x * Constants.TILESIZE, self.y * Constants.TILESIZE))