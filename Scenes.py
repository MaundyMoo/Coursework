import pygame, Image, Tiles, Constants, Entities, Pathfinding, Mapper, DatabaseHandler
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

class TitleScene(SceneBase):
    def __init__(self, WIDTH: int, HEIGHT: int):
        super().__init__(WIDTH, HEIGHT)
        self.Font = pygame.font.SysFont("Lucida Console", 56)
        self.TitleFont = pygame.font.SysFont("Lucida Console", 82)
        self.backgroundColour = (80, 180, 100)
        self.menuPointer = 0

        self.Title = self.TitleFont.render('Coursework', True, (200, 200, 100))
        self.offset = 120

        # Dictionary that holds both the text to be displayed in
        # the menu as well as the corresponding function that
        # the option should call
        self.dictOptions = {
                                0: ('Start', self.start),
                                1: ('Settings', self.settings),
                                2: ('Exit', self.exit)
                            }
        self.menu = []

    # Methods used as wrappers to call functions from the dictionary
    # As I cannot parse values through and this allows me to add extra
    # functionality if needed
    def start(self):
        self.SwitchScene(GameScene(self.WIDTH, self.HEIGHT))
    def settings(self):
        self.SwitchScene(SettingsScene(self.WIDTH, self.HEIGHT))
    def exit(self):
        self.Terminate()

    def Update(self):
        if self.menuPointer == -1: self.menuPointer = len(self.menu)-1
        if self.menuPointer == len(self.menu): self.menuPointer = 0
        self.menu = []
        for i in range(0, len(self.dictOptions)):
            # Long ternary operator for adding text to the menu probably cleaner without tbh
            self.menu.append(self.Font.render(self.dictOptions[i][0], True, (150, 50, 200))) \
                if i == self.menuPointer \
                else self.menu.append(self.Font.render(self.dictOptions[i][0], True, (50, 25, 75)))

    def ProcessInputs(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.menuPointer -= 1
                elif event.key == pygame.K_DOWN:
                    self.menuPointer += 1
                if event.key == pygame.K_RETURN:
                    # Calls the function held in the dictionary
                    self.dictOptions[self.menuPointer][1]()

    def Render(self, screen):
        # Fills the screen with a constant colour
        screen.fill(self.backgroundColour)
        # Draws the title to the screen
        # Screen.blit(surface, (left, top))
        screen.blit(self.Title, ((Constants.SCREEN_WIDTH/2) - self.Title.get_width()/2, 20))
        # Draws each option to the screen
        for i in range(0, len(self.menu)):
            screen.blit(self.menu[i], (20, self.Font.get_height() * i + self.offset))

class SettingsScene(TitleScene):
    def __init__(self, WIDTH: int, HEIGHT: int):
        super().__init__(WIDTH, HEIGHT)
        self.backgroundColour = (200, 150, 100)
        self.Database = DatabaseHandler.Database()

        self.offset = 20
        self.Title = self.TitleFont.render('', True, (200, 200, 100))

        self.dictOptions = {
                                0: ('Add Controls', self.foo),
                                1: ('New Profile', self.foo),
                                2: ('Main Menu', self.MainMenu)
                            }
        # Rectangle used as border
        # Rect((left, top), (width, height))
        self.control_border = pygame.Rect((Constants.SCREEN_WIDTH/2)-5, 5, Constants.SCREEN_WIDTH/2, self.HEIGHT-10)

        self.players = self.Database.get_players()
        self.playerPointer = 0
        # Default values just in case
        self.playerText = self.Font.render(self.players[0][0], True, (0, 0, 0))
        self.controls = self.Database.read_controls_player(self.players[0][0])
        self.bindingsText = [self.Font.render('UP:    ', True, (0, 0, 0)),
                             self.Font.render('DOWN:  ', True, (0, 0, 0)),
                             self.Font.render('LEFT:  ', True, (0, 0, 0)),
                             self.Font.render('RIGHT: ', True, (0, 0, 0))]

        self.controlTexts = [self.Font.render(str(self.controls[0]), True, (0, 0, 0)),
                             self.Font.render(str(self.controls[1]), True, (0, 0, 0)),
                             self.Font.render(str(self.controls[2]), True, (0, 0, 0)),
                             self.Font.render(str(self.controls[3]), True, (0, 0, 0))]

        self.leftArrow = self.Font.render('<', True, (0,0,0))
        self.rightArrow = self.Font.render('>', True, (0, 0, 0))

    def foo(self):
        print('temporary function')
    def MainMenu(self):
        Constants.PlayerControls = self.controls
        Constants.playerName = self.players[self.playerPointer][0]
        self.SwitchScene(TitleScene(self.WIDTH, self.HEIGHT))

    def Render(self, screen):
        super().Render(screen)
        # Draws a border where the controls / profile information will be shown
        pygame.draw.rect(screen, (0, 0, 0), self.control_border, 10)
        screen.blit(self.playerText, ((Constants.SCREEN_WIDTH*3)/4 - self.playerText.get_width()/2, 15))

        screen.blit(self.leftArrow,
                    (Constants.SCREEN_WIDTH / 2 + 15,
                     15))
        screen.blit(self.rightArrow,
                    (Constants.SCREEN_WIDTH - self.rightArrow.get_width() - 15,
                     15))

        for i in range(0, len(self.bindingsText)):
            screen.blit(self.bindingsText[i],
                        (Constants.SCREEN_WIDTH / 2 + 15,
                         15 + self.playerText.get_height() + self.controlTexts[i].get_height() * i))

        for i in range(0, len(self.controlTexts)):
            screen.blit(self.controlTexts[i],
                        (Constants.SCREEN_WIDTH/2 + 15 + self.bindingsText[0].get_width(),
                         15 + self.playerText.get_height() + self.controlTexts[i].get_height() * i))


    def ProcessInputs(self, events, pressed_keys):
        super().ProcessInputs(events, pressed_keys)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.playerPointer -= 1
                elif event.key == pygame.K_RIGHT:
                    self.playerPointer += 1

    def Update(self):
        super().Update()
        if self.playerPointer == -1: self.playerPointer = len(self.players)-1
        if self.playerPointer == len(self.players): self.playerPointer = 0
        # Updates the text to be shown
        self.playerText = self.Font.render((self.players[self.playerPointer][0]), True, (0, 0, 0))
        self.controls = self.Database.read_controls_player(self.players[self.playerPointer][0])
        self.controlTexts = [self.Font.render(pygame.key.name(self.controls[0]), True, (0, 0, 0)),
                             self.Font.render(pygame.key.name(self.controls[1]), True, (0, 0, 0)),
                             self.Font.render(pygame.key.name(self.controls[2]), True, (0, 0, 0)),
                             self.Font.render(pygame.key.name(self.controls[3]), True, (0, 0, 0))]

class GameScene(SceneBase):
    def __init__(self, WIDTH: int, HEIGHT: int):

        self.spritesheet = Image.SpriteSheet(path = "res/testSheet.png", spriteSize = 32)
        self.OffsetX, self.OffsetY = 0, 0
        self.animTiles = []
        self.backRendered = False
        self.playerInputs = Constants.PlayerControls

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