import pygame

from models.piece import Piece

class Player:
    """
    Represents a player in the game, managing their pieces, moves, and status.
    """

    def __init__(self, id:int) -> None:
        """
        Initializes a Player object.

        Args:
            id (int): The unique identifier for the player.
        """
        self.screen = pygame.display.get_surface()
        self.id = id
        self.pieces = []
        self.selected_piece = -1
        self.is_selected_piece = False
        self.played = False

    def is_win(self) -> bool:
        """
        Checks if the player has won the game.

        Returns:
            bool: True if the player has no more pieces, False otherwise.
        """
        return not self.pieces

    def add_piece(self, piece:Piece) -> None:
        """
        Adds a piece to the player's collection.

        Args:
            piece (Piece): The piece to be added to the player's collection.
        """
        self.pieces.append(piece)
    
    def play_piece(self) -> Piece:
        """
        Plays the selected piece and removes it from the player's collection.

        Returns:
            Piece: The piece that was played
        """
        self.played = True
        return self.pieces.pop(self.selected_piece)

    def can_play(self, last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> bool:
        """
        Determines if the player can play any of their pieces based on the last pieces played.

        Args:
            last_pieces (dict[tuple[int, int]]): The last pieces played.
            starting_double (tuple[int, int]): The starting double piece.

        Returns:
            bool: True if the player can play at least one piece, False otherwise.
        """
        for i in range(len(self.pieces)):
            playable_sides = self.get_piece_playable_sides(piece_id=i, 
                                                           last_pieces=last_pieces, 
                                                           starting_double=starting_double)
            if any(playable_sides):
                return True
        return False
    
    def get_atual_piece_values(self) -> tuple[int, int]:
        """
        Retrieves the values of the currently selected piece.

        Returns:
            tuple[int, int]:  values of the selected piece
        """
        return (-1, -1) if not self.pieces else self.pieces[self.selected_piece].values

    def draw(self) -> None:
        """
        Draws the player's pieces on the screen.

        Note:
            This method is currently a placeholder and does not perform any actions.
        """
        pass

    def update(self) -> None:
        """
        Updates the player's state and handles interactions.

        Note:
            This method is currently a placeholder and does not perform any actions.
        """
        pass
