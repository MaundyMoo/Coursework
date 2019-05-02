import Constants, pygame, Image, Logger, SoundHandler


class Entity:
    def __init__(self, x: int, y: int, spriteSheet: str, spriteSize: int, interval: int):
        self.x, self.y = x, y
        self.name: str
        # Animation Attributes
        # Size represents the size of the spritesheets sprites not the sprites ingame
        self.size = spriteSize
        # Interval is the time each frame is rendered for
        self.interval = interval
        # The spritesheet the entity reads from
        self.spritesheet = Image.SpriteSheet(spriteSheet, self.size)
        # Pygame allows flipping surfaces, which will be useful for left / right
        self.flipped = False
        # The number of frames can inferred from the width of the spritesheet divided by the size of the sprites
        self.frames = int(self.spritesheet.returnSize()[0] / self.size)
        # The length it takes to run through all the sprites in the row
        self.animLength = self.frames * self.interval
        # The row the sprites should be taken from
        self.row = 0
        # A value that will dictate what sprite should be shown
        self.tick = 0
        # A default sprite so the program has something to render on the first frame
        self.sprite = self.spritesheet.returnSprite(0, self.row)

        self.Sound = SoundHandler.Sound()

    def __str__(self):
        return self.name

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
        if dir < (self.spritesheet.returnSize()[1] / self.size):
            self.row = dir
            self.flipped = flip
        else:
            print('Error, invalid direction')

    def getPosition(self) -> tuple:
        return (self.y, self.x)


class Player(Entity):
    def __init__(self, x: int, y: int, map: list):
        # Attributes necessary for animations
        spritesheetPath = 'res/playerSheet.png'
        size = 32
        interval = 10

        super().__init__(x, y, spritesheetPath, size, interval)
        self.map = map

        self.logger = Logger.Logger(Constants.GAME_WIDTH, Constants.LOG_WIDTH, Constants.SCREEN_HEIGHT)

        self.maxHealth = 100
        self.currentHealth = self.maxHealth
        self.isDead = False
        self.attack = 3
        self.name = Constants.playerName

    def Update(self):
        super().Update()
        if self.currentHealth <= 0:
            self.Sound.PlaySound('res/SFX/death.wav')
            self.isDead = True
        self.logger.Update(self.currentHealth, self.maxHealth)

    def Render(self, screen, OffsetX, OffsetY):
        super().Render(screen, OffsetX, OffsetY)
        self.logger.Render(screen)

    def move(self, dX: int, dY: int, entities: list):
        # Checks for collions at the boundaries of the screen/map
        if self.y + dY < 0 or self.x + dX < 0:
            dX, dY = 0, 0
        elif self.y + dY > (len(self.map) - 1) or self.x + dX > (len(self.map[0]) - 1):
            dX, dY = 0, 0
        # Checks for collisions with tiles that are 'collidable'
        elif self.map[self.y + dY][self.x + dX].isCollidable():
            dX, dY = 0, 0
        # Checks for collisions with any entities
        else:
            for entity in entities:
                if (self.y + dY, self.x + dX) == entity.getPosition() and issubclass(type(entity), Enemy):
                    dX, dY = 0, 0
                    self.combat(entity)
        if not (dX == 0 and dY == 0): self.Sound.PlaySound('res/SFX/footstep.wav')
        self.x = self.x + dX
        self.y = self.y + dY

    def combat(self, enemy):
        self.Sound.PlaySound('res/SFX/attack.wav')
        if enemy.currentHealth < self.attack:
            enemy.die()
            self.logger.logCombat(attacker=self, defender=enemy, damage=self.attack)
            self.logger.logDeath(enemy)
        else:
            enemy.currentHealth -= self.attack
            self.logger.logCombat(attacker=self, defender=enemy, damage=self.attack)
            if not enemy.combat:
                enemy.combat = True
                self.currentHealth -= enemy.attack
                self.logger.logCombat(attacker=enemy, defender=self, damage=enemy.attack)

    def attacked(self, enemy):
        self.Sound.PlaySound('res/SFX/enemy_attack.wav')
        self.currentHealth -= enemy.attack
        self.logger.logCombat(enemy, self, enemy.attack)


class Enemy(Entity):
    def __init__(self, x, y, spritesheet, spriteSize, map, interval, animRow):
        super().__init__(x, y, spritesheet, spriteSize, interval)
        self.row = animRow
        self.map = map

        self.isDead = False
        self.currentHealth: int
        self.maxHealth: int

        self.combat = False

        self.agrorange = 8

    def Update(self):
        super().Update()
        self.combat = False
        if self.currentHealth <= 0:
            self.isDead = True

    def move(self, path, entities: list, player):
        positions = []
        if not path[0] == player.getPosition():
            for entity in entities:
                positions.append(entity.getPosition())
            if not path[0] in positions:
                self.y, self.x = path[0]
        else:
            if not self.combat:
                self.combat = True
                player.attacked(self)

    def die(self):
        self.isDead = True

    def inRange(self, player) -> bool:
        distanceToPlayer = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        if distanceToPlayer < self.agrorange:
            return True
        else:
            return False


class TestEnemy(Enemy):
    def __init__(self, x: int, y: int, Map: list):
        # Attributes necessary for animations
        spritesheetPath = 'res/enemySheet.png'
        spriteSize = 32
        interval = 10
        frames = 10
        animRow = 0
        super().__init__(x, y, spritesheetPath, spriteSize, Map, interval, animRow)

        self.maxHealth = 10
        self.currentHealth = self.maxHealth
        self.attack = 3
        self.name = 'test'
