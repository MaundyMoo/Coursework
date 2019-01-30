import Constants, pygame
class Entity:
    def __init__(self, x: int, y: int, sprite):
        self.x, self.y = x, y
        self.sprite = sprite
    def Update(self):
        pass
    def Render(self, screen):
        screen.blit(self.sprite, (self.x * Constants.TILESIZE, self.y * Constants.TILESIZE))

class Player(Entity):
    def __init__(self, x: int, y: int, sprite):
        super().__init__(x, y, sprite)

    def move(self, dX: int, dY: int):
        self.x = self.x + dX
        self.y = self.y + dY