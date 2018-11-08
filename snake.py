import pygame
pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Snake Game: Main Menu")

# Main Game loop
runGame = True
while runGame:
    pygame.time.delay(100)

    # Do Game Stuff