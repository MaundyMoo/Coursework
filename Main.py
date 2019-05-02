def run(activeScene, width: int, height: int):
    # Creates the screen object
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Coursework")
    # Creates a clock object that will handle the frames per second
    clock = pygame.time.Clock()
    FULLSCREEN = False
    while activeScene is not None:
        pressedKeys = pygame.key.get_pressed()
        # Event filtering - Detects if user wants to close the game, otherwise sends inputs to be handled by scene
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            # Checks if window is being closed or if alt-f4 is pressed (pygame doesn't close on alt-f4 by default)
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressedKeys[pygame.K_LALT] or pressedKeys[pygame.K_RALT]
                if event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True
                elif (event.key == pygame.K_RETURN and alt_pressed) or event.key == pygame.K_F11:
                    FULLSCREEN = not FULLSCREEN
                    if FULLSCREEN:
                        pygame.display.set_mode((width, height), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((width, height))
                    activeScene.backRendered = False
            if quit_attempt:
                activeScene.Terminate()
            else:
                filtered_events.append(event)
        # Runs Scene methods
        activeScene.ProcessInputs(filtered_events, pressedKeys)
        activeScene.Update()
        activeScene.Render(screen)

        # Swap to next scene if necessary
        activeScene = activeScene.next

        # Swaps the buffer of the screen for the next one
        pygame.display.flip()
        # Keeps the process waiting to ensure the program runs at 60fps
        clock.tick(60)
        # print('fps: ', clock.get_fps())
    pygame.quit()


if __name__ == "__main__":
    import pygame, Scenes
    from Constants import SCREEN_WIDTH, SCREEN_HEIGHT

    pygame.init()
    pygame.mouse.set_visible(False)
    w, h = 1280, 720
    scene = Scenes.TitleScene()
    run(scene, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
