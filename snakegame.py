# BASED ON:
# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US
#
# EDITED BY:
# Rikki Calteaux
# http://www.kirlac.com

import sys

import pygame
from pygame.locals import *

from config.vars import Vars
from colors.colorlist import Colors
from gameobjects.snake import Snake
from gameobjects.food import Food


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        (Vars.WINDOWWIDTH, Vars.WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    showStartScreen()


def runGame():
    P1SNAKE = Snake()
    FOOD = Food(P1SNAKE.coords)

    while True:  # Main game loop.
        for event in pygame.event.get():  # Event handling loop.
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    P1SNAKE.changeDirection(Vars.LEFT)
                elif event.key == K_RIGHT or event.key == K_d:
                    P1SNAKE.changeDirection(Vars.RIGHT)
                elif event.key == K_UP or event.key == K_w:
                    P1SNAKE.changeDirection(Vars.UP)
                elif event.key == K_DOWN or event.key == K_s:
                    P1SNAKE.changeDirection(Vars.DOWN)
                elif event.key == K_ESCAPE:
                    terminate()

        if P1SNAKE.checkHit():
            # Game over.
            return

        if P1SNAKE.checkEaten(FOOD.coords):
            P1SNAKE.move(True)
            FOOD.respawn(P1SNAKE.coords)
        else:
            P1SNAKE.move(False)

        DISPLAYSURF.fill(Vars.BGCOLOR)
        drawGrid()
        FOOD.draw(DISPLAYSURF)
        P1SNAKE.draw(DISPLAYSURF)
        drawScore(len(P1SNAKE.coords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(Vars.GAMEFPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to continue.', True,
                                    Colors.DARKGREY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (Vars.WINDOWWIDTH / 2, Vars.WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Snake!', True, Colors.WHITE,
                                  Colors.DARKGREEN)
    currentSelection = Vars.MENUSINGLEPLAYER
    while True:
        DISPLAYSURF.fill(Vars.BGCOLOR)
        titleRect1 = titleSurf1.get_rect()
        titleRect1.center = (Vars.WINDOWWIDTH / 2, Vars.WINDOWHEIGHT / 3)
        DISPLAYSURF.blit(titleSurf1, titleRect1)

        drawStartMenu(currentSelection)

        keyPress = checkForKeyPress()

        if keyPress == K_RETURN:
            makeSelection(currentSelection)
        elif keyPress is not None:
            currentSelection = changeSelectedItem(keyPress, currentSelection)

        pygame.display.update()
        FPSCLOCK.tick(Vars.COREFPS)


def changeSelectedItem(key, selected):
    if key == K_UP:
        selected -= 1
    elif key == K_DOWN:
        selected += 1

    return selected % len(Vars.MAINMENU)


def drawStartMenu(selection):
    for i, menuItem in enumerate(Vars.MAINMENU):
        if selection == i:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.ALMOSTBLACK, Colors.WHITE)
        else:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.WHITE)
        itemRect = itemSurf.get_rect()
        itemRect.center = (Vars.WINDOWWIDTH / 2,
            Vars.WINDOWHEIGHT / 3 * 2 + itemRect.height * i + 8 * i)
        DISPLAYSURF.blit(itemSurf, itemRect)


def makeSelection(selection):
    pygame.event.get()  # Clear event queue.
    if selection == Vars.MENUSINGLEPLAYER:
        Vars.MULTIPLAYERGAME = False
        runGame()
        showGameOverScreen()
    elif selection == Vars.MENUMULTIPLAYER:
        Vars.MULTIPLAYERGAME = True
        runGame()
    elif selection == Vars.MENUOPTIONS:
        terminate()
    elif selection == Vars.MENUEXIT:
        terminate()


def showOptionsScreen():
    somevar = 0


def showSnakeSelectScreen():
    somevar = 0


def showPauseScreen():
    somevar = 0


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, Colors.WHITE)
    overSurf = gameOverFont.render('Over', True, Colors.WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Vars.WINDOWWIDTH / 2, 10)
    overRect.midtop = (Vars.WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # Clear out any key presses in the event queue.

    while True:
        if checkForKeyPress():
            pygame.event.get()  # Clear event queue.
            return


def terminate():
    pygame.quit()
    sys.exit()


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, Colors.WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Vars.WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawGrid():
    # Draw vertical lines.
    for x in range(0, Vars.WINDOWWIDTH, Vars.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, Colors.ALMOSTBLACK, (x, 0),
                         (x, Vars.WINDOWHEIGHT))
    # Draw horizontal lines.
    for y in range(0, Vars.WINDOWHEIGHT, Vars.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, Colors.ALMOSTBLACK, (0, y),
                         (Vars.WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
