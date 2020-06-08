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
        self.previous = False   #state of previous generation of the cell
        self.neighbours = 0
        self.img = pygame.Surface((Cell.SIZE, Cell.SIZE))

    def update(self, board):
        ''' Updates the cell's state by analyzing the neighbourhood '''

        self.get_neighbours(board)
        #TODO:: check for the rules
        self.previous = self.alive

    def draw(self):
        ''' Draws the cell on the provided scene '''

        self.img.fill((0,0,0))

        if self.alive:
            pygame.draw.rect(self.img, (0, 0, 0), (1, 1, Cell.SIZE - 2, Cell.SIZE - 2))
        else:
            pygame.draw.rect(self.img, (255, 255, 255), (1, 1, Cell.SIZE - 2, Cell.SIZE - 2))
        
        self._scene_surface.blit(self.img, (self.pos.x*Cell.SIZE, self.pos.y*Cell.SIZE))

    def get_neighbours(self, board):
        ''' Gets the number of live neighbours '''

        for i in range(-1, 2):
            for j in range(-1, 2):
                temp = Vector2((self.pos.x + j), (self.pos.y + i))
                
                if temp.y > len(board) - 1: temp.y = 0
                if temp.y < 0: temp.y = -1
                if temp.x > len(board[0]) - 1: temp.x = 0
                if temp.x < 0: temp.x = -1

                self.neighbours += board[(int)(temp.y)][(int)(temp.x)].previous

        self.neighbours -= self.alive #removing itself