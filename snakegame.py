# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US

import random
import sys

import pygame
from pygame.locals import *

from config.vars import Vars
from colors.list import Colors
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
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    P1_SNAKE = Snake()

    # Spawn food in a random place.
    apple = getRandomLocation()

    while True:  # Main game loop.
        for event in pygame.event.get():  # Event handling loop.
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    P1_SNAKE.changeDirection(Vars.LEFT)
                elif event.key == K_RIGHT or event.key == K_d:
                    P1_SNAKE.changeDirection(Vars.RIGHT)
                elif event.key == K_UP or event.key == K_w:
                    P1_SNAKE.changeDirection(Vars.UP)
                elif event.key == K_DOWN or event.key == K_s:
                    P1_SNAKE.changeDirection(Vars.DOWN)
                elif event.key == K_ESCAPE:
                    terminate()

        if P1_SNAKE.checkHit():
            # Game over.
            return

        if P1_SNAKE.checkEaten(apple):
            P1_SNAKE.move(True)
            # Respawn food.
            apple = getRandomLocation()
        else:
            P1_SNAKE.move(False)

        DISPLAYSURF.fill(Vars.BGCOLOR)
        drawGrid()
        drawApple(apple)
        drawWorm(P1_SNAKE.coords)
        drawScore(len(P1_SNAKE.coords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(Vars.FPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a Key to play.', True,
                                    Colors.DARKGREY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (Vars.WINDOWWIDTH - 200, Vars.WINDOWHEIGHT - 30)
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
    titleSurf2 = titleFont.render('Snake', True, Colors.GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(Vars.BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (Vars.WINDOWWIDTH / 2, Vars.WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (Vars.WINDOWWIDTH / 2, Vars.WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # Clear event queue.
            return
        pygame.display.update()
        FPSCLOCK.tick(Vars.FPS)
        degrees1 += 3  # Rotate by 3 degrees each frame.
        degrees2 += 7  # Rotate by 7 degrees each frame.


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, Vars.CELLWIDTH - 1),
            'y': random.randint(0, Vars.CELLHEIGHT - 1)}


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


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, Colors.WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (Vars.WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(coords):
    for coord in coords:
        x = coord['x'] * Vars.CELLSIZE
        y = coord['y'] * Vars.CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, Vars.CELLSIZE, Vars.CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, Colors.DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(
            x + 4, y + 4, Vars.CELLSIZE - 8, Vars.CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, Colors.GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * Vars.CELLSIZE
    y = coord['y'] * Vars.CELLSIZE
    appleRect = pygame.Rect(x, y, Vars.CELLSIZE, Vars.CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, Colors.RED, appleRect)


def drawGrid():
    # Draw vertical lines.
    for x in range(0, Vars.WINDOWWIDTH, Vars.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, Colors.DARKGREY, (x, 0),
                         (x, Vars.WINDOWHEIGHT))
    # Draw horizontal lines.
    for y in range(0, Vars.WINDOWHEIGHT, Vars.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, Colors.DARKGREY, (0, y),
                         (Vars.WINDOWWIDTH, y))


if __name__ == '__main__':
    main()
