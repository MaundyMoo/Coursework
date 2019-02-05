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
        for y in range(0, len(Constants.testmap)):
            row = []
            for x in range(0, len(Constants.testmap[0])):
                if Constants.testmap[y][x] == 0:
                    row.append(Tiles.Tile(gridPos=(x, y),
                                              collision=False,
                                              sprite=self.spritesheet.returnSprite(0, 0)))
                elif Constants.testmap[y][x] == 1:
                    row.append(Tiles.Tile(gridPos=(x, y),
                                              collision=True,
                                              sprite=self.spritesheet.returnSprite(1, 0)))
                elif Constants.testmap[y][x] == 2:
                    row.append(Tiles.AnimTile(gridPos=(x, y),
                                              collision=False,
                                              SpriteSheet=self.spritesheet,
                                              row=1,
                                              frames=2,
                                              interval=4))
            self.TileMap.append(row)
        self.player = Entities.Player(x = 0, y = 0, sprite = self.spritesheet.returnSprite(0, 2), map = self.TileMap)
    def ProcessInputs(self, events, pressedKeys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.player.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.player.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.player.move(1, 0)

    def Update(self):
        for row in self.TileMap:
            for tiles in row:
                tiles.Update()
        self.player.Update()
    def Render(self, screen):
        screen.fill((0,0,0))
        for row in self.TileMap:
            for tiles in row:
                tiles.Render(screen)
        self.player.Render(screen)
