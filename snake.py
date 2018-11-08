import pygame
import math
import random

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
prevGameMode = 0

resMainMenu = pygame.image.load("StartC.png")
resPauseMenu = pygame.image.load("Pause.png")
resEndMenu = pygame.image.load("EndT.png")
resRulesMenu = pygame.image.load("Rules.png")
resControlsMenu = pygame.image.load("Controls.png")

# Globals
cellSizeX = 10
cellSizeY = 10
gridHeight = 50
gridWidth = 50
startPosX = 20
startPosY = 20
startLength = 3
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
                self.alive = False
        
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
        
theSnake = snake(0,0,3)
# End Snake Class

# Start Apple Logic

applesState = {
    # Apple Spec [X, Y, Vitality]
    'apples': [],
    'availableApplesDefault': [1, 2, 15, 5],
    'availableApples': None,
    'totalAvailableApples': 0
}

resAppleGold = pygame.image.load("Gold10.png")
resAppleNormal = pygame.image.load("Apple10.png")
resAppleRotting = pygame.image.load("Rotting10.png")
resApplePoison = pygame.image.load("Poison10.png")

resSoundAppleEat = pygame.mixer.Sound('AppleCoin.wav')
resSoundAppleEatGold = pygame.mixer.Sound("AppleGoldCoin.wav")
resSoundAppleEatRot = pygame.mixer.Sound("Rotting.wav")
resSoundDie = pygame.mixer.Sound("Dead.wav")

resMusic = pygame.mixer.music.load("384468.mp3")

def UpdateApples(applesState):
    EatApples(applesState)
    # Be nice to the player and decay the apples after the eat so an apple does not change a frame before its eaten
    DecayApples(applesState)
    return

def EatApples(applesState):
    for i in range(len(applesState['apples'])-1, -1, -1):
        if(applesState['apples'][i][0] == theSnake.x and applesState['apples'][i][1] == theSnake.y):
            #The snake ate the apple
            if(applesState['apples'][i][2] < 0):
                # invalid apple should never happen
                pass

            elif(applesState['apples'][i][2] <= 100):
                # if Poison kill
                theSnake.alive = False

            elif(applesState['apples'][i][2] <= 110):
                # else if rotting don't kill but don't grow
                if(soundsOn):
                    resSoundAppleEatRot.play()
                pass

            elif(applesState['apples'][i][2] <= 210):
                # else if normal grow one
                theSnake.length = theSnake.length + 3
                if(soundsOn):
                    resSoundAppleEat.play()
            else:
                # else if gold grow 3 and get 2 bonus points (Gold are worth 5 points)
                theSnake.length = theSnake.length + 9
                theSnake.bonusPoints = theSnake.bonusPoints + 5
                if(soundsOn):
                    resSoundAppleEatGold.play()
            
            applesState['apples'].pop(i)
            break
    return

def DecayApples(applesState):
    for i in range(len(applesState['apples'])-1, -1, -1):
        if(applesState['apples'][i][2] < 1):
            applesState['apples'].pop(i)
        else:
            applesState['apples'][i][2] = applesState['apples'][i][2] - 1
    return

def RenderApples(applesState, surface):
    for apple in applesState['apples']:
        if(apple[2] < 0):
            pass
        elif(apple[2] < 100):
            surface.blit(resApplePoison, (apple[0] * cellSizeX, apple[1] * cellSizeY))
        elif(apple[2] < 110):
            surface.blit(resAppleRotting, (apple[0] * cellSizeX, apple[1] * cellSizeY))
        elif(apple[2] <= 210):
            surface.blit(resAppleNormal, (apple[0] * cellSizeX, apple[1] * cellSizeY))
        else:
            surface.blit(resAppleGold, (apple[0] * cellSizeX, apple[1] * cellSizeY))
    return

# Start Apple Gen Logic

# Spec [Poison, Rotting, Normal, Gold]

def makeNewApple(applesState):
    # Insure apple waights are not empty and if they are then make new copy of the dificulty setting
    if(applesState['totalAvailableApples'] <= 0):
        applesState['availableApples'] = applesState['availableApplesDefault'].copy()
        applesState['totalAvailableApples'] = applesState['availableApples'][0] + applesState['availableApples'][1] + applesState['availableApples'][2] + applesState['availableApples'][3]
    
    # Calculate waighted apple
    apple = random.randint(1, applesState['totalAvailableApples'])
    if(apple <= applesState['availableApples'][0]):
        # Poison Apple
        applesState['availableApples'][0] = applesState['availableApples'][0] - 1
        applesState['totalAvailableApples'] = applesState['totalAvailableApples'] - 1
        return makePoisonApple(applesState)
    elif(apple <= applesState['availableApples'][0] + applesState['availableApples'][1]):
        # Rotting Apple
        applesState['availableApples'][1] = applesState['availableApples'][1] - 1
        applesState['totalAvailableApples'] = applesState['totalAvailableApples'] - 1
        return makeRottingApple(applesState)
    elif(apple <= applesState['availableApples'][0] + applesState['availableApples'][1] + applesState['availableApples'][2]):
        # Normal Apple
        applesState['availableApples'][2] = applesState['availableApples'][2] - 1
        applesState['totalAvailableApples'] = applesState['totalAvailableApples'] - 1
        return makeNormalApple(applesState)
    else:
        # Gold Apple
        applesState['availableApples'][3] = applesState['availableApples'][3] - 1
        applesState['totalAvailableApples'] = applesState['totalAvailableApples'] - 1
        return makeGoldApple(applesState)

def makePoisonApple(applesState):
    applesState['apples'].append([0,0, 100])
    # Place Apple
    # Dedup
    # Return index for chaining
    return DedupApples(*PlaceApple(applesState, len(applesState['apples']) - 1))
    
def makeRottingApple(applesState):
    applesState['apples'].append([0,0, 110])
    # Place Apple
    # Dedup
    # Return index for chaining
    return DedupApples(*PlaceApple(applesState, len(applesState['apples']) - 1))
    
def makeNormalApple(applesState):
    applesState['apples'].append([0,0, 210])
    # Place Apple
    # Dedup
    # Return index for chaining
    return DedupApples(*PlaceApple(applesState, len(applesState['apples']) - 1))
    
def makeGoldApple(applesState):
    applesState['apples'].append([0,0, random.randint(235, 275)])
    # Place Apple
    # Dedup
    # Return index for chaining
    return DedupApples(*PlaceApple(applesState, len(applesState['apples']) - 1))
    

def PlaceApple(applesState, i):
    # Move the apple to a pos we know is not valid
    applesState['apples'][i][0] = theSnake.x
    applesState['apples'][i][1] = theSnake.y
    
    # Place it well
    while IsBadPlace(applesState, i):
        applesState['apples'][i][0] = random.randint(0, gridWidth - 1)
        applesState['apples'][i][1] = random.randint(0, gridHeight - 1)

    # Return index for chaining
    return applesState, i

# Seprate function so that all the Placement Invalidation Logic can be put in the same place even though right now its just one check this gives options for expantion
def IsBadPlace(applesState, i):
    if(abs(applesState['apples'][i][0] - theSnake.x) <= appleMinPlacementDistance and abs(applesState['apples'][i][1] - theSnake.y) <= appleMinPlacementDistance):
        return True
    return False

def DedupApples(applesState, i):
    #TODO
    # Return index for chaining
    return applesState, i

# End Apple Gen Logic
# End Apple Logic

# Calculation Cache
targetAmountOfApplesLength = 0
targetAmountOfApples = 0

# Sound State Controls
musicOn = True
soundsOn = True

# Input Cache
lastKeysDown = pygame.key.get_pressed()
keysDown = pygame.key.get_pressed()

# Main Game loop
runGame = True
while runGame:
    pygame.time.delay(100)

    # Do Game Stuff
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
    
    lastKeysDown = keysDown
    keysDown = pygame.key.get_pressed()

    # Global Controls
    #if(keysDown[pygame.K_F1]):
    #    runGame = False # For debuging drop out of loop and die
    
    if(keysDown[pygame.K_r] == True and lastKeysDown[pygame.K_r] == False and gameState != 4 and gameState != 5):
        prevGameMode = gameState
        nextGameState = 4
    
    if(keysDown[pygame.K_c] == True and lastKeysDown[pygame.K_c] == False and gameState != 4 and gameState != 5):
        prevGameMode = gameState
        nextGameState = 5

    if(keysDown[pygame.K_m] == True and lastKeysDown[pygame.K_m] == False):
        if(musicOn):
            pygame.mixer.music.fadeout(1)
            musicOn = False
        else:
            pygame.mixer.music.play(-1)
            musicOn = True
    
    if(keysDown[pygame.K_s] == True and lastKeysDown[pygame.K_s] == False):
        if(soundsOn):
            resSoundAppleEat.fadeout(1)
            resSoundAppleEatGold.fadeout(1)
            resSoundAppleEatRot.fadeout(1)
            resSoundDie.fadeout(1)
            soundsOn = False
        else:
            soundsOn = True

    # Game States
    if (gameState == -1):
        # Run once a startup
        pygame.mixer.music.play(-1)


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

            # Wipe The Board
            applesState['apples'] = []
            targetAmountOfApples = 0
            targetAmountOfApplesLength = 0
        
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
        # Make Apples
        if(len(applesState['apples']) < targetAmountOfApples):
            makeNewApple(applesState)

        elif(theSnake.length > targetAmountOfApplesLength):
            targetAmountOfApplesLength = theSnake.length
            targetAmountOfApples = int(math.sqrt(targetAmountOfApplesLength * 5))
            if(len(applesState['apples']) < targetAmountOfApples):
                makeNewApple(applesState)

        # Clear Screen
        win.fill((0,0,0))

        # Check for pause input
        if(keysDown[pygame.K_ESCAPE]):
            # Pause the game
            nextGameState = 2

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

        # Update Apples
        UpdateApples(applesState)

        # Draw Items
        RenderApples(applesState, win)

        # Draw
        theSnake.draw(win)
        
        # Check for Dead
        # If dead go to game over
        if(theSnake.alive == False):
            nextGameState = 3
            if(soundsOn):
                resSoundDie.play()

        # Update Title with Score
        pygame.display.set_caption("Snake Game: Playing Score: "+str(theSnake.length + theSnake.bonusPoints)+" ( Len:"+ str(theSnake.length) +" | Bonus:"+ str(theSnake.bonusPoints) +" )")

        # Flush
        pygame.display.update()

    if (gameState == 2):
        # Draw Pause Screen only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            win.fill((0,0,0))
            # Draw Menu
            win.blit(resPauseMenu, (0,0))
            # Update
            pygame.display.update()
            
        # Check for esc input
        if(keysDown[pygame.K_ESCAPE]):
            nextGameState = 1
        
    if (gameState == 3):
        # Draw Gameover Screen only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            # win.fill((0,0,0))
            # Draw Menu
            win.blit(resEndMenu, (0,0))
            # Update
            pygame.display.update()
        
        # Check for arrow input
        if(keysDown[pygame.K_SPACE]):
            nextGameState = 0

    if (gameState == 4):
        # Draw Rules Screen only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            win.fill((0,0,0))
            # Draw Menu
            win.blit(resRulesMenu, (0,0))
            # Update
            pygame.display.update()
            
        # Check for esc input
        if(keysDown[pygame.K_ESCAPE] or keysDown[pygame.K_r]):
            nextGameState = prevGameMode

    if (gameState == 5):
        # Draw Controls Screen only on transition into mode for efficency
        if(gameState != lastGameState):
            # Clear Screen
            win.fill((0,0,0))
            # Draw Menu
            win.blit(resControlsMenu, (0,0))
            # Update
            pygame.display.update()
            
        # Check for esc input
        if(keysDown[pygame.K_ESCAPE] or keysDown[pygame.K_r]):
            nextGameState = prevGameMode


    # Last thing in loop
    # Update gamestate
    # Don't set unless needed for preformance
    if(lastGameState != gameState):
        lastGameState = gameState
    if(gameState != nextGameState):
        gameState = nextGameState