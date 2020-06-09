import pygame
from pygame.math import Vector2
import numpy as np
import random
from .Cell import Cell


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

    def reset(self):
        for row in self.board:
            for cell in row:
                cell.alive = False
    
    def generate(self):
        for row in self.board:
            for cell in row:
                cell.alive = random.choice((1,0,0,0,0,0,0,0,0,0,0,0))
                # cell.alive = random.randint(0,2)

    def change_cell_state(self, cursor_pos):
        ''' Changes the current state (dead or alive) of the selected cell '''

        index = self.get_board_index(cursor_pos)
        cell = self.board
        
        # print (index.x, index.y)
        if cell[(int)(index.y)][(int)(index.x)].alive:
            cell[(int)(index.y)][(int)(index.x)].alive = False
        else:
            cell[(int)(index.y)][(int)(index.x)].alive = True

    def get_board_index(self, cursor_pos):
        ''' Returns the index of the selected cell '''

        cursor_pos = Vector2(cursor_pos[0], cursor_pos[1])
        rel_cursor_pos = Vector2(cursor_pos.x-self.pos.x, 
                                cursor_pos.y-self.pos.y)

        return Vector2((rel_cursor_pos.x // Cell.SIZE),
                    (rel_cursor_pos.y // Cell.SIZE))

    def update(self):
        ''' Updates each cell on the board '''

        self.checkprevious()
        for row in self.board:
            for cell in row:
                cell.update(self.board)

    def checkprevious(self):
        for row in self.board:
            for cell in row:
                 cell.previous = cell.alive

    def draw(self):
        ''' Draw the Game Scene on the main surface '''

        # self.img.fill((122, 122, 122))
        for row in self.board:
            for cell in row:
                cell.draw()
        self._display_surface.blit(self.img, (self.pos.x, self.pos.y))
