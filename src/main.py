import pygame, sys, os
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, mixer disabled'

pygame.init()

#load images
#load backgroundimage
background = pygame.image.load('data/arcadebg.png')
backgroundRect = background.get_rect()

#set up sounds
pygame.mixer.music.load('data/mmusic.wav')

BASICFONT = pygame.font.Font("data/f.ttf", 30)
DARKGRAY  = ( 40,  40,  40)

size = (width, height) = background.get_size()
screen = pygame.display.set_mode((size), FULLSCREEN)
pygame.mouse.set_visible(False)

pygame.display.set_caption('21sArcade')

FPS = 40
myClock = pygame.time.Clock()

fontObj = pygame.font.SysFont('Century Gothic', 35)

################################################
#       menu
###############################################
def menu(surf, fObj, menuItems):
    selected = 0
    while True:
        # Get user input
        eList = pygame.event.get()
        for e in eList:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                selected -= 1
                if selected < 0:
                    selected = len(menuItems)-1
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                selected += 1
                if selected > len(menuItems)-1:
                    selected = 0
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return selected

        # Draw
        y = 350
        for i in range(len(menuItems)):
            tempS = fObj.render(menuItems[i], True, (120,120,120))
            surf.blit(tempS, (500 - tempS.get_width()/2, y))
            if selected == i:
                tempS = fObj.render(menuItems[i], True, (255,255,255))
                surf.blit(tempS, (500 - tempS.get_width()/2, y))
            y += tempS.get_height() + 10

        pygame.display.flip()

##########################################################
        # screens
#############################################################

def drawPressKeyMsg(): #for showstartscreen() and showgameoverscreen()
    pressKeySurf = BASICFONT.render('Press a key to play.', True, (192,192,192))
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (400,400)
    screen.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0: #QUIT events in event queue?
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def holdscreen():
    spacebg = pygame.image.load('data/hold.png')
    spacebgRect = spacebg.get_rect()
    while True:
        screen.blit(spacebg, spacebgRect)
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        myClock.tick(FPS)

def page2snake():
    abg = pygame.image.load('data/snakepage2.png')
    abgRect = abg.get_rect()
    while True:
        screen.blit(abg,abgRect)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    main()
                if event.key == K_RETURN:
                    holdscreen()
                    pygame.mixer.music.stop()
                    import snake
        pygame.display.update()
        myClock.tick(FPS)

def page2space():
    abg = pygame.image.load('data/spacepage2.png')
    abgRect = abg.get_rect()
    while True:
        screen.blit(abg,abgRect)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    main()
                if event.key == K_RETURN:
                    holdscreen()
                    pygame.mixer.music.stop()
                    import spacetrek
        pygame.display.update()
        myClock.tick(FPS)

def page2about():
    abg = pygame.image.load('data/aboutpage2.png')
    abgRect = abg.get_rect()
    while True:
        screen.blit(abg,abgRect)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    main()
        pygame.display.update()
        myClock.tick(FPS)

##################################################
#	main game loop
##################################################
def main():
    while 1:
        
        screen.blit(background, backgroundRect)
        
        #call menu function
        item = menu(screen, fontObj, ['Snake',
                                      'Space Trek',
                                      '',
                                      '',
                                      'ABOUT',
                                      'QUIT'])
        if item == 0:
            page2snake()
        elif item == 1:
            page2space()
        #elif item == 2:
        #elif item == 3:
            
                
        elif item == 4:
            page2about()
 #           a1=fontObj.render('Developed by:', True, (190,190,190))
 #           a2=fontObj.render('MANAN', True, (190,190,190))
 #           screen.blit(a1, (700, 540))
 #           screen.blit(a2, (710, 580))
 #           myClock.tick(0)
        elif item == 5:
            pygame.quit()
            sys.exit()
    
        pygame.display.update()

#############3
pygame.mixer.music.play(-1, 0.0)
main()
