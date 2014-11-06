import random

import pygame

from config.vars import Vars
from colors.colorlist import Colors


class Snake:

    HEAD = 0  # Syntactic sugar: index of the snake's head.

    def __init__(self):
        # Set a random start point.
        self.startx = random.randint(5, Vars.CELLWIDTH - 6)
        self.starty = random.randint(5, Vars.CELLHEIGHT - 6)
        self.coords = [{'x': self.startx, 'y': self.starty},
            {'x': self.startx - 1, 'y': self.starty},
            {'x': self.startx - 2, 'y': self.starty}]
        self.direction = Vars.RIGHT

    def changeDirection(self, direction):
        if direction == Vars.LEFT and self.direction != Vars.RIGHT:
            self.direction = Vars.LEFT
        elif direction == Vars.RIGHT and self.direction != Vars.LEFT:
            self.direction = Vars.RIGHT
        elif direction == Vars.UP and self.direction != Vars.DOWN:
            self.direction = Vars.UP
        elif direction == Vars.DOWN and self.direction != Vars.UP:
            self.direction = Vars.DOWN

    def checkHit(self):
        # Check if the snake has hit itself or the edge.
        if (self.coords[Snake.HEAD]['x'] == -1 or
            self.coords[Snake.HEAD]['x'] == Vars.CELLWIDTH or
            self.coords[Snake.HEAD]['y'] == -1 or
            self.coords[Snake.HEAD]['y'] == Vars.CELLHEIGHT or
            self.coords[Snake.HEAD] in self.coords[1:]):
            # Game over.
            return True
        else:
            return False

    def checkEaten(self, foodCoords):
        # Check if snake has eaten food.
        if self.coords[Snake.HEAD] == foodCoords:
            return True
        else:
            return False

    def move(self, growing):
        if self.direction == Vars.UP:
            newHead = {'x': self.coords[Snake.HEAD]['x'],
                       'y': self.coords[Snake.HEAD]['y'] - 1}
        elif self.direction == Vars.DOWN:
            newHead = {'x': self.coords[Snake.HEAD]['x'],
                       'y': self.coords[Snake.HEAD]['y'] + 1}
        elif self.direction == Vars.LEFT:
            newHead = {'x': self.coords[Snake.HEAD]['x'] - 1,
                       'y': self.coords[Snake.HEAD]['y']}
        elif self.direction == Vars.RIGHT:
            newHead = {'x': self.coords[Snake.HEAD]['x'] + 1,
                       'y': self.coords[Snake.HEAD]['y']}

        if not growing:
            # remove the last tail segment.
            del self.coords[-1]

        # Move the snake by adding a segment in the direction it is moving
        self.coords.insert(0, newHead)

    def draw(self, surf):
        for coord in self.coords:
            x = coord['x'] * Vars.CELLSIZE
            y = coord['y'] * Vars.CELLSIZE
            segmentRect = pygame.Rect(x, y, Vars.CELLSIZE, Vars.CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, Colors.DARKGREEN, segmentRect)
            wormInnerSegmentRect = pygame.Rect(
                x + 4, y + 4, Vars.CELLSIZE - 8, Vars.CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, Colors.GREEN, wormInnerSegmentRect)