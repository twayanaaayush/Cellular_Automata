from pygame.locals import *
import pygame
import sys
from .Scene import Scene
from .Buttons import Button


class App:
    ''' Creates a single non-resizable window App. '''

    #some CONSTANTS.
    WINDOW_WIDTH, WINDOW_HEIGHT = 850, 600
    SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
    FPS = 60

    def __init__(self):
        ''' Initializing pygame components '''

        pygame.init()
        pygame.display.set_caption("Conway's Game of Life")
        self._display_surf = pygame.display.set_mode(App.SIZE)
        self.clock = pygame.time.Clock()

        #offsets for the game scene, to position them relative to the main display surafce.
        self.scene_x_off, self.scene_y_off = 50, 50
        #creting a Scene instance.
        self.game_scene = Scene(self._display_surf, self.scene_x_off, self.scene_y_off)

        #Buttons for interaction.
        self.run_button = Button(self._display_surf, (600, 50), "Run", 95)
        self.pause_button = Button(self._display_surf, (705, 50), "Pause", 95)
        self.generate_button = Button(self._display_surf, (600, 110),"Generate Random", 200)
        self.reset_button = Button(self._display_surf, (600, 170),"Reset", 200)

        #Grouping the buttons, i.e.adding them to a list.
        self.button_grp = [self.run_button, self.pause_button, self.generate_button, self.reset_button]

        #creating a pygame Surface called Legend to display various info.
        self.legend = pygame.Surface((200,300))

        #setting the running variable to control the game loop.
        self.running = True

    def input_handler(self):
        ''' Handling the user inputs '''

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False    #setting the running to false to exit the loop.
            elif event.type == MOUSEBUTTONDOWN:
            #checking for the mouse button down event to track if the user clicked the
            #cell on the board(game_scene).
                cursor_pos = pygame.mouse.get_pos() #gets the current cursor position.
                if self.checkbounds(cursor_pos):
                    #checking if the cursor position is within the game_scene bounds, if yes, calling a
                    #function to change the clicked cell's state.
                    self.game_scene.change_cell_state(cursor_pos)
                else:
                    #Not the best way....try to optimize this
                    #implementing onClick events for buttons.
                    if (self.run_button.onclick(cursor_pos)): self.game_scene.state = "run"
                    elif (self.pause_button.onclick(cursor_pos)): self.game_scene.state = "pause"
                    elif (self.generate_button.onclick(cursor_pos)): self.game_scene.state = "generate"
                    elif (self.reset_button.onclick(cursor_pos)): self.game_scene.state = "reset"

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
        
        #calling the update function for game_scene if the status is run, because
        #we wouldn't want to change anything in the screen...everything remains same in other states.
        if self.game_scene.state == "run":
            self.game_scene.update()    
        elif self.game_scene.state == "reset":
            self.game_scene.reset()
            self.game_scene.state = "pause"
        elif self.game_scene.state == "generate":
            self.game_scene.generate()
            self.game_scene.state = "run"

    def draw(self):
        ''' Rendering the graphics on the display surface '''

        #fills the display surface to a color...alternative to clearing the screen to perform new drawing action.
        self._display_surf.fill((255, 255, 255))
        #calling the draw function for game_scene object.
        self.game_scene.draw()
        #draws all the buttons in the button group.
        for button in self.button_grp:
            button.draw()
        #updating the display window..similar to display.flip()
        pygame.display.update()

    def run(self):
        ''' Main Event Loop '''

        while self.running:    #running the loop till user exits the application.
            self.input_handler()
            self.update()
            self.draw()
            self.clock.tick(App.FPS)    #this apparantly maintains the Frame count..idk

        pygame.quit() and sys.exit()


if __name__ == '__main__':
    App().run()