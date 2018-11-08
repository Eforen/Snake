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
startLength = 3
theSnake = None
apples = []
appleMinPlacementDistance = 6

# Start Snake Class
class snake(object):
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.body = [[x, y]]
        self.heading = 0 # Up, Right, Down, Left
        self.alive = True
        self.bonusPoints = 0
    
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

# Start Apple Logic
# Apple Spec [X, Y, Vitality]

resAppleGold = pygame.image.load("Gold.png")
resAppleNormal = pygame.image.load("Apple.png")
resAppleRotting = pygame.image.load("Rotting.png")
resApplePoison = pygame.image.load("Poison.png")

def UpdateApples():
    EatApples()
    # Be nice to the player and decay the apples after the eat so an apple does not change a frame before its eaten
    DecayApples()

def EatApples():
    for i in range(len(apples)-1, 0):
        if(apples[i][0] == theSnake.x and apples[i][1] == theSnake.y):
            #The snake ate the apple
            if(apples[i][2] < 0):
                # invalid apple should never happen
                pass
            elif(apples[i][2] < 100):
                # if Poison kill
                theSnake.alive = False
                pass
            elif(apples[i][2] < 110):
                # else if rotting don't kill but don't grow
                pass
            elif(apples[i][2] < 210):
                # else if normal grow one
                theSnake.length = theSnake.length + 1
                pass
            else:
                # else if gold grow 3 and get 2 bonus points (Gold are worth 5 points)
                theSnake.length = theSnake.length + 3
                theSnake.bonusPoints = theSnake.bonusPoints + 2
                pass
            
            apples.pop(i)
            break

def DecayApples():
    for i in range(len(apples)-1, 0):
        if(apple[i][2] < 1):
            apples.pop(i)
        else:
            apple[i][2] = apple[i][2] - 1

def RenderApples(surface):
    for apple in apples:
        if(apple[2] < 0):
            pass
        elif(apple[2] < 100):
            surface.blit(resApplePoison, (apple[0] * cellSizeX, apple[1] * cellSizeY))
        elif(apple[2] < 110):
            surface.blit(resAppleRotting, (apple[0] * cellSizeX, apple[1] * cellSizeY))
        elif(apple[2] < 210):
            surface.blit(resAppleNormal, (apple[0] * cellSizeX, apple[1] * cellSizeY))
        else:
            surface.blit(resAppleGold, (apple[0] * cellSizeX, apple[1] * cellSizeY))

# Start Apple Gen Logic

# Spec [Poison, Rotting, Normal, Gold]
availableApplesDefault = [5, 10, 50, 5]
availableApples = [0,0,0,0]

def makeNewApple():
    # Insure apple waights are not empty and if they are then make new copy of the dificulty setting
    totalAvailableApples = availableApples[0] + availableApples[1] + availableApples[2] + availableApples[3]
    if(totalAvailableApples <= 0):
        availableApples = availableApplesDefault.copy()
        totalAvailableApples = availableApples[0] + availableApples[1] + availableApples[2] + availableApples[3]
    
    # Calculate waighted apple
    apple = random.randint(1, totalAvailableApples)
    if(apple <= availableApples[0]):
        # Poison Apple
        availableApples[0] = availableApples[0] - 1
        return makePoisonApple()
    elif(apple <= availableApples[0] + availableApples[1]):
        # Rotting Apple
        availableApples[1] = availableApples[1] - 1
        return makeRottingApple()
    elif(apple <= availableApples[0] + availableApples[1] + availableApples[2]):
        # Normal Apple
        availableApples[2] = availableApples[2] - 1
        return makeNormalApple()
    else:
        # Gold Apple
        availableApples[3] = availableApples[3] - 1
        return makeGoldApple()

def makePoisonApple():
    apples.append([0,0, 100])
    # Place Apple
    # Dedup
    # Return index for chaining
    return Dedup(PlaceApple(len(apples) - 1))
    
def makeRottingApple():
    apples.append([0,0, 100])
    # Place Apple
    # Dedup
    # Return index for chaining
    return Dedup(PlaceApple(len(apples) - 1))
    
def makeNormalApple():
    apples.append([0,0, 100])
    # Place Apple
    # Dedup
    # Return index for chaining
    return Dedup(PlaceApple(len(apples) - 1))
    
def makeGoldApple():
    apples.append([0,0, 100])
    # Place Apple
    # Dedup
    # Return index for chaining
    return Dedup(PlaceApple(len(apples) - 1))
    

def PlaceApple(i):
    # Move the apple to a pos we know is not valid
    apple[i][0] = theSnake.x
    apple[i][1] = theSnake.y
    
    # Place it well
    while IsBadPlace(i):
        apples[i][0] = random.randint(0, gridWidth - 1)
        apples[i][1] = random.randint(0, gridHeight - 1)

    # Return index for chaining
    return i

# Seprate function so that all the Placement Invalidation Logic can be put in the same place even though right now its just one check this gives options for expantion
def IsBadPlace(i):
    if(abs(apple[i][0] - theSnake.x) <= appleMinPlacementDistance and abs(apple[i][1] - theSnake.y) <= appleMinPlacementDistance):
        return True
    return False

def DedupApple(i):
    #TODO
    # Return index for chaining
    return i

# End Apple Gen Logic
# End Apple Logic

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
        # Draw Title Screen and init only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            win.fill((0,0,0))
            # Draw Menu
            win.blit(resMainMenu, (0,0))
            # Update
            pygame.display.update()
            
            # Setup New Snake
            theSnake = snake(startPosX, startPosY, startLength)
        
        # Check for arrow input
        if(keysDown[pygame.K_UP]):
            theSnake.heading = 0
            nextGameState = 1
        if(keysDown[pygame.K_RIGHT]):
            theSnake.heading = 1
            nextGameState = 1
        if(keysDown[pygame.K_DOWN]):
            theSnake.heading = 2
            nextGameState = 1
        if(keysDown[pygame.K_LEFT]):
            theSnake.heading = 3
            nextGameState = 1

    if (gameState == 1):
        # Gameplay State

        # Clear Screen
        win.fill((0,0,0))

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

        # Make Apples
        

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