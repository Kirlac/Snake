import random

import pygame

from config.snakeconfig import Config
from colors.colorlist import Colors


class Snake:

    HEAD = 0  # Syntactic sugar: index of the snake's head.

    def __init__(self):
        # Set a random start point.
        self.startx = random.randint(5, Config.CELLWIDTH - 6)
        self.starty = random.randint(5, Config.CELLHEIGHT - 6)
        self.coords = [{'x': self.startx, 'y': self.starty},
            {'x': self.startx - 1, 'y': self.starty},
            {'x': self.startx - 2, 'y': self.starty}]
        self.direction = Config.RIGHT
        self.newDirection = self.direction
        self.alive = True

    def changeDirection(self, direction):
        if direction == Config.LEFT and self.direction != Config.RIGHT:
            self.newDirection = Config.LEFT
        elif direction == Config.RIGHT and self.direction != Config.LEFT:
            self.newDirection = Config.RIGHT
        elif direction == Config.UP and self.direction != Config.DOWN:
            self.newDirection = Config.UP
        elif direction == Config.DOWN and self.direction != Config.UP:
            self.newDirection = Config.DOWN

    def checkHit(self):
        # Check if the snake has hit itself or the edge.
        if (self.coords[Snake.HEAD]['x'] == -1 or
                self.coords[Snake.HEAD]['x'] == Config.CELLWIDTH or
                self.coords[Snake.HEAD]['y'] == -1 or
                self.coords[Snake.HEAD]['y'] == Config.CELLHEIGHT or
                self.coords[Snake.HEAD] in self.coords[1:]):
            # Game over.
            self.alive = False
            return True
        else:
            return False

    def checkEaten(self, food, snakes):
        # Check if snake has eaten food.
        if self.coords[Snake.HEAD] == food.coords:
            food.respawn(snakes)
            return True
        else:
            return False

    def move(self, growing):
        self.direction = self.newDirection
        if self.direction == Config.UP:
            newHead = {'x': self.coords[Snake.HEAD]['x'],
                       'y': self.coords[Snake.HEAD]['y'] - 1}
        elif self.direction == Config.DOWN:
            newHead = {'x': self.coords[Snake.HEAD]['x'],
                       'y': self.coords[Snake.HEAD]['y'] + 1}
        elif self.direction == Config.LEFT:
            newHead = {'x': self.coords[Snake.HEAD]['x'] - 1,
                       'y': self.coords[Snake.HEAD]['y']}
        elif self.direction == Config.RIGHT:
            newHead = {'x': self.coords[Snake.HEAD]['x'] + 1,
                       'y': self.coords[Snake.HEAD]['y']}

        if not growing:
            # remove the last tail segment.
            del self.coords[-1]

        # Move the snake by adding a segment in the direction it is moving
        self.coords.insert(0, newHead)

    def draw(self, surf):
        for coord in self.coords:
            x = coord['x'] * Config.CELLSIZE
            y = coord['y'] * Config.CELLSIZE
            segmentRect = pygame.Rect(x, y, Config.CELLSIZE, Config.CELLSIZE)
            pygame.draw.rect(surf, Colors.DARKGREEN, segmentRect)
            wormInnerSegmentRect = pygame.Rect(
                x + 4, y + 4, Config.CELLSIZE - 8, Config.CELLSIZE - 8)
            pygame.draw.rect(surf, Colors.GREEN, wormInnerSegmentRect)