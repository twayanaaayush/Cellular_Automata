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
        #offset for the legend display
        self.legend_x_offset, self.legend_y_offset = 600, 250 
        #fonts to display in the legend
        self.factive_cell = None
        self.fcolorcode = self.create_font("-"*8+" Color Code "+"-"*8, 18)
        self.fdeath = self.create_font("Red:  Death", 15, (200,0,0))
        self.fbirth = self.create_font("Blue:  Birth", 15, (0,0,200))
        self.fstatic = self.create_font("Black:  Static", 15)
        self.fcell_count =  self.create_font("Total Cells:  " + str(self.game_scene.cell_count), 15)
        self.fstatus = self.create_font("Status:  " + str(self.game_scene.state).upper(), 15, (200,0,0))

        #setting the running variable to control the game loop.
        self.running = True

        #tracks when the state changed (used to update the fstatus only when there is change in game state)
        self.status = self.game_scene.state

    def create_font(self, text, size, color=(50,50,50)):
        ''' Returns a new font object '''

        font = pygame.font.SysFont("Calibri", size, True)
        text = font.render(text, True, color)
        return text

    def update_font(self):
        ''' Updates the font object to match the updated info. '''

        self.factive_cell = self.create_font("Live Cells:  " + str(self.game_scene.active_cell), 15)

        if self.status != self.game_scene.state:
            if self.game_scene.state == "run":
                self.fstatus = self.create_font("Status:  " + str(self.game_scene.state).upper(), 15, (0,100,0))
            else:
                self.fstatus = self.create_font("Status:  " + str(self.game_scene.state).upper(), 15, (200,0,0))


    def render_font(self, surface):
        ''' Draws the fonts to the legend display '''

        #renders the font to the legend surface
        surface.blit(self.fcell_count, (10,10))
        surface.blit(self.factive_cell, (10,30))
        surface.blit(self.fcolorcode, (10,70))
        surface.blit(self.fdeath, (10,100))
        surface.blit(self.fbirth, (10,120))
        surface.blit(self.fstatic, (10,140))
        surface.blit(self.fstatus, (10,285))

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
            self.game_scene.active_cell = 0 #kinda redundant but it does the job
        elif self.game_scene.state == "generate":
            self.game_scene.generate()
            self.game_scene.state = "run"


        #updates the font in the legend display
        self.update_font()
        self.status = self.game_scene.state

    def draw(self):
        ''' Rendering the graphics on the display surface '''

        #fills the display surface to a color...alternative to clearing the screen to
        #perform new drawing action.
        self._display_surf.fill((255, 255, 255))

        #calling the draw function for game_scene object.
        self.game_scene.draw()

        #draws all the buttons in the button group.
        for button in self.button_grp:
            button.draw()

        self.legend.fill((255, 255, 255))
        self.render_font(self.legend)   #renders the font to the screen
        #draws the legend display to the main display surface
        self._display_surf.blit(self.legend, (self.legend_x_offset, self.legend_y_offset))

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