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

from config.snakeconfig import Config
from colors.colorlist import Colors
from gameobjects.snake import Snake
from gameobjects.food import Food


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    Config.loadSettings()

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode(
        (Config.SCREENSIZE['width'], Config.SCREENSIZE['height']))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    showStartScreen()


def runGame():
    global DISPLAYSURF

    if Config.MULTIPLAYER:
        SNAKES = {'P1': Snake(), 'P2': Snake()}
    else:
        SNAKES = {'P1': Snake()}
    FOOD = Food(SNAKES)

    while True:  # Main game loop.
        events = pygame.event.get(KEYDOWN)
        if len(events) > 0:
            for event in events:
                if event.key == K_LEFT:
                    SNAKES['P1'].changeDirection(Config.LEFT)
                elif event.key == K_RIGHT:
                    SNAKES['P1'].changeDirection(Config.RIGHT)
                elif event.key == K_UP:
                    SNAKES['P1'].changeDirection(Config.UP)
                elif event.key == K_DOWN:
                    SNAKES['P1'].changeDirection(Config.DOWN)
                elif event.key == K_a:
                    if Config.MULTIPLAYER:
                        SNAKES['P2'].changeDirection(Config.LEFT)
                    else:
                        SNAKES['P1'].changeDirection(Config.LEFT)
                elif event.key == K_d:
                    if Config.MULTIPLAYER:
                        SNAKES['P2'].changeDirection(Config.RIGHT)
                    else:
                        SNAKES['P1'].changeDirection(Config.RIGHT)
                elif event.key == K_w:
                    if Config.MULTIPLAYER:
                        SNAKES['P2'].changeDirection(Config.UP)
                    else:
                        SNAKES['P1'].changeDirection(Config.UP)
                elif event.key == K_s:
                    if Config.MULTIPLAYER:
                        SNAKES['P2'].changeDirection(Config.DOWN)
                    else:
                        SNAKES['P1'].changeDirection(Config.DOWN)
                elif event.key == K_ESCAPE:
                    resumeGame = showPauseScreen(FOOD, SNAKES)
                    if not resumeGame:
                        return
                    else:
                        pygame.time.wait(100)
                        # Clear out any key presses in the event queue.
                        checkForKeyPress()

        for snakeID in SNAKES:
            if SNAKES[snakeID].checkHit():
                # Game over.
                showGameOverScreen()
                return

            SNAKES[snakeID].move(SNAKES[snakeID].checkEaten(FOOD, SNAKES))

        DISPLAYSURF.fill(Config.BGCOLOR)
        drawGrid()
        FOOD.draw(DISPLAYSURF)
        for snakeID in SNAKES:
            SNAKES[snakeID].draw(DISPLAYSURF)
            drawScore(len(SNAKES[snakeID].coords) - 3, snakeID)
        pygame.display.update()
        gameFPS = Config.SETTINGS['difficulty'] + 1
        FPSCLOCK.tick(gameFPS)


def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press any key to continue.', True,
                                    Colors.DARKGREY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.center = (Config.SCREENSIZE['width'] / 2,
        Config.SCREENSIZE['height'] - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    pygame.event.get()
    if len(keyUpEvents) == 0:
        return None
    return keyUpEvents[0].key


def showStartScreen():
    currentSelection = Config.MENUSINGLEPLAYER

    pygame.time.wait(100)
    checkForKeyPress()  # Clear out any key presses in the event queue.

    while True:
        titleFont = pygame.font.Font('freesansbold.ttf', 100)
        titleSurf = titleFont.render('Snake!', True, Colors.WHITE,
            Colors.DARKGREEN)
        titleRect = titleSurf.get_rect()
        titleRect.center = (Config.SCREENSIZE['width'] / 2,
            Config.SCREENSIZE['height'] / 3)

        DISPLAYSURF.fill(Config.BGCOLOR)
        DISPLAYSURF.blit(titleSurf, titleRect)

        drawStartMenu(currentSelection)

        keyPress = checkForKeyPress()

        if keyPress == K_RETURN:
            makeStartSelection(currentSelection)
        elif keyPress == K_ESCAPE:
            terminate()
        elif keyPress == K_UP or keyPress == K_DOWN:
            currentSelection = changeStartSelectedItem(
                keyPress, currentSelection)

        pygame.display.update()
        FPSCLOCK.tick(Config.FPS)


def changeStartSelectedItem(key, selected):
    if key == K_UP:
        selected -= 1
    elif key == K_DOWN:
        selected += 1

    return selected % len(Config.MAINMENU)


def drawStartMenu(selection):
    for i, menuItem in enumerate(Config.MAINMENU):
        if selection == i:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.ALMOSTBLACK, Colors.WHITE)
        else:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.WHITE)
        itemRect = itemSurf.get_rect()
        itemRect.center = (Config.SCREENSIZE['width'] / 2,
            Config.SCREENSIZE['height'] / 3 * 2 + itemRect.height * i + 8 * i)
        DISPLAYSURF.blit(itemSurf, itemRect)


def makeStartSelection(selection):
    pygame.event.get()  # Clear event queue.
    if selection == Config.MENUSINGLEPLAYER:
        Config.MULTIPLAYER = False
        showSnakeSelectScreen()
        runGame()
    elif selection == Config.MENUMULTIPLAYER:
        Config.MULTIPLAYER = True
        showSnakeSelectScreen()
        runGame()
    elif selection == Config.MENUOPTIONS:
        showOptionsScreen()
    elif selection == Config.MENUEXIT:
        terminate()


def showOptionsScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf = titleFont.render('OPTIONS', True, Colors.WHITE,
                                  Colors.DARKGREEN)

    currentSelection = Config.OPTIONSSIZE

    pygame.time.wait(100)
    checkForKeyPress()  # Clear out any key presses in the event queue.

    while True:
        titleRect = titleSurf.get_rect()
        titleRect.center = (Config.SCREENSIZE['width'] / 2,
            Config.SCREENSIZE['height'] / 3)

        DISPLAYSURF.fill(Config.BGCOLOR)
        DISPLAYSURF.blit(titleSurf, titleRect)

        drawOptionsMenu(currentSelection)

        keyPress = checkForKeyPress()

        if keyPress == K_RETURN:
            if makeOptionsSelection(currentSelection):
                return
        elif keyPress == K_ESCAPE:
            Config.loadSettings()
            return
        elif (keyPress == K_UP or keyPress == K_DOWN or
                keyPress == K_LEFT or keyPress == K_RIGHT):
            currentSelection = changeOptionsSelectedItem(
                keyPress, currentSelection)

        pygame.display.update()
        FPSCLOCK.tick(Config.FPS)


def changeOptionsSelectedItem(key, selected):
    global DISPLAYSURF
    if key == K_UP:
        selected -= 1
    elif key == K_DOWN:
        selected += 1
    elif key == K_LEFT:
        if selected == Config.OPTIONSDIFFICULTY:
            Config.SETTINGS['difficulty'] = int(
                (Config.SETTINGS['difficulty'] - 2) % Config.MAXDIFFICULTY)
        elif selected == Config.OPTIONSWRAP:
            Config.SETTINGS['screenWrap'] = not Config.SETTINGS['screenWrap']
        elif selected == Config.OPTIONSSIZE:
            Config.SETTINGS['screenSize'] = (
                (Config.SETTINGS['screenSize'] - 1) %
                len(Config.SCREENSIZEOPTIONS))
            Config.SCREENSIZE = (
                Config.SCREENSIZEOPTIONS[Config.SETTINGS['screenSize']])
            Config.CELLWIDTH = int(
                Config.SCREENSIZE['width'] / Config.CELLSIZE)
            Config.CELLHEIGHT = int(
                Config.SCREENSIZE['height'] / Config.CELLSIZE)
            DISPLAYSURF = pygame.display.set_mode(
                (Config.SCREENSIZE['width'], Config.SCREENSIZE['height']))
    elif key == K_RIGHT:
        if selected == Config.OPTIONSDIFFICULTY:
            Config.SETTINGS['difficulty'] = int(
                (Config.SETTINGS['difficulty'] + 2) % Config.MAXDIFFICULTY)
        elif selected == Config.OPTIONSWRAP:
            Config.SETTINGS['screenWrap'] = not Config.SETTINGS['screenWrap']
        elif selected == Config.OPTIONSSIZE:
            Config.SETTINGS['screenSize'] = (
                (Config.SETTINGS['screenSize'] + 1) %
                len(Config.SCREENSIZEOPTIONS))
            Config.SCREENSIZE = (
                Config.SCREENSIZEOPTIONS[Config.SETTINGS['screenSize']])
            Config.CELLWIDTH = int(
                Config.SCREENSIZE['width'] / Config.CELLSIZE)
            Config.CELLHEIGHT = int(
                Config.SCREENSIZE['height'] / Config.CELLSIZE)
            DISPLAYSURF = pygame.display.set_mode(
                (Config.SCREENSIZE['width'], Config.SCREENSIZE['height']))
    return selected % len(Config.OPTIONSMENU)


def drawOptionsMenu(selection):
    for i, menuItem in enumerate(Config.OPTIONSMENU):
        if selection == i:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.ALMOSTBLACK, Colors.WHITE)
        else:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.WHITE)

        itemRect = itemSurf.get_rect()

        if i != Config.OPTIONSDEFAULTS and i != Config.OPTIONSOK:
            itemRect.bottomright = (
                Config.SCREENSIZE['width'] / 2 - 8,
                Config.SCREENSIZE['height'] / 3 * 2 +
                itemRect.height * i + 8 * i)

            if i == Config.OPTIONSSIZE:
                sizeIndex = Config.SETTINGS['screenSize']
                optionSurf = BASICFONT.render(
                    str(Config.SCREENSIZEOPTIONS[sizeIndex]['width']) + ' x ' +
                    str(Config.SCREENSIZEOPTIONS[sizeIndex]['height']),
                    True, Colors.WHITE)
                optionRect = optionSurf.get_rect()
            elif i == Config.OPTIONSDIFFICULTY:
                optionSurf = BASICFONT.render(
                    str(int(Config.SETTINGS['difficulty'] / 2) + 1),
                    True, Colors.WHITE)
                optionRect = optionSurf.get_rect()
            elif i == Config.OPTIONSWRAP:
                optionSurf = BASICFONT.render(
                    str(Config.SETTINGS['screenWrap']), True, Colors.WHITE)
                optionRect = optionSurf.get_rect()

            optionRect.bottomleft = (
                    Config.SCREENSIZE['width'] / 2 + 8,
                    Config.SCREENSIZE['height'] / 3 * 2 +
                    optionRect.height * i + 8 * i)
            DISPLAYSURF.blit(optionSurf, optionRect)
        else:
            itemRect.center = (
                Config.SCREENSIZE['width'] / 2,
                Config.SCREENSIZE['height'] / 3 * 2 +
                itemRect.height * i + 8 * i)
        DISPLAYSURF.blit(itemSurf, itemRect)


def makeOptionsSelection(selection):
    pygame.event.get()  # Clear event queue.
    if selection == Config.OPTIONSOK:
        Config.saveSettings()
        return True
    elif selection == Config.OPTIONSDEFAULTS:
        Config.resetSettings()
        return False
    else:
        changeOptionsSelectedItem(K_LEFT, selection)
        return False


def showSnakeSelectScreen():
    '''
    '''


def showPauseScreen(FOOD, SNAKES):
    fadeOutSurf = pygame.Surface((Config.SCREENSIZE['width'],
        Config.SCREENSIZE['height']))
    fadeOutSurf.set_alpha(128)
    fadeOutSurf.fill(Colors.ALMOSTBLACK)

    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf = titleFont.render('PAUSED', True, Colors.WHITE,
                                  Colors.DARKGREEN)
    titleRect = titleSurf.get_rect()
    titleRect.center = (Config.SCREENSIZE['width'] / 2,
        Config.SCREENSIZE['height'] / 3)

    currentSelection = Config.PAUSECONTINUE

    pygame.time.wait(100)
    checkForKeyPress()  # Clear out any key presses in the event queue.

    while True:
        DISPLAYSURF.fill(Config.BGCOLOR)
        drawGrid()
        FOOD.draw(DISPLAYSURF)
        for snakeID in SNAKES:
            SNAKES[snakeID].draw(DISPLAYSURF)
            drawScore(len(SNAKES[snakeID].coords) - 3, snakeID)

        DISPLAYSURF.blit(fadeOutSurf, (0, 0))
        DISPLAYSURF.blit(titleSurf, titleRect)

        drawPauseMenu(currentSelection)

        keyPress = checkForKeyPress()

        if keyPress == K_RETURN:
            resumeGame = makePauseSelection(currentSelection)
            return resumeGame
        elif keyPress == K_ESCAPE:
            return True
        elif keyPress == K_UP or keyPress == K_DOWN:
            currentSelection = changePauseSelectedItem(
                keyPress, currentSelection)

        pygame.display.update()
        FPSCLOCK.tick(Config.FPS)


def drawPauseMenu(selection):
    for i, menuItem in enumerate(Config.PAUSEMENU):
        if selection == i:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.ALMOSTBLACK, Colors.WHITE)
        else:
            itemSurf = BASICFONT.render(menuItem, True,
                Colors.WHITE)
        itemRect = itemSurf.get_rect()
        itemRect.center = (Config.SCREENSIZE['width'] / 2,
            Config.SCREENSIZE['height'] / 3 * 2 + itemRect.height * i + 8 * i)
        DISPLAYSURF.blit(itemSurf, itemRect)


def changePauseSelectedItem(key, selected):
    if key == K_UP:
        selected -= 1
    elif key == K_DOWN:
        selected += 1

    return selected % len(Config.PAUSEMENU)


def makePauseSelection(selection):
    pygame.event.get()  # Clear event queue.
    if selection == Config.PAUSECONTINUE:
        # Return to game.
        return True
    elif selection == Config.PAUSEMAINMENU:
        # Quit to main menu.
        return False
    elif selection == Config.PAUSEEXIT:
        terminate()


def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, Colors.WHITE)
    overSurf = gameOverFont.render('Over', True, Colors.WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (Config.SCREENSIZE['width'] / 2, 10)
    overRect.midtop = (Config.SCREENSIZE['width'] / 2,
        gameRect.height + 10 + 25)

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


def drawScore(score, snakeID):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, Colors.WHITE)
    scoreRect = scoreSurf.get_rect()
    if snakeID == 'P1':
        scoreRect.topleft = (Config.SCREENSIZE['width'] - 120, 10)
    elif snakeID == 'P2':
        scoreRect.topleft = (120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawGrid():
    # Draw vertical lines.
    for x in range(0, Config.SCREENSIZE['width'], Config.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, Colors.ALMOSTBLACK, (x, 0),
                         (x, Config.SCREENSIZE['height']))
    # Draw horizontal lines.
    for y in range(0, Config.SCREENSIZE['height'], Config.CELLSIZE):
        pygame.draw.line(DISPLAYSURF, Colors.ALMOSTBLACK, (0, y),
                         (Config.SCREENSIZE['width'], y))


if __name__ == '__main__':
    main()
