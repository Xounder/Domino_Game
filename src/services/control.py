import pygame
from random import randint

from models.piece import Piece
import resources.settings as config
from models.map import Map
from models.player import Player
from utils.timer import Timer

class Control: # FALTA A UNIÃO COM O MAPA
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.WIN = 1
        self.DRAW = 2
        self.RUN = 0

        self.map_game = Map()
        self.import_pieces_assets()

        self.active_game([config.PLAYER, config.PLAYER], False) # REMOVER

    def active_game(self, players:list[str], dual:bool) -> None:
        self.all_pieces = config.domino_pieces[:]
        self.game_status = self.RUN 
        self.ply_id = 0
        self.active = True
        self.dual = dual
        self.starting_double = [-1, -1]
        self.map_game.start_game()
        self.create_players(players)
        self.distribute_pieces()

    def create_players(self, players:list[str]) -> None:
        self.players = []
        for i, ply_type in enumerate(players):
            if ply_type == config.INACTIVE: 
                continue
            if ply_type == config.PLAYER:
                self.players.append(Player(i))
            if ply_type == config.AI:
                #self.players.append(AIPlayer(i))
                pass

    def next_player(self) -> None:
        atual_player = self.get_atual_player()
        atual_player.reset()
        self.ply_id = (self.ply_id + 1) % len(self.players)
            
    def import_pieces_assets(self) -> None:
        self.pieces_surf = {'up': [], 'down': [], 'left': [], 'right': []}
        for key in self.pieces_surf:
            pieces_surf = [pygame.image.load(f'img/pieces/{key}/{i}.png').convert() for i in range(7)]
            self.pieces_surf[key] = [pygame.transform.scale(pieces_surf[i], 
                                        (config.TILE_SIZE/2, config.TILE_SIZE/2)) for i in range(7)]
            
    def distribute_pieces(self) -> None:
        for ply in self.players:
            for i in range(7):
                piece = self.buy_piece()
                if piece.is_double() and piece.values[0] > self.starting_double[0]:
                    self.starting_double = piece.values
                    self.ply_id = ply.id
                ply.add_piece(piece)    

    def buy_piece(self) -> Piece:
        choosed_piece = randint(0, self.get_remaining_pieces() - 1)
        piece_values = self.all_pieces.pop(choosed_piece)
        piece_assets = self.get_pieces_assets(piece_values)
        return Piece(piece_values, piece_assets)
    
    def get_atual_player(self) -> Player:
        return self.players[self.ply_id]
    
    def get_remaining_pieces(self) -> int:
        return len(self.all_pieces)     
            
    def can_buy(self) -> bool:
        return self.get_remaining_pieces() > 0

    def get_piece_asset(self, piece_value:int) -> dict[str, pygame.Surface]:
        piece_asset = {}
        for key, value in self.pieces_surf.items():
            piece_asset[key] = value[piece_value]
        return piece_asset
    
    def get_pieces_assets(self, piece_values: tuple[int, int]) -> tuple[dict, dict]:
        piece_assets = tuple(self.get_piece_asset(piece_value) for piece_value in piece_values)
        return piece_assets
    
    def is_win(self) -> bool:
        if self.get_atual_player().is_win():
            self.game_status = self.WIN
            return True
        return False

    def is_draw(self) -> bool:
        if self.get_remaining_pieces() > 0: return False
        
        for ply in self.players:
            if ply.can_play(last_pieces={'right':(0, 0), 'left':(0, 0)}): # modificar
                return False
        self.game_status = self.DRAW
        return True
    
    def draw(self) -> None:
        self.map_game.draw()
        self.get_atual_player().draw(can_buy=self.can_buy(), last_pieces={'right':(0, 0), 'left':(0, 0)}) # modificar

    def update(self) -> None:
        atual_player = self.get_atual_player()
        if not atual_player.played:
            atual_player.update(can_buy=self.can_buy(), buy_piece=self.buy_piece)
        else:
            if self.is_win(): return
            if self.is_draw(): return
            self.next_player()
            