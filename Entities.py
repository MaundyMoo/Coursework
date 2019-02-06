import Constants, pygame
class Entity:
    def __init__(self, x: int, y: int, sprite):
        self.x, self.y = x, y
        self.sprite = sprite
    def Update(self):
        pass
    def Render(self, screen, OffsetX: int, OffsetY: int):
        screen.blit(self.sprite, (self.x * Constants.TILESIZE + OffsetX, self.y * Constants.TILESIZE + OffsetY))

class Player(Entity):
    def __init__(self, x: int, y: int, sprite, map: list):
        super().__init__(x, y, sprite)
        self.map = map

    def move(self, dX: int, dY: int):
        #Checks for collions at the boundaries of the screen/map
        if self.y + dY < 0 or self.x + dX < 0:
            dX, dY = 0, 0
        elif self.y + dY > (len(self.map)-1) or self.x + dX > (len(self.map[0])-1):
            dX, dY = 0, 0
        #Checks for collisions with tiles that are 'collidable'
        elif self.map[self.y + dY][self.x + dX].isCollidable():
            dX, dY = 0, 0
        self.x = self.x + dX
        self.y = self.y + dY

    def getPosition(self) -> tuple:
        return (self.x, self.y)