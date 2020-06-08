import pygame
from pygame.math import Vector2
from Cell import Cell
import numpy as np


class Scene:
    ''' Game Scene :: Main Canvas '''

    def __init__(self, surface, x, y):
        self._display_surface = surface
        self.pos = Vector2(x, y)

        self.width, self.height = 500, 500
        self.img = pygame.Surface((self.width, self.height))

        self.board = np.array([[Cell(self.img, x, y) 
                                for x in range((int)(self.width / Cell.SIZE))] 
                                for y in range((int)(self.height / Cell.SIZE))])
              
    def update(self):
        for row in self.board:
            for cell in row:
                cell.update()

    def draw(self):
        ''' Draw the Game Scene on the main surface '''

        self.img.fill((122, 122, 122))
        for row in self.board:
            for cell in row:
                cell.draw()
        self._display_surface.blit(self.img, (self.pos.x, self.pos.y))
