'''
This class is responsable for the majority of the UI elements that
pertain to player information
'''
import pygame,  Constants
class Logger:
    def __init__(self, pos: int, width: int, height: int):
        self.position = Constants.GAME_WIDTH
        self.width, self.height = Constants.LOG_WIDTH, Constants.SCREEN_HEIGHT
        #Initialise attributes with a default value (0 or null crashes unfortunately)
        #As the width of the health bar is given by the ratio health / maxHealth
        self.playerMaxHealth: int = 1
        self.playerHealth: int = 1

        self.log = []

        #Attributes for the health bar
        self.Font = pygame.font.SysFont("Impact", 20)
        self.textOffset = 5
        self.healthX = 10
        self.healthBarWidth = self.width - self.healthX * 2
        self.healthBarHeight = 20
        self.healthY = self.height - self.healthBarHeight * 2
        self.healthOffset = 10

    def Update(self, playerHealth: int, playerMaxHealth: int):
        self.playerHealth = playerHealth
        self.playerMaxHealth = playerMaxHealth

    def Render(self, screen):
        #draw.rect(screen, (r,g,b), (posX, posY, width, height))
        pygame.draw.rect(screen, (100,100,100), (self.position, 0, self.width, self.height))
        # Draws three rectangles for the health bar, Health bar in green, back in red, and border in black
        # Border
        pygame.draw.rect(screen, (0, 0, 0), (self.position + self.healthX - self.healthOffset / 2, self.healthY - self.healthOffset / 2,
                                             self.healthBarWidth + self.healthOffset, self.healthBarHeight + self.healthOffset))
        # Damage
        pygame.draw.rect(screen, (255, 0, 0), (self.position + self.healthX, self.healthY, self.healthBarWidth, self.healthBarHeight))
        # Health
        pygame.draw.rect(screen, (0, 255, 0), (self.position + self.healthX, self.healthY,
                                               self.healthBarWidth * (self.playerHealth / self.playerMaxHealth), self.healthBarHeight))
        # Text
        healthText = self.Font.render((str(self.playerHealth) + "/" + str(self.playerMaxHealth)), True, (0, 0, 100))
        screen.blit(healthText, (self.position + self.healthX + self.healthBarWidth / 2 - healthText.get_width() / 2,
                                 self.healthY - self.healthOffset / 4))

        #Log
        for i in range(0, len(self.log)):
            screen.blit(self.log[i], (self.position + 5, self.Font.get_height() * i + self.textOffset))

        #pygame.draw.rect(screen, (0, 0, 0), (self.position, self.Font.get_height() * self.logAmount + self.textOffset, self.width, 4))

    def logDeath(self, entity: str):
        msg = str(entity) + ' was killed.'
        pygMsg = self.Font.render(msg, True, (0, 0, 0))
        self.log.append(pygMsg)

    def logCombat(self, attacker: str, defender: str, damage: int):
        msg = str(attacker) + ' hit ' + str(defender) + ' for ' + str(damage) + '.'
        pygMsg = self.Font.render(msg, True, (0,0,0))
        self.log.append(pygMsg)

    def logDamage(self, entity: str, Damage: int):
        msg = str(entity) + ' took ' + str(Damage) + ' damage.'
        pygMsg = self.Font.render(msg, True, (0, 0, 0))
        self.log.append(pygMsg)