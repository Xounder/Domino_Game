import pygame
from random import randint

import resources.settings as config
from models import AIPlayer, HumanPlayer, Piece, Map, Player
from utils.screen import Painter
from managers import TimerManager, SoundManager

class Control:
    """
    Manages the game logic, player turns, piece distribution, game state (win, draw, running), and drawing messages.
    """

    def __init__(self):
        """
        Initializes the Control class, setting up the game state, timers, and the map.
        """
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
        """
        Starts the game with the specified players and mode. Initializes game elements such as the map and players.

        Args:
            players (list[str]): List of player types ('HumanPlayer' or 'AIPlayer').
            dual_mode (bool): Whether the game is in dual mode (teams of two players).
        """
        self.all_pieces = config.domino_pieces[:]
        self.game_status = self.RUN 
        self.ply_id = 0
        self.dual_mode = dual_mode
        self.active = True
        self.map_game.start_game()
        self.create_players(players)
        self.distribute_pieces()

    def create_players(self, players:list[str]) -> None:
        """
        Creates player instances based on the provided player types.

        Args:
            players (list[str]): List of player types ('HumanPlayer' or 'AIPlayer').
        """
        self.players = []
        for i, ply_type in enumerate(players):
            if ply_type == config.PLAYER:
                self.players.append(HumanPlayer(i))
            else:
                self.players.append(AIPlayer(i))

    def next_player(self) -> None:
        """
        Advances to the next player, resetting the current player's state and checking for a win condition.
        """
        atual_player = self.get_atual_player()
        atual_player.reset()
        self.ply_id = self.get_player_id(qnt_next=1)
        while self.players[self.ply_id].is_win():
            self.ply_id = self.get_player_id(qnt_next=1)
        TimerManager.active_timer(self.player_message_timer)
            
    def import_pieces_assets(self) -> None:
        """
        Loads and scales the image assets for the domino pieces.
        """
        self.pieces_surf = {'up': [], 'down': [], 'left': [], 'right': []}
        for key in self.pieces_surf:
            pieces_surf = [pygame.image.load(f'img/pieces/{key}/{i}.png').convert() for i in range(7)]
            self.pieces_surf[key] = [pygame.transform.scale(pieces_surf[i], 
                                        (config.TILE_SIZE/2, config.TILE_SIZE/2)) for i in range(7)]
            
    def distribute_pieces(self) -> None:
        """
        Distributes domino pieces to players and determines the starting double piece.
        """
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
        """
        Buys a random piece from the remaining pieces and returns a Piece object.

        Returns:
            Piece: The purchased piece.
        """
        choosed_piece = randint(0, self.get_remaining_pieces() - 1)
        piece_values = self.all_pieces.pop(choosed_piece)
        piece_assets = self.get_pieces_assets(piece_values)
        return Piece(piece_values, piece_assets)
    
    def get_atual_player(self) -> Player:
        """
        Returns the current player based on the player ID.

        Returns:
            Player: The current player object.
        """
        return self.players[self.ply_id]
    
    def get_remaining_pieces(self) -> int:
        """
        Returns the number of remaining pieces in the game.

        Returns:
            int: The number of remaining pieces.
        """
        return len(self.all_pieces)     

    def get_piece_asset(self, piece_value:int) -> dict[str, pygame.Surface]:
        """
        Returns the image asset for a given piece value.

        Args:
            piece_value (int): The value of the domino piece.

        Returns:
            dict[str, pygame.Surface]: A dictionary containing image assets for the piece.
        """
        piece_asset = {}
        for key, value in self.pieces_surf.items():
            piece_asset[key] = value[piece_value]
        return piece_asset
    
    def get_pieces_assets(self, piece_values: tuple[int, int]) -> tuple[dict, dict]:
        """
        Returns the image assets for two given piece values.

        Args:
            piece_values (tuple[int, int]): The values of the two domino pieces.

        Returns:
            tuple[dict, dict]: A tuple containing dictionaries of image assets for both pieces.
        """
        piece_assets = tuple(self.get_piece_asset(piece_value) for piece_value in piece_values)
        return piece_assets
    
    def get_player_id(self, qnt_next:int) -> int:
        """
        Returns the ID of the next player based on the current player ID.

        Args:
            qnt_next (int): The number of players to skip.

        Returns:
            int: The ID of the next player.
        """
        return (self.ply_id + qnt_next) % len(self.players)
    
    def get_message_to_draw(self) -> str:
        """
        Returns the message to be displayed based on the current game status (running, win, or draw).

        Returns:
            str: The message to be displayed.
        """
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
        """
        Returns whether the current player can buy a piece.

        Returns:
            bool: True if the player can buy a piece, False otherwise.
        """
        return self.get_remaining_pieces() > 0

    def is_win(self) -> bool:
        """
        Checks if the current player has won the game.

        Returns:
            bool: True if the current player has won, False otherwise.
        """
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
        """
        Checks if the game has ended in a draw.

        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        if self.get_remaining_pieces() > 0: return False
        
        for ply in self.players:
            if ply.can_play(last_pieces=self.map_game.last_pieces, 
                            starting_double=self.map_game.starting_double):
                return False
        self.game_status = self.DRAW
        self.active_end_game_message()
        return True
    
    def active_end_game_message(self) -> None:
        """
        Activates the end game message timer to display the win/draw message.
        """
        TimerManager.active_timer(self.message_timer)
        sound_name = 'draw' if self.game_status == self.DRAW else 'won'
        SoundManager.play_sound(sound_name=sound_name)
    
    def draw_message(self, message:str) -> None:
        """
        Draws the message to the screen.

        Args:
            message (str): The message to be displayed.
        """
        Painter.draw_message(screen=self.screen, 
                             size=(300, 100), 
                             center_pos=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2),
                             dist=3,
                             message=message,
                             text_color='red',
                             f_color='red',
                             b_color='#ffffef')

    def draw(self) -> None:
        """
        Draws the game state on the screen, including the map and player message if the game is running.
        """
        self.map_game.draw()
        if self.game_status == self.RUN:
            if TimerManager.is_run(self.player_message_timer):
                self.draw_message(self.get_message_to_draw())

            self.get_atual_player().draw(can_buy=self.can_buy(), 
                                        last_pieces=self.map_game.last_pieces, 
                                        starting_double=self.map_game.starting_double)
        else: # Win and Draw
            if TimerManager.is_run(self.message_timer):
                self.draw_message(self.get_message_to_draw())

    def update(self) -> None:
        """
        Updates the game state, processes the current player's turn, and checks for win or draw conditions.
        """
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
