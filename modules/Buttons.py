import pygame
from pygame.math import Vector2

class Button:
    ''' Button Class '''

    def __init__(self, surface, pos, text="", w=100, h=50, color = (200,200,200), hover_color = (180,180,180)):
        self._display_surface = surface
        self.pos = Vector2(pos[0], pos[1])
        self.width, self.height = w, h
        self.color = color
        self.hover_color = hover_color
        self.img = pygame.Surface((self.width, self.height))
        self.surf_rect = self.img.get_rect(topleft=(self.pos.x, self.pos.y))
        
        #Rendering font
        self.font = pygame.font.SysFont("Arial", 18, True)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect(center=(w/2, h/2))

    def draw(self):
        self.img.fill((255,255,255))
        pygame.draw.rect(self.img, self.color, (0, 0, self.width, self.height))
        #check if mouse is hovering over the button
        self.onhover()
        self.img.blit(self.text, self.text_rect)
        #draw the button on the display surface
        self._display_surface.blit(self.img, (self.pos.x, self.pos.y))
    
    def onhover(self):
        if self.surf_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.img, self.hover_color, (0, 0, self.width, self.height))

    def onclick(self, cursor_pos):
        if self.checkbounds(cursor_pos):
            return True
        return False

    def checkbounds(self, cursor_pos):
        ''' Checks if the cursor is within the button bounds '''

        if cursor_pos[0] > self.pos.x and \
            cursor_pos[0] < self.pos.x + self.width and \
                cursor_pos[1] > self.pos.y and \
                    cursor_pos[1] < self.pos.y + self.height:
                return True
        return False


