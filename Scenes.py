import pygame, Image
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
        self.test = Image.ReadImage('res/test.png')
        print(type(self.test))
    def ProcessInputs(self, events, pressedKeys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.SwitchScene(TestScene2(self.WIDTH, self.HEIGHT))
    def Render(self, screen):
        screen.fill((0,0,0))
        screen.blit(self.test, (int(self.WIDTH / 2), self.HEIGHT / 2))
        