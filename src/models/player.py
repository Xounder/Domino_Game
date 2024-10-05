import pygame
from settings.settings import *

class Player:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.pieces = []
        self.section = 0
        self.choose_piece = 0
        self.piece_choosed = False

    def buy_piece(self, piece):
        self.pieces.append(piece)
    
    def remove_piece(self):
        self.pieces.pop(self.choose_piece)
        
