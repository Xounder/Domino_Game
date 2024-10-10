import pygame

from managers.sound_manager import SoundManager
import resources.settings as config
from utils.screen import RectButton, CircleButton, Painter

class StartWindow:
    """
    Represents the start window of the game where players can select the number of players, type of player, and start the game.
    """

    def __init__(self):
        """
        Initializes the StartWindow class. 
        Sets up buttons for selecting players, the start button, and other related UI elements.
        """
        self.screen = pygame.display.get_surface()
        self.initialize()

        pos = [config.SCREEN_WIDTH/2 - 330, config.SCREEN_HEIGHT/2 - 222]
        size = (200, 125)
        self.players_buttons = [RectButton(surf_size=size, rect_pos=((pos[0] + i * (size[0] + 5)), pos[1]), 
                                 dist=3, topleft=True)  for i in range(3)]
        
        self.start_button = RectButton(surf_size=(255, 75), 
                                       rect_pos=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT - 100), 
                                       dist=3, center=True) 

        self.dual_mode_button = CircleButton(size=12,
                                            rect_pos=(config.SCREEN_WIDTH - 300, config.SCREEN_HEIGHT/2 - 70))
        
        pos = (config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2)
        size = (120, 40)
        self.type_player_button = [RectButton(surf_size=size, rect_pos=(pos[0] + 20, pos[1] + i * (size[1] + 5)), 
                                              dist=3, center= True) for i in range(4)]

    def initialize(self):
        """
        Initializes or resets the player configuration to default settings.
        Sets the default number of players and activates the window.
        """ 
        self.players = [config.PLAYER for i in range(4)]
        self.qnt_ply = config.MIN_QUANTITY_PLAYER
        self.active = True
        SoundManager.play_sound(sound_name='music_theme', loops=-1)

    def draw(self):
        """
        Draws the start window, including buttons for selecting the number of players, player types, and the start button.
        Uses different colors to highlight selected player options.
        """
        self.start_button.draw_text_button(self.screen, text='START', text_color='black', 
                                           font_size=42, text_back_color='white')

        if self.qnt_ply == config.MAX_QUANTITY_PLAYER:
            self.dual_mode_button.draw_text_button(self.screen, text='P1 & P3 X P2 & P4',
                                                   text_color='red', text_back_color='white',
                                                   font_size=30, back_color='black')
            
        for i, ply_button in enumerate(self.players_buttons):
            rect_color = 'red' if i + config.MIN_QUANTITY_PLAYER == self.qnt_ply else 'black'
            ply_button.draw_text_button(self.screen, 
                                        text=f'{i + config.MIN_QUANTITY_PLAYER} Players', 
                                        text_color='black', font_size=42, text_back_color='white', 
                                        f_color=rect_color)
        
        for i in range(self.qnt_ply):
            button = self.type_player_button[i]
            width = button.get_rect(size=True)[0]/2 + 30
            pos = button.get_rect(center=True)

            Painter.blit_text_shadow(self.screen, f'P{i + 1}:', 'red', (pos[0] - width, pos[1]), center=True)
            button.draw_text_button(self.screen, config.type_players[self.players[i]], 'red', 32)

    def update(self):
        """
        Updates the state of the start window
        """
        self.input()

    def input(self):
        """
        Handles logic for selecting the number of players, player types, and triggering the start of the game.
        """
        if self.qnt_ply == config.MAX_QUANTITY_PLAYER:
            self.dual_mode_button.is_pressed()
        else:
            self.dual_mode_button.pressed = False

        if self.start_button.is_pressed():
            self.players = self.players[:self.qnt_ply]
            if self.players.count(config.PLAYER) > 0:
                self.active = False

        for i, ply_button in enumerate(self.players_buttons):
            if ply_button.is_pressed(): 
                self.qnt_ply = i + config.MIN_QUANTITY_PLAYER
                break
        
        for i, type_ply in enumerate(self.type_player_button):
            if type_ply.is_pressed():
                self.players[i] = (self.players[i] + 1) % config.QUANTITY_PLAYER_TYPES
  