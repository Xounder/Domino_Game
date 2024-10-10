import pygame

from models.piece import Piece

class Player:
    def __init__(self, id:int) -> None:
        self.screen = pygame.display.get_surface()
        self.id = id
        self.pieces = []
        self.selected_piece = -1
        self.is_selected_piece = False
        self.played = False

    def is_win(self) -> bool:
        return not self.pieces

    def add_piece(self, piece:Piece) -> None:
        self.pieces.append(piece)
    
    def play_piece(self) -> Piece:
        self.played = True
        return self.pieces.pop(self.selected_piece)

    def can_play(self, last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> bool:
        for i in range(len(self.pieces)):
            playable_sides = self.get_piece_playable_sides(piece_id=i, 
                                                           last_pieces=last_pieces, 
                                                           starting_double=starting_double)
            if any(playable_sides):
                return True
        return False
    
    def get_atual_piece_values(self) -> tuple[int, int]:
        return (-1, -1) if not self.pieces else self.pieces[self.selected_piece].values

    def draw(self) -> None:
        pass

    def update(self) -> None:
        pass
