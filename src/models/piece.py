import pygame

import resources.settings as config

class Piece:
    def __init__(self, values:tuple[int, int], all_surf_piece:tuple[dict, dict]) -> None:
        self.values = values
        self.first_surf_piece = all_surf_piece[0]
        self.second_surf_piece = all_surf_piece[1]

    def is_double(self) -> bool:
        return self.values[0] == self.values[1]
    
    def is_playable(self, last_pieces:dict[tuple[int, int]]) -> tuple[bool, bool]:
        right, left = last_pieces.keys()

        if last_pieces[right] == last_pieces[left]:
            is_double = self.is_double()
            return (is_double, is_double)
        
        return tuple(self.values[0] == piece[1] or self.values[1] == piece[1] for piece in last_pieces.values())
    
    def get_piece_orientantion(self, orientation:str) -> tuple[str, str]:
        if orientation == config.PIECE_DIRECTION_UP:
            piece_orientation = [config.PIECE_DIRECTION_DOWN, config.PIECE_DIRECTION_UP]            

        elif orientation == config.PIECE_DIRECTION_LEFT:
            piece_orientation = [config.PIECE_DIRECTION_RIGHT, config.PIECE_DIRECTION_LEFT]

        elif orientation == config.PIECE_DIRECTION_RIGHT:
            piece_orientation = [config.PIECE_DIRECTION_LEFT, config.PIECE_DIRECTION_RIGHT]

        else: # DOWN and CENTER
            piece_orientation = [config.PIECE_DIRECTION_UP, config.PIECE_DIRECTION_DOWN]

        return piece_orientation
    
    def get_piece_surfaces(self, piece_orientation:str, player:bool=False, size:tuple[int, int]=[]) -> tuple:
        first_surf = self.first_surf_piece[piece_orientation[0]]
        second_surf = self.second_surf_piece[piece_orientation[1]]

        if player:
            first_surf = pygame.transform.scale(first_surf, size)
            second_surf = pygame.transform.scale(second_surf, size)
            
        return (first_surf, second_surf)

    def draw(self, screen:pygame.display, first_pos:tuple[int, int], second_pos:tuple[int, int], 
                    orientation:str, player:bool=False, size:tuple[int, int]=[]) -> None:
        piece_orientation = self.get_piece_orientantion(orientation)
        first_surf, second_surf = self.get_piece_surfaces(piece_orientation, player, size)
                                                   
        screen.blit(first_surf, first_pos) 
        screen.blit(second_surf, second_pos)

    '''def draw_pieces_table(self, piece, pos, type_piece):
        # desenha as peças que foram jogadas/estão na mesa
        x = pos[0]
        y = pos[1]        
        if type_piece == 'mid': #mid center
            self.display_surface.blit(self.pieces_surf['up'][piece[0]], (x + tile_size/4, y)) 
            self.display_surface.blit(self.pieces_surf['down'][piece[1]], (x + tile_size/4, y + tile_size/2))
        elif type_piece == 'right': #right
            self.display_surface.blit(self.pieces_surf['left'][piece[0]], (x - tile_size/4, y + tile_size/4))
            self.display_surface.blit(self.pieces_surf['right'][piece[1]], (x + tile_size/4, y + tile_size/4))
        elif type_piece == 'left': #left
            self.display_surface.blit(self.pieces_surf['right'][piece[0]], (x + 3*tile_size/4, y + tile_size/4))
            self.display_surface.blit(self.pieces_surf['left'][piece[1]], (x + tile_size/4, y + tile_size/4))
        elif type_piece == 'up': #up right/left
            self.display_surface.blit(self.pieces_surf['up'][piece[1]], (x + tile_size/4, y + tile_size/4))
            self.display_surface.blit(self.pieces_surf['down'][piece[0]], (x + tile_size/4, y + 3*tile_size/4))
        elif type_piece == 'down': #down right/left
            self.display_surface.blit(self.pieces_surf['up'][piece[0]], (x + tile_size/4, y - tile_size/4))
            self.display_surface.blit(self.pieces_surf['down'][piece[1]], (x + tile_size/4, y + tile_size/4))'''

