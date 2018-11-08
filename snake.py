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
resEndMenu = pygame.image.load("End.png")

# Globals
cellSizeX = 10
cellSizeY = 10
gridHeight = 50
gridWidth = 50
startPosX = 20
startPosY = 20
theSnake = None

# Start Snake Class
class snake(object):
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.body = [[x, y]]
        self.heading = 0 # Up, Right, Down, Left
        self.alive = True
    
    def move(self):
        # Deal with body length and pop last if too long
        while(len(self.body) > self.length - 1):
            self.body.pop(len(self.body) - 1)

        # Move and check for walls
        if(self.heading == 0):
            # Move Up
            if(self.y < 1):
                self.alive = False;
            self.y = self.y - 1
        
        if(self.heading == 1):
            # Move Right
            if(self.x > gridWidth - 2): # - 2 because one for 0 index and one for last col
                self.alive = False;
            self.x = self.x + 1
        
        if(self.heading == 2):
            # Move Down
            if(self.y > gridHeight - 2): # - 2 because one for 0 index and one for last row
                self.alive = False;
            self.y = self.y + 1
        
        if(self.heading == 3):
            # Move Left
            if(self.x < 1):
                self.alive = False;
            self.x = self.x - 1
        
        # Make sure the snake did not bite itself
        for segment in self.body:
            if(segment[0] == self.x and segment[1] == self.y):
                self.alive == False
        
        # Add new body segment where head currently is
        self.body.insert(0, [self.x, self.y])
        
    def newHeading(self, heading):
        # turn only if heading is at right angle to current heading
        if((self.heading % 2) != (heading % 2)):
            self.heading = heading

    def draw(self, surface):
        # Draw outline
        for segment in self.body:
            pygame.draw.rect(surface, (0, 55, 0), (segment[0] * cellSizeX-1, segment[1] * cellSizeY-1, cellSizeX + 2, cellSizeY + 2))

        # Draw body
        for segment in self.body:
            pygame.draw.rect(surface, (0, 64, 0), (segment[0] * cellSizeX, segment[1] * cellSizeY, cellSizeX, cellSizeY))

        # Draw head
        pygame.draw.rect(surface, (47, 160, 53), (self.x * cellSizeX-3, self.y * cellSizeY - 3, cellSizeX + 3, cellSizeY + 3))
        pygame.draw.rect(surface, (0, 127, 19), (self.x * cellSizeX-2, self.y * cellSizeY - 2, cellSizeX + 2, cellSizeY + 2))
        
        
# End Snake Class


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
        # Gameplay State

        # Clear Screen
        win.fill((0,0,0))
        
        # Init on transition into mode from start screen
        if(lastGameState == 0):
            # Setup New Snake
            theSnake = snake(startPosX, startPosY, 3)

        # Apply Input with basic sanitization
        if(((keysDown[pygame.K_UP] and keysDown[pygame.K_DOWN]) or (keysDown[pygame.K_RIGHT] and keysDown[pygame.K_LEFT])) == False):
            # Not trying to go both ways
            if(keysDown[pygame.K_UP]):
                theSnake.newHeading(0)
            if(keysDown[pygame.K_RIGHT]):
                theSnake.newHeading(1)
            if(keysDown[pygame.K_DOWN]):
                theSnake.newHeading(2)
            if(keysDown[pygame.K_LEFT]):
                theSnake.newHeading(3)

        # Actually Move
        theSnake.move()

        # Draw Items

        # Draw
        theSnake.draw(win)

        # Check for Apple

        # Check for Poison Apple
        
        # Check for Dead
        # If dead go to game over
        if(theSnake.alive == False):
            nextGameState = 3

        # Update Title with Score

        # Flush
        pygame.display.update()

    if (gameState == 2):
        # Draw Pause Screen

        # Violently Clear Screen for Debug
        win.fill((0,204,255))
        pygame.display.update()
        
    if (gameState == 3):
        # Draw Gameover Screen only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            win.fill((0,0,0))
            # Draw Menu
            win.blit(resEndMenu, (0,0))
            # Update
            pygame.display.update()
        
        # Check for arrow input
        if(keysDown[pygame.K_SPACE]):
            nextGameState = 0


    # Last thing in loop
    # Update gamestate
    # Don't set unless needed for preformance
    if(lastGameState != gameState):
        lastGameState = gameState
    if(gameState != nextGameState):
        gameState = nextGameState