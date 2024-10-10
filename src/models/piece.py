import pygame

import resources.settings as config

class Piece:
    """
    A class representing a game piece with two sides, each having a value. Handles piece properties, drawing,
    and playable conditions.
    """

    def __init__(self, values:tuple[int, int], all_surf_piece:tuple[dict, dict]) -> None:
        """
        Initializes a Piece object.

        Args:
            values (tuple[int, int]): A tuple containing the values of the piece's two sides.
            all_surf_piece (tuple[dict, dict]): Two dictionaries that hold the image surfaces for each side of the piece.
        """
        self.values = values
        self.first_surf_piece = all_surf_piece[0]
        self.second_surf_piece = all_surf_piece[1]

    def is_double(self) -> bool:
        """
        Checks if the piece is a double (both sides have the same value).

        Returns:
            bool: True if the piece is a double, False otherwise.
        """
        return self.values[0] == self.values[1]
    
    def is_playable(self, last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> tuple[bool, bool]:
        """
        Checks if the piece can be played based on the last played pieces and the starting double piece.

        Args:
            last_pieces (dict[tuple[int, int]]): A dictionary of the last played pieces, with their positions.
            starting_double (tuple[int, int]): The values of the starting double piece.

        Returns:
            tuple[bool, bool]: A tuple indicating whether the piece is playable on both sides.
        """
        right, left = last_pieces.keys()

        if last_pieces[right] == last_pieces[left] == (0, 0):
            is_starting_double = starting_double == self.values
            return (is_starting_double, is_starting_double)
        
        return tuple(self.values[0] == piece[1] or self.values[1] == piece[1] for piece in last_pieces.values())
    
    def get_piece_orientantion(self, orientation:str) -> tuple[str, str]:
        """
        Determines the piece's orientation based on the given direction.

        Args:
            orientation (str): The current direction of the piece (e.g., 'UP', 'DOWN').

        Returns:
            tuple[str, str]: The orientations for the two sides of the piece.
        """
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
        """
        Retrieves the surfaces (images) for the piece based on its orientation and whether it is controlled by a player.

        Args:
            piece_orientation (str): The orientation of the piece (up, down, left, right).
            player (bool): Indicates if the piece is controlled by a player. Default is False.
            size (tuple[int, int]): The size to scale the piece if it's a player's piece.

        Returns:
            tuple: The surfaces for both sides of the piece.
        """
        first_surf = self.first_surf_piece[piece_orientation[0]]
        second_surf = self.second_surf_piece[piece_orientation[1]]

        if player:
            first_surf = pygame.transform.scale(first_surf, size)
            second_surf = pygame.transform.scale(second_surf, size)
            
        return (first_surf, second_surf)
    
    def reverse_piece(self, piece_direction:str) -> None:
        """
        Reverses the piece values and surfaces based on the given direction.

        Args:
            piece_direction (str): The direction in which to reverse the piece (up, down, etc.).
        """
        self.values.reverse()
        self.first_surf_piece, self.second_surf_piece = self.second_surf_piece, self.first_surf_piece

    def draw(self, screen:pygame.display, first_pos:tuple[int, int], second_pos:tuple[int, int], 
                    orientation:str, player:bool=False, size:tuple[int, int]=[]) -> None:
        """
        Draws the piece on the screen at the specified positions, with the given orientation.

        Args:
            screen (pygame.display): The surface on which to draw the piece.
            first_pos (tuple[int, int]): The position of the first half of the piece.
            second_pos (tuple[int, int]): The position of the second half of the piece.
            orientation (str): The orientation of the piece (up, down, left, right).
            player (bool): Indicates if the piece is controlled by a player. Default is False.
            size (tuple[int, int]): The size to scale the piece if it's a player's piece.
        """
        piece_orientation = self.get_piece_orientantion(orientation)
        first_surf, second_surf = self.get_piece_surfaces(piece_orientation, player, size)
                                                   
        screen.blit(first_surf, first_pos if orientation != config.PIECE_DIRECTION_UP else second_pos) 
        screen.blit(second_surf, second_pos if orientation != config.PIECE_DIRECTION_UP else first_pos)
