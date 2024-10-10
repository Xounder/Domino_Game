import pygame
from random import randint

import resources.settings as config
from models import AIPlayer, HumanPlayer, Piece, Map
from utils.screen import Painter
from managers.timer_manager import TimerManager

class Control:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.active = False
        self.WIN = 1
        self.DRAW = 2
        self.RUN = 0

        self.map_game = Map()
        self.import_pieces_assets()

        self.player_message_timer = 'player_message_timer'
        self.message_timer = 'message_timer'
        TimerManager.add_timer(self.player_message_timer, duration=1)
        TimerManager.add_timer(self.message_timer, duration=3)

    def active_game(self, players:list[str], dual_mode:bool) -> None:
        self.all_pieces = config.domino_pieces[:]
        self.game_status = self.RUN 
        self.ply_id = 0
        self.dual_mode = dual_mode
        self.active = True
        self.map_game.start_game()
        self.create_players(players)
        self.distribute_pieces()

    def create_players(self, players:list[str]) -> None:
        self.players = []
        for i, ply_type in enumerate(players):
            if ply_type == config.PLAYER:
                self.players.append(HumanPlayer(i))
            else:
                self.players.append(AIPlayer(i))

    def next_player(self) -> None:
        atual_player = self.get_atual_player()
        atual_player.reset()
        self.ply_id = self.get_player_id(qnt_next=1)
        while self.players[self.ply_id].is_win():
            self.ply_id = self.get_player_id(qnt_next=1)
        TimerManager.active_timer(self.player_message_timer)
            
    def import_pieces_assets(self) -> None:
        self.pieces_surf = {'up': [], 'down': [], 'left': [], 'right': []}
        for key in self.pieces_surf:
            pieces_surf = [pygame.image.load(f'img/pieces/{key}/{i}.png').convert() for i in range(7)]
            self.pieces_surf[key] = [pygame.transform.scale(pieces_surf[i], 
                                        (config.TILE_SIZE/2, config.TILE_SIZE/2)) for i in range(7)]
            
    def distribute_pieces(self) -> None:
        starting_double = (-1, -1)
        pieces_players = []
        piece_player = []

        while starting_double == (-1, -1):
            pieces_players = []
            piece_player = []
            for ply in self.players:
                for i in range(7):
                    piece = self.buy_piece()
                    if piece.is_double() and piece.values[0] > starting_double[0]:
                        starting_double = piece.values
                        self.ply_id = ply.id
                    piece_player.append(piece)

                pieces_players.append(piece_player[:])
                piece_player.clear()

        self.map_game.starting_double = starting_double   
        for i in range(len(self.players)):
            for piece in pieces_players[i]:
                self.players[i].add_piece(piece) 

    def buy_piece(self) -> Piece:
        choosed_piece = randint(0, self.get_remaining_pieces() - 1)
        piece_values = self.all_pieces.pop(choosed_piece)
        piece_assets = self.get_pieces_assets(piece_values)
        return Piece(piece_values, piece_assets)
    
    def get_atual_player(self) -> Player:
        return self.players[self.ply_id]
    
    def get_remaining_pieces(self) -> int:
        return len(self.all_pieces)     

    def get_piece_asset(self, piece_value:int) -> dict[str, pygame.Surface]:
        piece_asset = {}
        for key, value in self.pieces_surf.items():
            piece_asset[key] = value[piece_value]
        return piece_asset
    
    def get_pieces_assets(self, piece_values: tuple[int, int]) -> tuple[dict, dict]:
        piece_assets = tuple(self.get_piece_asset(piece_value) for piece_value in piece_values)
        return piece_assets
    
    def get_player_id(self, qnt_next:int) -> int:
        return (self.ply_id + qnt_next) % len(self.players)
    
    def get_message_to_draw(self) -> str:
        if self.game_status == self.RUN:
            message = f'Player {self.ply_id + 1}'
        elif self.game_status == self.WIN:
                message = f'P{self.ply_id + 1} '
                if self.dual_mode:
                    second_id = self.get_player_id(qnt_next=2)
                    message += f'& P{second_id + 1} ' 
                message += 'WIN' 
        else:
            message = 'D R A W'

        return message
    
    def can_buy(self) -> bool:
        return self.get_remaining_pieces() > 0

    def is_win(self) -> bool:
        atual_player = self.get_atual_player()
        if atual_player.is_win():
            index = self.get_player_id(qnt_next=2)
            if self.dual_mode and not self.players[index].is_win():
                return False
            
            self.game_status = self.WIN
            self.active_end_game_message()
            return True
        return False

    def is_draw(self) -> bool:
        if self.get_remaining_pieces() > 0: return False
        
        for ply in self.players:
            if ply.can_play(last_pieces=self.map_game.last_pieces, 
                            starting_double=self.map_game.starting_double):
                return False
        self.game_status = self.DRAW
        self.active_end_game_message()
        return True
    
    def active_end_game_message(self) -> None:
        TimerManager.active_timer(self.message_timer)
    
    def draw_message(self, message:str) -> None:
        Painter.draw_message(screen=self.screen, 
                             size=(300, 100), 
                             center_pos=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2),
                             dist=3,
                             message=message,
                             text_color='red',
                             f_color='red',
                             b_color='#ffffef')

    def draw(self) -> None:
        if self.game_status == self.RUN:
            self.map_game.draw()
            if TimerManager.is_run(self.player_message_timer):
                self.draw_message(self.get_message_to_draw())

            self.get_atual_player().draw(can_buy=self.can_buy(), 
                                        last_pieces=self.map_game.last_pieces, 
                                        starting_double=self.map_game.starting_double)
        else: # Win and Draw
            if TimerManager.is_run(self.message_timer):
                self.draw_message(self.get_message_to_draw())

    def update(self) -> None:
        if self.game_status == self.RUN:
            atual_player = self.get_atual_player()
            if not atual_player.played:
                atual_player.update(can_buy=self.can_buy(), 
                                    buy_piece=self.buy_piece, 
                                    last_pieces=self.map_game.last_pieces, 
                                    starting_double=self.map_game.starting_double)
            else:
                if self.is_win(): return
                if self.is_draw(): return
                self.next_player()
        
            self.map_game.update(piece_value=atual_player.get_atual_piece_values(), 
                                is_selected_piece=atual_player.is_selected_piece, 
                                get_player_piece=atual_player.play_piece)
        else:
            if not TimerManager.is_run(self.message_timer):
                self.active = False
