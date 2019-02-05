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
    def __init__(self, x: int, y: int, sprite, map: list):
        super().__init__(x, y, sprite)
        self.map = map

    def move(self, dX: int, dY: int):
        #Checks for collions at the boundaries of the screen/map
        if self.y + dY < 0 or self.x + dX < 0:
            print('offscreen UP or LEFT')
        elif self.y + dY > (len(self.map)-1) or self.x + dX > (len(self.map[0])-1):
            print('offscreen DOWN or RIGHT')
        #Checks for collisions with tiles that are 'collidable'
        elif self.map[self.y + dY][self.x + dX].isCollidable():
            print('Collides')
        else:
            self.x = self.x + dX
            self.y = self.y + dY
