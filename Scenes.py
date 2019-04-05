import pygame, Image, Tiles, Constants, Entities, Pathfinding, Mapper
from random import choice
class SceneBase:
    def __init__(self, WIDTH: int, HEIGHT: int):
        self.next = self
        self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
    def Update(self):
        pass
    def ProcessInputs(self, events, pressed_keys):
        pass
    def Render(self, screen):
        pass
    def SwitchScene(self, next):
        self.next = next
    def Terminate(self):
        self.SwitchScene(None)

class GameScene(SceneBase):
    def __init__(self, WIDTH: int, HEIGHT: int):

        self.spritesheet = Image.SpriteSheet(path = "res/testSheet.png", spriteSize = 32)
        self.OffsetX, self.OffsetY = 0, 0
        self.animTiles = []
        self.backRendered = False
        self.playerInputs = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

        self.Entities = []

        super().__init__(WIDTH, HEIGHT)

        self.TileMap, caverns = Mapper.generateCellularAutomata()
        self.entitypositions = Mapper.placeEnemiesCellular(caverns)

        for position in self.entitypositions:
            self.Entities.append(Entities.TestEnemy(x=position[1], y=position[0], Map=self.TileMap))

        playerPos = choice(caverns[0])
        while playerPos in self.entitypositions:
            playerPos = choice(caverns[0])

        self.player = Entities.Player(x = playerPos[1], y = playerPos[0], map = self.TileMap)
        self.graph = Pathfinding.Graph(self.TileMap)

    def ProcessInputs(self, events, pressedKeys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in self.playerInputs:
                #self.playerInputs = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
                #UP
                if event.key == self.playerInputs[0]:
                    self.player.move(0, -1, self.Entities)
                    self.player.setDirection(0)
                #DOWN
                elif event.key == self.playerInputs[1]:
                    self.player.move(0, 1, self.Entities)
                    self.player.setDirection(1)
                #LEFT
                elif event.key == self.playerInputs[2]:
                    self.player.move(-1, 0, self.Entities)
                    self.player.setDirection(2)
                #RIGHT
                elif event.key == self.playerInputs[3]:
                    self.player.move(1, 0, self.Entities)
                    self.player.setDirection(2, True)
                for entity in self.Entities:
                    if entity.inRange(self.player):
                        path = self.graph.Astar(source = entity.getPosition(), target = self.player.getPosition())
                        entity.move(path, self.Entities, self.player)
                self.offsetScene()
                self.backRendered = False

    def Update(self):
        for tiles in self.animTiles: tiles.Update()
        self.player.Update()
        if self.player.isDead: self.Terminate()
        for entity in self.Entities:
            entity.Update()
            if entity.isDead: self.Entities.remove(entity)

    def Render(self, screen):
        if not self.backRendered: self.backRender(screen)
        for tiles in self.animTiles: tiles.Render(screen, self.OffsetX, self.OffsetY)
        self.TileMap[self.player.getPosition()[0]][self.player.getPosition()[1]].Render(screen, self.OffsetX, self.OffsetY)
        self.player.Render(screen, self.OffsetX, self.OffsetY)
        for entity in self.Entities:
            self.TileMap[entity.getPosition()[0]][entity.getPosition()[1]].Render(screen, self.OffsetX, self.OffsetY)
            entity.Render(screen, self.OffsetX, self.OffsetY)

    def offsetScene(self):
        #Getting map dimensions, both tile and pixel dimensions
        #TEMPORY FOR NOW UNTIL MAP GENERATION IS IMPLEMENTED
        mapHeight, mapWidth = len(self.TileMap), len(self.TileMap[0])
        mapPixelHeight, mapPixelWidth = mapHeight * Constants.TILESIZE, mapWidth * Constants.TILESIZE
        #Getting the position and pixel position of the player
        playerY, playerX = self.player.getPosition()
        playerPixelX, playerPixelY = playerX * Constants.TILESIZE, playerY * Constants.TILESIZE
        #Checking for X offset
        if playerPixelX <= int(Constants.GAME_WIDTH / 2):
            self.OffsetX = 0
        elif playerPixelX >= (mapPixelWidth - int(Constants.GAME_WIDTH / 2)):
            self.OffsetX = -(mapPixelWidth - Constants.GAME_WIDTH)
        else:
            self.OffsetX = -int(((playerPixelX - int(Constants.GAME_WIDTH / 2)) / Constants.TILESIZE) + 1) * (Constants.TILESIZE)
        #Checking for Y offset
        if playerPixelY <= int(Constants.SCREEN_HEIGHT / 2):
            self.OffsetY = 0
        elif playerPixelY >= (mapPixelHeight - int(Constants.SCREEN_HEIGHT / 2)):
            self.OffsetY = -(mapPixelHeight - Constants.SCREEN_HEIGHT)
        else:
            self.OffsetY = -int(((playerPixelY - int(Constants.SCREEN_HEIGHT / 2)) / Constants.TILESIZE) + 1) * (Constants.TILESIZE)

    def backRender(self, screen):
        tileXStart = abs(int(self.OffsetX/Constants.TILESIZE))
        tileYStart = abs(int(self.OffsetY/Constants.TILESIZE))
        self.animTiles = []
        for y in range(tileYStart, tileYStart + int(Constants.SCREEN_HEIGHT/Constants.TILESIZE)):
            for x in range(tileXStart, tileXStart + int(Constants.GAME_WIDTH/Constants.TILESIZE)):
                if type(self.TileMap[y][x]) == Tiles.AnimTile: self.animTiles.append(self.TileMap[y][x])
                self.TileMap[y][x].Render(screen, self.OffsetX, self.OffsetY)
        self.backRendered = True