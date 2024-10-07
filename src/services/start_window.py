import pygame

import resources.settings as config
from utils.screen import RectButton, CircleButton

class StartWindow:
    def __init__(self, active_game):
        self.display_surface = pygame.display.get_surface()
        self.active_game = active_game
        self.qnt_ply = config.MIN_QUANTITY_PLAYER
        self.dual_mode = False
        
        # Quantity Players - Selectors
        pos = [config.SCREEN_WIDTH/2 - 330, config.SCREEN_HEIGHT/2 - 222]
        self.players_buttons = [RectButton(surf_size=(200, 125), rect_pos=((pos[0] + (i * 200)), pos[1]), 
                                 dist=3, topleft=True)  for i in range(3)]
        
        # Start Button
        self.start_button = RectButton(surf_size=(255, 75), 
                                       rect_pos=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT - 100), 
                                       dist=3, center=True) 

        # Dual Mode Button
        self.dual_mode_button = CircleButton(size=12,
                                            rect_pos=(config.SCREEN_WIDTH - 300, config.SCREEN_HEIGHT/2 - 70), 
                                            colors=['red', 'blue'])

    def draw(self):
        self.start_button.draw_text_button(self.display_surface, text='START', text_color='black', 
                                           font_size=42, text_back_color='white')

        if self.qnt_ply == config.MAX_QUANTITY_PLAYER:
            self.dual_mode_button.draw_text_button(self.display_surface, text='P1 & P3 X P2 & P4',
                                                   text_color='red', text_back_color='white',
                                                   font_size=30, back_color='black')
            
        for i, ply_button in enumerate(self.players_buttons):
            rect_color = 'red' if i + config.MIN_QUANTITY_PLAYER == self.qnt_ply else 'black'

            ply_button.draw_text_button(self.display_surface, 
                                                    text=f'{i + config.MIN_QUANTITY_PLAYER} Players', 
                                                    text_color='black', font_size=42, text_back_color='white', 
                                                    f_color=rect_color)
        
    def update(self):
        self.input()

    def input(self):
        if self.qnt_ply == config.MAX_QUANTITY_PLAYER:
            self.dual_mode = self.dual_mode_button.is_pressed()

        if self.start_button.is_pressed():
            self.active_game(self.qnt_ply, self.dual_mode)

        for i, ply_button in enumerate(self.players_buttons):
            if ply_button.is_pressed(): 
                self.qnt_ply = i + config.MIN_QUANTITY_PLAYER
                break

    def reset(self):
        self.dual_mode = False
        self.qnt_ply = 2
