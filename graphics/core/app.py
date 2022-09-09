import pygame
import sys

class Input:
    """Handles the various inputs for applications, such as from the keyboard.
    """
    def __init__(self):
        
        # indicate whether the user has quit the application.
        self._quit = False

        #### Begin extension from 2.5 ####
        # lists for key states
        #   down, up: discrete events that last for one iteration
        #   pressed: continuous events occurring between down and up events
        self.__key_down_list = []
        self.__key_pressed_list = []
        self.__key_up_list = []
        ######## End extension ########

    @property
    def quit(self):
        return self._quit

    @quit.setter
    def quit(self, q):
        self._quit = bool(q)

    @property
    def key_down_list(self):
        return self.__key_down_list

    @property
    def key_pressed_list(self):
        return self.__key_pressed_list

    @property
    def key_up_list(self):
        return self.__key_up_list

    def update(self):
        """Iterate over all user input events (such as keyboard or mouse) that occurred since the last events were checked."""

#### Begin extension from 2.5 ####
        # reset discrete key states
        self.__key_down_list = []
        self.__key_up_list = []
######## End extension ########

        for event in pygame.event.get():
            # quit event occurs by clicking the close button
            if event.type == pygame.QUIT:
                self._quit = True

#### Begin extension from 2.5 ####
            # handle keyboard events
            #   keydown events initiate the pressed state
            #   keyup events terminate the pressed state
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self.__key_down_list.append(key_name)
                self.__key_pressed_list.append(key_name)
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.__key_up_list.append(key_name)
                self.__key_pressed_list.remove(key_name)

    def iskeydown(self, key_code):
        """Checks the down state of the given key"""
        return key_code in self.__key_down_list


    def iskeypressed(self, key_code):
        """Checks the pressed state of the given key"""
        return key_code in self.__key_pressed_list


    def iskeyup(self, key_code):
        """Checks the up state of the given key"""
        return key_code in self.__key_up_list
######## End extension ########


class WindowApp:
    """A basic application window for rendering 3D graphics.
    """
    def __init__(self, screen_size=[512, 512]):

        # initialize all pygame modules
        pygame.init()
        #indicate rendering details
        display_flags = pygame.OPENGL | pygame.DOUBLEBUF
        # initialize buffers to perform antialiasing
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        # use a core OpenGL profile for cross-platform compatibility
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, 
                                        pygame.GL_CONTEXT_PROFILE_CORE)
        # create and display the window
        self.screen = pygame.display.set_mode(screen_size, display_flags)
        # set the text that appears in the title bar of the window
        pygame.display.set_caption("Graphics Window")

        # manage time-related data and operations
        self.clock = pygame.time.Clock()

#### Begin extension from 2.1 ####
        # handle user inputs
        self.input = Input()
######## End extension ########

#### Begin extension from 2.4 ####
        # timekeeper variables
        self.__time = 0
        self.__delta_time = 0

    @property
    def time(self):
        return self.__time

    @property
    def delta_time(self):
        return self.__delta_time
######## End extension ########

    # to be implemented by subclasses !!--- Should be named 'startup' to avoid confusion with __init__ ---!!
    def startup(self):
        pass

    # to be implemented by subclasses
    def update(self):
        pass

    # the main execution method containing all phases of an interactive program
    def run(self):
        # indicate the main loop is active
        running = True

        ## startup ##
        self.startup()

        ## main loop ##
        while running:

#### Begin extenstion from 2.1 ####
            ## process input ##
            self.input.update()
            if self.input.quit:
                running = False
                break
######## End extension ########

#### Begin extension from 2.4 ####
            # calculate seconds since last iteration of the run loop
            self.__delta_time = self.clock.get_time() / 1000
            # increment time application has been running
            self.__time += self.__delta_time
######## End extension #########

            ## update ##
            self.update()

            ## render ##
            # display on the screen
            pygame.display.flip()

            # pause if necessary to achieve 60 FPS
            self.clock.tick(60)

        ## shutdown ##
        pygame.quit()
        sys.exit()