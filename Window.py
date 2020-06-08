from pygame.locals import *
import pygame
import sys
import Scene
from Cell import Cell


class App:
    ''' Creates a single non-resizable window App. '''

    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    FPS = 60

    def __init__(self):
        ''' Initializing pygame components '''

        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self._display_surf = pygame.display.set_mode(App.SIZE)
        self.clock = pygame.time.Clock()

        self.scene_x_off, self.scene_y_off = 150, 50
        self.game_scene = Scene.Scene(self._display_surf, self.scene_x_off, self.scene_y_off)

        self.running = True

    def input_handler(self):
        ''' Handling the user inputs '''

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                cursor_pos = pygame.mouse.get_pos()
                if self.checkbounds(cursor_pos):
                    index = self.get_board_index(cursor_pos)
                    cell = self.game_scene.board

                    # print (index.x, index.y)
                    if cell[(int)(index.y)][(int)(index.x)].alive:
                        cell[(int)(index.y)][(int)(index.x)].alive = False
                    else:
                        cell[(int)(index.y)][(int)(index.x)].alive = True

    def checkbounds(self, cursor_pos):
        if cursor_pos[0] > self.scene_x_off and \
            cursor_pos[0] < self.scene_x_off + self.game_scene.width and \
                cursor_pos[1] > self.scene_y_off and \
                    cursor_pos[1] < self.scene_y_off + self.game_scene.height:
                return True
        return False

    def get_board_index(self, cursor_pos):
        vec2d = pygame.math.Vector2

        cursor_pos = vec2d(cursor_pos[0], cursor_pos[1])
        rel_cursor_pos = vec2d(cursor_pos.x-self.scene_x_off, 
                                cursor_pos.y-self.scene_y_off)

        return vec2d((rel_cursor_pos.x // Cell.SIZE),
                    (rel_cursor_pos.y // Cell.SIZE))

    def update(self):
        ''' Updating the game window '''
        
        self.game_scene.update()

    def draw(self):
        ''' Rendering the graphics on the display surface '''

        self._display_surf.fill((255, 255, 255))
        self.game_scene.draw()
        pygame.display.update()

    def run(self):
        ''' Main Event Loop '''

        while self.running:
            self.input_handler()
            self.update()
            self.draw()
            self.clock.tick(App.FPS)

        pygame.quit() and sys.exit()


if __name__ == '__main__':
    App().run()