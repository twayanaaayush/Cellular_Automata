from pygame.locals import *
import pygame
import sys
from .Scene import Scene
from .Buttons import Button


class App:
    ''' Creates a single non-resizable window App. '''

    WINDOW_WIDTH, WINDOW_HEIGHT = 850, 600
    SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    FPS = 60

    def __init__(self):
        ''' Initializing pygame components '''

        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self._display_surf = pygame.display.set_mode(App.SIZE)
        self.clock = pygame.time.Clock()

        self.scene_x_off, self.scene_y_off = 50, 50
        self.game_scene = Scene(self._display_surf, self.scene_x_off, self.scene_y_off)
        self.scene_state = "pause"

        self.run_button = Button(self._display_surf, (600, 50), "Run", 95)
        self.pause_button = Button(self._display_surf, (705, 50), "Pause", 95)
        self.generate_button = Button(self._display_surf, (600, 110),"Generate Random", 200)
        self.reset_button = Button(self._display_surf, (600, 170),"Reset", 200)

        self.button_grp = [self.run_button, self.pause_button, self.generate_button, self.reset_button]

        self.running = True

    def input_handler(self):
        ''' Handling the user inputs '''

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                cursor_pos = pygame.mouse.get_pos()
                if self.checkbounds(cursor_pos):
                    self.game_scene.change_cell_state(cursor_pos)
                else:
                    #Not the best way....try to optimize this
                    if (self.run_button.onclick(cursor_pos)): self.scene_state = "run"
                    elif (self.pause_button.onclick(cursor_pos)): self.scene_state = "pause"
                    elif (self.generate_button.onclick(cursor_pos)): self.scene_state = "generate"
                    elif (self.reset_button.onclick(cursor_pos)): self.scene_state = "reset"

    def checkbounds(self, cursor_pos):
        ''' Checks if the cursor is within the game scene bounds '''

        if cursor_pos[0] > self.scene_x_off and \
            cursor_pos[0] < self.scene_x_off + self.game_scene.width and \
                cursor_pos[1] > self.scene_y_off and \
                    cursor_pos[1] < self.scene_y_off + self.game_scene.height:
                return True
        return False

    def update(self):
        ''' Updating the display window '''
        
        if self.scene_state == "run":
            self.game_scene.update()
        elif self.scene_state == "reset":
            self.game_scene.reset()
            self.scene_state = "pause"
        elif self.scene_state == "generate":
            self.game_scene.generate()
            self.scene_state = "run"


    def draw(self):
        ''' Rendering the graphics on the display surface '''

        self._display_surf.fill((255, 255, 255))
        self.game_scene.draw()
        for button in self.button_grp:
            button.draw()
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