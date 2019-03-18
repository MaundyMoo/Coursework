import Constants, pygame, Image
class Entity:
    def __init__(self, x: int, y: int, spriteSheet: str, spriteSize: int, interval: int):
        self.x, self.y = x, y

        #Animation Attributes
            #Size represents the size of the spritesheets sprites not the sprites ingame
        self.size = spriteSize
            #Interval is the time each frame is rendered for
        self.interval = interval
            #The spritesheet the entity reads from
        self.spritesheet = Image.SpriteSheet(spriteSheet, self.size)
            #Pygame allows flipping surfaces, which will be useful for left / right
        self.flipped = False
            #The number of frames can inferred from the width of the spritesheet divided by the size of the sprites
        self.frames = int(self.spritesheet.returnSize()[0]/self.size)
            #The length it takes to run through all the sprites in the row
        self.animLength = self.frames * self.interval
            #The row the sprites should be taken from
        self.row = 0
            #A value that will dictate what sprite should be shown
        self.tick = 0
            #A default sprite so the program has something to render on the first frame
        self.sprite = self.spritesheet.returnSprite(0, self.row)

    def Update(self):
        self.animate()

    def Render(self, screen, OffsetX: int, OffsetY: int):
        screen.blit(self.sprite, (self.x * Constants.TILESIZE + OffsetX, self.y * Constants.TILESIZE + OffsetY))

    def animate(self):
        self.tick += 1
        if self.tick >= self.animLength:
            self.tick = 0
        self.sprite = self.spritesheet.returnSprite(self.tick // self.interval, self.row)
        self.sprite = pygame.transform.flip(self.sprite, self.flipped, False)

    def setDirection(self, dir: int, flip: bool = False):
        if dir < (self.spritesheet.returnSize()[1]/self.size):
            self.row = dir
            self.flipped = flip
        else:
            print('Error, invalid direction')

class Player(Entity):
    def __init__(self, x: int, y: int, map: list):
        #Attributes necessary for animations
        spritesheetPath = 'res/playerSheet.png'
        size = 32
        interval = 10

        super().__init__(x, y, spritesheetPath, size, interval)
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

class Enemy(Entity):
    def __init__(self, x, y, spritesheet, spriteSize, map, interval, animRow):
        super().__init__(x, y, spritesheet, spriteSize, interval)
        self.row = animRow
        self.map = map

    def getPosition(self) -> tuple:
        return (self.x, self.y)

class TestEnemy(Enemy):
    def __init__(self, x: int, y: int, Map: list):
        # Attributes necessary for animations
        spritesheetPath = 'res/enemySheet.png'
        spriteSize = 32
        interval = 10
        frames = 10
        animRow = 0
        super().__init__(x, y, spritesheetPath, spriteSize, Map, interval, animRow)