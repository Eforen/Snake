import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Snake Game: Main Menu")

# Game state Global
# 0: Title Screen
# 1: Gameplay
# 2: Pause
# 3: Game Over
gameState = 0


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