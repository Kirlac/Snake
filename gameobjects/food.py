import random

import pygame

from config.vars import Vars
from colors.colorlist import Colors


class Food:

    def __init__(self, snakeCoords):
        # Spawn food in a random place.
        self.respawn(snakeCoords)

    @staticmethod
    def getRandomLocation():
        return {'x': random.randint(0, Vars.CELLWIDTH - 1),
                'y': random.randint(0, Vars.CELLHEIGHT - 1)}

    def draw(self, surf):
        x = self.coords['x'] * Vars.CELLSIZE
        y = self.coords['y'] * Vars.CELLSIZE
        foodRect = pygame.Rect(x, y, Vars.CELLSIZE, Vars.CELLSIZE)
        pygame.draw.rect(surf, Colors.DARKBROWN, foodRect)

    def respawn(self, snakeCoords):
        self.coords = Food.getRandomLocation()
        if self.coords in snakeCoords:
            self.respawn(snakeCoords)