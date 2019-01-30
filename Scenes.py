import pygame, Image, Tiles, Constants, Entities
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

class TestScene(SceneBase):
    def __init__(self, WIDTH: int, HEIGHT: int):
        super().__init__(WIDTH, HEIGHT)
        self.TileMap = []
        self.spritesheet = Image.SpriteSheet(path = "res/testSheet.png", spriteSize = 32)
        self.player = Entities.Player(x = 1, y = 1, sprite = self.spritesheet.returnSprite(0, 2))
        for y in range(0, int(HEIGHT/Constants.TILESIZE)):
            for x in range(0, int(WIDTH/Constants.TILESIZE)):
                '''
                self.TileMap.append(Tiles.Tile(gridPos = (x, y),
                                   sprite = self.spritesheet.returnSprite(0, 0), collision = False))
                '''
                self.TileMap.append(Tiles.AnimTile(gridPos = (x, y),
                                    collision = False,
                                    SpriteSheet = self.spritesheet,
                                    row = 0,
                                    frames = 2,
                                    interval = 5))
    def ProcessInputs(self, events, pressedKeys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.SwitchScene(TestScene2(self.WIDTH, self.HEIGHT))
    def Update(self):
        for Tiles in self.TileMap:
            Tiles.Update()
        self.player.Update()
    def Render(self, screen):
        screen.fill((0,0,0))
        for each in self.TileMap:
            each.Render(screen)
        self.player.Render(screen)
