import pygame
from pygame.math import Vector2
import random


class Cell:
    ''' Just what it sounds:: a cell with a status of dead or alive '''

    SIZE = 10

    def __init__(self, surface, x, y):
        self._scene_surface = surface
        self.pos = Vector2(x, y)

        self.alive = random.choice((1,0,0,0,0,0,0,0,0,0,0,0,0))
        self.previous = self.alive   #state of previous generation of the cell
        self.neighbours = 0
        self.img = pygame.Surface((Cell.SIZE, Cell.SIZE))

    def get_neighbours(self, board):
        ''' Gets the number of live neighbours '''

        self.neighbours = 0

        for i in range(-1, 2):
            for j in range(-1, 2):
                temp = Vector2((self.pos.x + j), (self.pos.y + i))
                
                if temp.y > len(board) - 1: temp.y = 0
                if temp.y < 0: temp.y = -1
                if temp.x > len(board[0]) - 1: temp.x = 0
                if temp.x < 0: temp.x = -1

                self.neighbours += board[(int)(temp.y)][(int)(temp.x)].previous

        self.neighbours -= self.previous #removing itself

    def rulesoflife(self):
        '''
            "Rules of Life and Death"
            
            1. If the cell is alive and has 1 or less neighbour or if the cell has 4 or more neighbours, it dies.
            2. If the cell is dead and has exactly 3 neighbours, it becomes alive.
            3. In any other cases, the cell retains it's state.
        '''

        if self.previous == True and self.neighbours < 2: self.alive = False
        elif self.previous == True and self.neighbours > 3: self.alive = False
        elif self.previous == 0 and self.neighbours == 3: self.alive = True
        
    def saveprevious(self):
        self.previous = self.alive

    def update(self, board):
        ''' Updates the cell's state by analyzing the neighbourhood '''

        self.get_neighbours(board)
        self.rulesoflife()

    def draw(self):
        ''' Draws the cell on the provided scene '''

        self.img.fill((0,0,0))

        if not self.previous and self.alive: color = (0, 0, 255) #cell is born
        elif self.alive: color = (0, 0, 0)
        elif self.previous and not self.alive: color = (255, 0, 0) #cell dies
        else: color = (255, 255, 255)
        
        pygame.draw.rect(self.img, color, (1, 1, Cell.SIZE - 2, Cell.SIZE - 2))
        self._scene_surface.blit(self.img, (self.pos.x*Cell.SIZE, self.pos.y*Cell.SIZE))