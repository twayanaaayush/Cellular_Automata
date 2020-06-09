import pygame
from pygame.math import Vector2

class Button:
    ''' Button Class '''

    def __init__(self, surface, x, y, w=100, h=50, color = (200, 200, 200)):
        self._display_surface = surface
        self.pos = Vector2(x, y)
        self.width, self.height = w, h
        self.color = color
        self.img = pygame.Surface((self.width, self.height))

    def draw(self):
        self.img.fill((255,255,255))
        pygame.draw.rect(self.img, self.color, (0, 0, self.width, self.height))
        self._display_surface.blit(self.img, (self.pos.x, self.pos.y))
