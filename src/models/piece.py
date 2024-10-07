import pygame

import resources.settings as config

class Piece:
    def __init__(self, values:tuple[int, int], all_surf_piece:tuple[dict, dict]) -> None:
        self.values = values
        self.first_surf_piece = all_surf_piece[0]
        self.second_surf_piece = all_surf_piece[1]

    def is_double(self) -> bool:
        return self.values[0] == self.values[1]
    
    def is_playable(self, last_pieces:dict[tuple[int, int]]):
        right, left = last_pieces.keys()

        if last_pieces[right] == last_pieces[left]:
            return self.is_double()
        
        return any(self.values[0] == piece[1] or self.values[1] == piece[1] for piece in last_pieces.values())

    def draw(self, screen:pygame.display, pos:tuple[int, int], orientation:str) -> None:
        if orientation == config.PIECE_DIRECTION_UP:
            piece_orientation = [config.PIECE_DIRECTION_DOWN, config.PIECE_DIRECTION_UP]            

        elif orientation == config.PIECE_DIRECTION_LEFT:
            piece_orientation = [config.PIECE_DIRECTION_RIGHT, config.PIECE_DIRECTION_LEFT]

        elif orientation == config.PIECE_DIRECTION_RIGHT:
            piece_orientation = [config.PIECE_DIRECTION_LEFT, config.PIECE_DIRECTION_RIGHT]

        else: # DOWN and CENTER
            piece_orientation = [config.PIECE_DIRECTION_UP, config.PIECE_DIRECTION_DOWN]
                
        screen.blit(self.first_surf_piece[piece_orientation[0]], pos) 
        screen.blit(self.second_surf_piece[piece_orientation[1]], pos)
