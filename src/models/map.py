from typing import Callable
import pygame

import resources.settings as config
from models.piece import Piece
from utils.screen import RectButton

class Map:
    """
    A class representing the game board, managing the placement and drawing of pieces on the board.
    """

    def __init__(self) -> None:
        """
        Initializes the Map object, setting up buttons, pieces positions, and sides.
        """
        self.screen = pygame.display.get_surface()
        self.pieces_pos = config.pieces_pos
        self.RIGHT = 'right'
        self.LEFT = 'left'

        button_size = (25, 25)
        self.button_left = RectButton(button_size, (0, 0), 3, topleft=True)
        self.button_right = RectButton(button_size, (0, 0), 3, topleft=True)

    def start_game(self) -> None:
        """
        Initializes game state for starting a new round. Resets pieces, positions, and sides.
        """
        self.starting_double = []
        self.board_pieces = []
        self.board_pieces_orientation = []
        self.board_pieces_sides = []
        self.last_pieces = {
            self.RIGHT: (0, 0),
            self.LEFT: (0, 0)
        }
        self.next_position = {
            self.RIGHT: 0,
            self.LEFT: 0
        }
        self.valid_placement_sides = {
            self.RIGHT: False,
            self.LEFT: False
        }

    def add_piece_on_board(self, piece:Piece, piece_side:str, orientation:str) -> None:
        """
        Adds a piece to the board in the specified orientation and side.

        Args:
            piece (Piece): The piece to add to the board.
            piece_side (str): The side (right/left) where the piece is placed.
            orientation (str): The orientation of the piece (up, down, left, right).
        """
        if piece.values[0] != self.last_pieces[piece_side][1]:
            piece.reverse_piece(piece_side)
            
        if len(self.board_pieces) == 0:
            self.next_position[self.RIGHT] += 1 
            self.next_position[self.LEFT] += 1 
            self.last_pieces[self.RIGHT] = piece.values
            self.last_pieces[self.LEFT] = piece.values
        else:
            self.next_position[piece_side] += 1 
            self.last_pieces[piece_side] = piece.values

        self.board_pieces.append(piece)
        self.board_pieces_sides.append(piece_side)
        self.board_pieces_orientation.append(orientation)

    def calculate_piece_surfaces_pos(self, piece_pos:tuple[int, int], orientation:str) -> tuple[tuple, tuple]:
        """
        Calculates the screen positions for the two sides of a piece based on its orientation.

        Args:
            piece_pos (tuple[int, int]): The coordinates of the piece on the board.
            orientation (str): The orientation of the piece.

        Returns:
            tuple[tuple, tuple]: The positions for both sides of the piece on the screen.
        """
        x, y = piece_pos
        tile_map = config.TILE_SIZE/4
        x_plus_tile, y_plus_tile = x + tile_map, y + tile_map

        if orientation == config.PIECE_DIRECTION_CENTER:
            return ((x_plus_tile, y), (x_plus_tile, y + config.TILE_SIZE/2))
        elif orientation == config.PIECE_DIRECTION_RIGHT:
            first_pos = (x - tile_map, y_plus_tile)
        elif orientation == config.PIECE_DIRECTION_LEFT:
            first_pos = (x + 3 * tile_map, y_plus_tile)
        elif orientation == config.PIECE_DIRECTION_UP:
            return ((x_plus_tile, y_plus_tile), (x_plus_tile, y + 3 * tile_map))
        elif orientation == config.PIECE_DIRECTION_DOWN:
            first_pos = (x_plus_tile, y - tile_map)
    
        return (first_pos, (x_plus_tile, y_plus_tile))

    def get_piece_surfaces_map_pos(self, piece_id:int, piece_side:str, orientation:str) -> tuple[tuple, tuple]:
        """
        Retrieves the position on the map for the piece surfaces based on its side and orientation.

        Args:
            piece_id (int): The ID of the piece.
            piece_side (str): The side of the board (right/left) where the piece is placed.
            orientation (str): The orientation of the piece.

        Returns:
            tuple[tuple, tuple]: The screen positions for both sides of the piece.
        """
        piece_pos = self.pieces_pos[piece_side][piece_id]
        map_pos = list(map(lambda x: x * config.TILE_SIZE, piece_pos))
        return self.calculate_piece_surfaces_pos(piece_pos=map_pos, 
                                                 orientation=orientation)
                
    def draw(self) -> None:
        """
        Draws all board pieces and available placement options for the next piece.
        """
        self.draw_board_pieces()
        self.draw_next_piece_options()

    def draw_board_pieces(self) -> None:
        """
        Draws all pieces currently placed on the board, with their respective positions and orientations.
        """
        piece_side_id = {
            self.RIGHT: 0, 
            self.LEFT: 0
        }

        for i, piece in enumerate(self.board_pieces):
            piece_side = self.board_pieces_sides[i]
            piece_id = piece_side_id[piece_side]
            orientation = self.board_pieces_orientation[i]

            first_pos, second_pos = self.get_piece_surfaces_map_pos(piece_id, piece_side, orientation)
            piece.draw(self.screen, first_pos, second_pos, self.board_pieces_orientation[i])   

            if i == 0:
                piece_side_id[self.LEFT] += 1
                piece_side_id[self.RIGHT] += 1
            else:
                piece_side_id[piece_side] += 1

    def draw_next_piece_options(self) -> None:
        """
        Draws buttons indicating the possible placement options for the next piece.
        """
        for side, can_place in self.valid_placement_sides.items():
            if can_place:
                button = self.button_left if side == self.LEFT else self.button_right
                self.draw_option_button(side, button)
            
    def draw_option_button(self, piece_side:str, button:RectButton) -> None:
        """
        Draws a button at the next valid placement position for a piece.

        Args:
            piece_side (str): The side (right/left) where the button should be placed.
            button (RectButton): The button object to draw.
        """
        piece_pos = self.pieces_pos[piece_side][self.next_position[piece_side]]
        pos = list(map(lambda x: x * config.TILE_SIZE + config.TILE_SIZE/2, piece_pos))

        button.set_rect(pos)
        button.draw_button(self.screen, f_color='red' if piece_side == self.RIGHT else 'blue')

    def find_placement_side(self, piece_to_add:tuple[int, int]) -> tuple[bool, bool]:
        """
        Determines which side of the board (right/left) can accommodate the next piece based on its values.

        Args:
            piece_to_add (tuple[int, int]): The values of the piece to be placed.

        Returns:
            tuple[bool, bool]: A tuple indicating if the piece can be placed on either side.
        """
        if len(self.board_pieces) == 0:
            self.valid_placement_sides[self.RIGHT] = self.starting_double
        else:
            for side, last_piece in self.last_pieces.items():
                self.valid_placement_sides[side] = last_piece[1] in piece_to_add

    def update(self, piece_value:tuple[int, int], is_selected_piece:bool, 
                    get_player_piece:Callable[[], Piece]) -> None:
        """
        Updates the state of the board, handles piece placement logic based on player input.

        Args:
            piece_value (tuple[int, int]): The values of the piece the player wants to place.
            is_selected_piece (bool): Indicates if the player has selected a piece to place.
            get_player_piece (Callable[[], Piece]): A callable that returns the selected piece for the player.
        """
        if is_selected_piece:  
            self.find_placement_side(piece_value)

            if self.valid_placement_sides[self.RIGHT] and self.button_right.is_pressed():
                piece_side = self.RIGHT
            elif self.valid_placement_sides[self.LEFT] and self.button_left.is_pressed():
                piece_side = self.LEFT
            else:
                piece_side = None

            if piece_side:
                player_piece = get_player_piece()
                orientation = config.pieces_orientation[piece_side][self.next_position[piece_side]]
                self.add_piece_on_board(player_piece, piece_side, orientation)
                self.valid_placement_sides[self.RIGHT] = False
                self.valid_placement_sides[self.LEFT] = False
