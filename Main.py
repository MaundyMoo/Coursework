def run(width: int, height: int):
    #Creates the screen object 
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Coursework")
    #Creates a clock object that will handle the frames per second
    clock = pygame.time.Clock()
    while True:
        #Swaps the buffer of the screen for the next one 
        pygame.display.flip()
        #Keeps the process waiting to ensure the program runs at 60fps
        clock.tick(60)

if __name__ == "__main__":
    import pygame
    pygame.init()
    pygame.mouse.set_visible(False)
    run(width = 1280, height = 720)