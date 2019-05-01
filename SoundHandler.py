import pygame, Constants


class Sound:
    def __init__(self):
        # Some weird trick to fix delays with sound, idk why it works
        pygame.mixer.pre_init(22050, -16, 2, 1024)
        pygame.mixer.quit()
        pygame.mixer.init(22050, -16, 2, 1024)

    def PlayMusic(self, path: str):
        pygame.mixer.music.load(Constants.getPath(path))
        pygame.mixer.music.play()
    def PlaySound(self, path: str):
        pygame.mixer.Sound(Constants.getPath(path)).play()
