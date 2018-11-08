import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Snake Game: Main Menu")

# Game state Global
# -0: Bootstrap Init
#  0: Title Screen
#  1: Gameplay
#  2: Pause
#  3: Game Over

nextGameState = 0
gameState = -1
lastGameState = -1

resMainMenu = pygame.image.load("Start.png")

# Main Game loop
runGame = True
while runGame:
    pygame.time.delay(100)

    # Do Game Stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
        
    keysDown = pygame.key.get_pressed()

    if(keysDown[pygame.K_F1]):
        runGame = False # For debuging drop out of loop and die

    if (gameState == 0):
        # Draw Title Screen only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            win.fill((0,0,0))
            # Draw Menu
            win.blit(resMainMenu, (0,0))
            # Update
            pygame.display.update()
        
        # Check for arrow input
        if(keysDown[pygame.K_UP] or keysDown[pygame.K_RIGHT] or keysDown[pygame.K_DOWN] or keysDown[pygame.K_LEFT] ):
            nextGameState = 1

    if (gameState == 1):
        # Do Gameplay Logic
        # Draw Gameplay State
        
        # Violently Clear Screen for Debug
        win.fill((198,0,255))
        pygame.display.update()

    if (gameState == 2):
        # Draw Pause Screen

        # Violently Clear Screen for Debug
        win.fill((0,204,255))
        pygame.display.update()
        
    if (gameState == 3):
        # Draw Gameover Screen

        # Violently Clear Screen for Debug
        win.fill((48,255,0))
        pygame.display.update()


    # Last thing in loop
    # Update gamestate
    # Don't set unless needed for preformance
    if(lastGameState != gameState):
        lastGameState = gameState
    if(gameState != nextGameState):
        gameState = nextGameState