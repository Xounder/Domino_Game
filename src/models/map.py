import pygame

import resources.settings as config
from models.piece import Piece
from utils.screen import RectButton

class Map:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.RIGHT = 'right'
        self.LEFT = 'left'

        self.button_left = RectButton((15, 15), (0, 0), 3, topleft=True)
        self.button_right = RectButton((15, 15), (0, 0), 3, topleft=True)
        background = pygame.image.load('img/background.jpg').convert()
        self.background = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.background_rect = self.background.get_rect(topleft= (0, 0))

    def start_game(self):
        self.board_pieces = []
        self.board_pieces_orientation = []
        self.last_pieces = {
            self.RIGHT: (0, 0),
            self.LEFT: (0, 0)
        }
        self.next_position = {
            self.RIGHT: 0,
            self.LEFT: 0
        }

    def add_piece_on_board(self, piece:Piece, piece_side:str, orientation:str):
        if len(self.board_pieces) == 0:
            self.next_position[self.RIGHT] += 1 
            self.next_position[self.LEFT] += 1 
            self.last_pieces[self.RIGHT] = piece.values
            self.last_pieces[self.LEFT] = piece.values
        else:
            if piece.values[0] != self.last_pieces[piece_side][1]:
                piece.values.reverse()

            self.next_position[piece_side] += 1 
            self.last_pieces[piece_side] = piece.values

        self.board_pieces.append(piece)
        self.board_pieces_orientation.append(orientation)
                
    def draw(self):
        self.screen.blit(self.background, self.background_rect)

        for piece in self.board_pieces:
            piece.draw(screen=self.screen, 
                       pos=list(map(lambda x: x * config.TILE_SIZE, piece.values)),
                       orientation=self.board_pieces_orientation)   

    def draw_next_piece_options(self, left:bool, right:bool):
        self.draw_option_button(left)
        self.draw_option_button(right)

    def draw_option_button(self, piece_side:bool):
        piece_pos = config.pieces_pos[piece_side][self.next_position[piece_side]]
        pos = list(map(lambda x: x * config.TILE_SIZE + 15, piece_pos))

        self.button_left.set_rect(pos)
        self.button_left.draw_button(self.screen)

    def find_placement_side(piece_to_add:tuple[int, int]) -> tuple[bool, bool]:
        # verifica qual lado (L/R) pode ser jogada a peça
        pass
