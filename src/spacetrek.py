import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TEXTCOLOR = (255, 255, 255)

#color
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
DARKGRAY  = ( 100,  100,  100)
BGCOLOR = BLACK

FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 45
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 8
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawScore(score,topScore):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    topscoreSurf = BASICFONT.render('Top Score: %s'%(topScore), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 180, 20)
    topscoreRect = topscoreSurf.get_rect()
    topscoreRect.topleft = (WINDOWWIDTH - 180, 50)
    SCREEN.blit(scoreSurf, scoreRect)
    SCREEN.blit(topscoreSurf, topscoreRect)

def showStartScreen():
    titleFont = pygame.font.Font("data/f.ttf", 120)
    titleSurf = titleFont.render('SPACE TREK', True, (192,192,192))
    titleRect = titleSurf.get_rect()
    titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    while True:
        SCREEN.fill(BGCOLOR)
        SCREEN.blit(titleSurf, titleRect)
        titleRect = titleSurf.get_rect()
        titleRect.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
    
        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        mainClock.tick(FPS)

def drawPressKeyMsg(): #for showstartscreen() and showgameoverscreen()
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 50)
    SCREEN.blit(pressKeySurf, pressKeyRect)

def showGameOverScreen():
    gameOverFont = pygame.font.Font("data/f.ttf", 120)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 80)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 105)

    SCREEN.blit(gameSurf, gameRect)
    SCREEN.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500) #not so soon key press
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0: #QUIT events in event queue?
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), FULLSCREEN)
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

#load backgroundimage
background = pygame.image.load('data/s2.png').convert()
backgroundRect = background.get_rect()

# set up fonts
BASICFONT = pygame.font.Font("data/f.ttf", 30)

# set up sounds
gameOverSound = pygame.mixer.Sound('data/gameover.wav')
pygame.mixer.music.load('data/background.mid')

# set up images
playerImage = pygame.image.load('data/player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('data/baddie.png')

# show the "Start" screen
showStartScreen()

topScore = 0
while True:
    # set up the start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score -= 200
                if event.key == ord('x'):
                    slowCheat = False
                    score -= 100
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        SCREEN.blit(background,backgroundRect)

        # Draw the score and top score.
        drawScore(score,topScore)

        # Draw the player's rectangle
        SCREEN.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            SCREEN.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    #game over
    showGameOverScreen()

    pygame.display.update()

    gameOverSound.stop()

