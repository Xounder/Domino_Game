import pygame

from models.player import Player

class AIPlayer(Player): 
    def __init__(self, id: int) -> None:
        super().__init__(id)

    def update(self) -> None:
        pass