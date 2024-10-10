from models.player import Player

class AIPlayer(Player): 
    """
    A class representing an AI-controlled player in the game. Inherits from the Player class.
    """
    
    def __init__(self, id: int) -> None:
        """
        Initializes an AIPlayer object with the specified player ID.

        Args:
            id (int): The unique identifier for the AI player.
        """
        super().__init__(id)

    def update(self) -> None:
        """
        Updates the AI player's state during its turn. Currently not implemented.
        """
        pass