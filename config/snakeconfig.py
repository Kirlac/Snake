import os
import pickle

from colors.colorlist import Colors


class Config:

    SETTINGSFILE = 'snake.settings'

    SCREENSIZEOPTIONS = [{'width': 640, 'height': 360},
                         {'width': 960, 'height': 540},
                         {'width': 1024, 'height': 576},
                         {'width': 1280, 'height': 720}]

    SETTINGS = {'screenSize': 2,
                'difficulty': 0,
                'screenWrap': False}

    FPS = 30
    GAMEFPS = 15
    CELLSIZE = 20
    SCREENSIZE = SCREENSIZEOPTIONS[SETTINGS['screenSize']]
    CELLWIDTH = int(SCREENSIZE['width'] / CELLSIZE)
    CELLHEIGHT = int(SCREENSIZE['height'] / CELLSIZE)
    MAXDIFFICULTY = 30

    BGCOLOR = Colors.BLACK

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    MULTIPLAYER = False

    MAINMENU = ['START SINGLE PLAYER GAME',
                'START TWO PLAYER GAME',
                'OPTIONS',
                'EXIT']

    MENUSINGLEPLAYER = 0
    MENUMULTIPLAYER = 1
    MENUOPTIONS = 2
    MENUEXIT = 3

    PAUSEMENU = ['CONTINUE',
                 'BACK TO MAIN MENU',
                 'EXIT']

    PAUSECONTINUE = 0
    PAUSEMAINMENU = 1
    PAUSEEXIT = 2

    OPTIONSMENU = ['SCREEN SIZE',
                   'DIFFICULTY',
                   'SCREEN WRAP',
                   'RESET DEFAULTS',
                   'OK']

    OPTIONSSIZE = 0
    OPTIONSDIFFICULTY = 1
    OPTIONSWRAP = 2
    OPTIONSDEFAULTS = 3
    OPTIONSOK = 4

    @staticmethod
    def loadSettings():
        if os.path.isfile(Config.SETTINGSFILE):
            with open(Config.SETTINGSFILE, 'rb') as settings:
                Config.SETTINGS = pickle.load(settings)

                Config.SCREENSIZE = (
                    Config.SCREENSIZEOPTIONS[Config.SETTINGS['screenSize']])
                Config.CELLWIDTH = int(
                    Config.SCREENSIZE['width'] / Config.CELLSIZE)
                Config.CELLHEIGHT = int(
                    Config.SCREENSIZE['height'] / Config.CELLSIZE)
        else:
            Config.resetSettings()
            Config.saveSettings()

    def saveSettings():
        with open(Config.SETTINGSFILE, 'wb') as settings:
            Config.SETTINGS = pickle.dump(Config.SETTINGS, settings)

    def resetSettings():
        Config.SETTINGS = {'screenSize': 2,
                           'difficulty': 0,
                           'screenWrap': False}
        Config.SCREENSIZE = (
            Config.SCREENSIZEOPTIONS[Config.SETTINGS['screenSize']])
        Config.CELLWIDTH = int(Config.SCREENSIZE['width'] / Config.CELLSIZE)
        Config.CELLHEIGHT = int(Config.SCREENSIZE['height'] / Config.CELLSIZE)