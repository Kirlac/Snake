import random

import pygame

from config.snakeconfig import Config
from colors.colorlist import Colors


class Food:

    def __init__(self, snakes):
        # Spawn food in a random place.
        self.respawn(snakes)
        self.color = Colors.WHITE

    @staticmethod
    def getRandomLocation():
        return {'x': random.randint(0, Config.CELLWIDTH - 1),
                'y': random.randint(0, Config.CELLHEIGHT - 1)}

    def draw(self, surf):
        x = self.coords['x'] * Config.CELLSIZE
        y = self.coords['y'] * Config.CELLSIZE
        foodRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
        pygame.draw.rect(surf, self.color, foodRect)

    def respawn(self, snakes):
        self.coords = Food.getRandomLocation()
        for snakeID in snakes:
            if self.coords in snakes[snakeID].coords:
                self.respawn(snakes)