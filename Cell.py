import pygame
from pygame.math import Vector2
import random


class Cell:
    ''' Just what it sounds:: a cell with a status of dead or alive '''

    SIZE = 10

    def __init__(self, surface, x, y):
        self._scene_surface = surface
        self.pos = Vector2(x, y)

        # self.alive = random.randint(0,1)
        self.alive = False
        self.neighbours = 0
        self.img = pygame.Surface((Cell.SIZE, Cell.SIZE))

    def update(self):
        #TODO::
        pass

    def draw(self):
        self.img.fill((0,0,0))

        if self.alive:
            pygame.draw.rect(self.img, (0, 0, 0), (1, 1, Cell.SIZE - 2, Cell.SIZE - 2))
        else:
            pygame.draw.rect(self.img, (255, 255, 255), (1, 1, Cell.SIZE - 2, Cell.SIZE - 2))
        
        self._scene_surface.blit(self.img, (self.pos.x*Cell.SIZE, self.pos.y*Cell.SIZE))

    def get_neighbours():
        #TODO:: Find the neighbours..there must be 8 neighbours adjacent to the cell
        pass