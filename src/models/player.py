import pygame
from resources.settings import *

class Player:
    # Inputs serão passados para ca
    # Conterá as regras das logicas de escolha da peça e inserção delas no mapa 
    # (passsará a peça para o mapa qnd escolhida)
    # Atualizará as peças (update, draw)

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
        
