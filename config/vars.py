from colors.colorlist import Colors


class Vars:

    COREFPS = 30
    GAMEFPS = 15
    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    CELLSIZE = 20
    CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
    CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

    BGCOLOR = Colors.BLACK

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    MULTIPLAYERGAME = False

    MAINMENU = ['START SINGLE PLAYER GAME',
                'START TWO PLAYER GAME',
                'OPTIONS',
                'EXIT']

    MENUSINGLEPLAYER = 0
    MENUMULTIPLAYER = 1
    MENUOPTIONS = 2
    MENUEXIT = 3