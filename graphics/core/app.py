import pygame
import sys
from abc import ABC, abstractmethod

class Input:
    """ Handles the various inputs for applications, such as from the keyboard. """
    def __init__(self):
        self._quit = False  # whether the user has quit the application.

        # sets for key states
        #   down, up: discrete events that last for one iteration
        #   pressed: continuous events occurring between down and up events
        self.__down_keys = set()
        self.__pressed_keys = set()
        self.__up_keys = set()

    @property
    def quit(self):
        return self._quit

    @quit.setter
    def quit(self, q):
        self._quit = bool(q)

    @property
    def down_keys(self):
        return self.__down_keys

    @property
    def pressed_keys(self):
        return self.__pressed_keys

    @property
    def up_keys(self):
        return self.__up_keys

    def update(self):
        """
        Iterate over all user input events (such as keyboard or mouse) that occurred since the last
        events were checked.
        """

        # reset discrete key states
        self.__down_keys.clear()
        self.__up_keys.clear()

        for event in pygame.event.get():
            # quit event occurs by clicking the close button
            if event.type == pygame.QUIT:
                self._quit = True

            # handle keyboard events
            #   keydown events initiate the pressed state
            #   keyup events terminate the pressed state
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                self.__down_keys.add(key_name)
                self.__pressed_keys.add(key_name)
            if event.type == pygame.KEYUP:
                key_name = pygame.key.name(event.key)
                self.__up_keys.add(key_name)
                self.__pressed_keys.remove(key_name)

    def iskeydown(self, key_code):
        """Checks the down state of the given key"""
        return key_code in self.__down_keys


    def iskeypressed(self, key_code):
        """Checks the pressed state of the given key"""
        return key_code in self.__pressed_keys


    def iskeyup(self, key_code):
        """Checks the up state of the given key"""
        return key_code in self.__up_keys


class WindowApp(ABC):
    """ A basic application window for rendering 3D graphics. """

    def __init__(self, screen_size=(512, 512)):

        # initialize all pygame modules
        pygame.init()

        # specify rendering details
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

        # handle user inputs
        self.input = Input()

        # timekeeper variables
        self.__time = 0
        self.__delta_time = 0

    @property
    def time(self):
        return self.__time

    @property
    def delta_time(self):
        return self.__delta_time

    @abstractmethod
    def startup(self):
        pass

    @abstractmethod
    def update(self):
        pass

    # the main method that runs all the phases of an interactive program
    def run(self):
        # indicate the main loop is active
        running = True

        ## startup ##
        self.startup()

        ## main loop ##
        while running:

            ## process input ##
            self.input.update()
            if self.input.quit:
                running = False
                break

            # calculate seconds since last iteration of the run loop
            self.__delta_time = self.clock.get_time() / 1000
            # increment time application has been running
            self.__time += self.__delta_time

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