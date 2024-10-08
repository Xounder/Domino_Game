import pygame, sys

from resources.settings import *
from services.control import Control
from services.start_window import StartWindow

from managers.timer_manager import TimerManager

from models.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Dominó')
        self.clock = pygame.time.Clock()

        self.control_game = Control()
        self.start_window = StartWindow(self.control_game.active_game)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            TimerManager.update_timers()

            if self.control_game.active: # MODIFICAR A FORMA DE UPDATE
                self.control_game.draw()
                self.control_game.update()
            else:
                self.start_window.draw()
                self.start_window.update()

            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()