import pygame, sys

import resources.settings as config
from services.control import Control
from services.start_window import StartWindow

from managers.timer_manager import TimerManager
from managers.updater_manager import UpdaterManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption('Dominó')
        self.clock = pygame.time.Clock()

        background = pygame.image.load('img/background.jpg').convert()
        self.background = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.background_rect = self.background.get_rect(topleft= (0, 0))

        self.game_controller = Control()
        self.start_window = StartWindow()
        UpdaterManager.set_exclusive_update(self.start_window, self.start_game)
        
    def start_game(self) -> None:
        self.game_controller.active_game(self.start_window.players, 
                                         self.start_window.dual_mode_button.pressed)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background, self.background_rect)

            if self.start_window.active:
                self.start_window.draw()
            else:
                UpdaterManager.set_exclusive_update(self.game_controller, self.start_window.initialize)

            if self.game_controller.active:
                self.game_controller.draw()
            else:
                UpdaterManager.set_exclusive_update(self.start_window, self.start_game)

            TimerManager.update_timers()
            UpdaterManager.update()

            pygame.display.update()
            self.clock.tick(60)


game = Game()
game.run()
