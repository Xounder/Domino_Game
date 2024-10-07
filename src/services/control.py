import pygame
from resources.settings import *
from models.map import Map
from models.player import Player
from utils.timer import Timer

class Control:
    # Remover os draws daqui
    # Conterá o controle do jogo

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.run_game = False
        self.active_timer_once = True
        self.map_game = Map()
        # win surface
        win_surf = pygame.image.load('img/win.png').convert()
        self.win_surf = pygame.transform.scale(win_surf, (win_surf.get_width()*2, win_surf.get_height()*2))
        self.win_rect = self.win_surf.get_rect(center= (screen_width/2, screen_height/2))
        # draw surface
        draw_surf = pygame.image.load('img/draw.png').convert()
        self.draw_surf = pygame.transform.scale(draw_surf, (draw_surf.get_width()*2, draw_surf.get_height()*2))
        self.draw_rect = self.draw_surf.get_rect(center = (screen_width/2, screen_height/2))
        # draw e win msg
        self.show_msg_timer = Timer(1.5)
        self.font_win = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.ply_win_surf = None
        self.ply_win_rect = None
            
    def active_game(self, qnt_ply, dual):
        self.create_players(qnt_ply, dual)
        self.run_game = True
        self.active_timer_once = True

    def create_players(self, qnt_ply, dual):
        self.players = [Player() for i in range(qnt_ply)]
        self.map_game.game_assets(self.players, dual)

    def draw(self):
        self.map_game.draw()
        self.draw_end_game()
        
    def draw_end_game(self):
        if self.map_game.win: # win
            if self.show_msg_timer.run:
                self.display_surface.blit(self.win_surf, self.win_rect)
                if not self.map_game.dual:
                    text = f'{self.map_game.winner + 1}' 
                else:
                    text = '1 & 3' if (self.map_game.winner + 1) == 1 or (self.map_game.winner + 1) == 2 else '2 & 4'
                self.blit_shadow_text(text, (screen_width/2, screen_height/2))
            else:
                if not self.active_timer_once:
                    self.run_game = False
        if self.map_game.draw_game: # draw
            if self.show_msg_timer.run:
                self.display_surface.blit(self.draw_surf, self.draw_rect)
            else:
                if not self.active_timer_once:
                    self.run_game = False

    def blit_shadow_text(self, text, pos):
        self.ply_win_surf = self.font_win.render(text, False, 'black')
        self.ply_win_rect = self.ply_win_surf.get_rect(center= (pos[0] + 1, pos[1] + 1))
        self.display_surface.blit(self.ply_win_surf, self.ply_win_rect)
        self.ply_win_surf = self.font_win.render(text, False, 'black')
        self.ply_win_rect = self.ply_win_surf.get_rect(center= (pos[0] - 1, pos[1] - 1))
        self.display_surface.blit(self.ply_win_surf, self.ply_win_rect)
        self.ply_win_surf = self.font_win.render(text, False, 'red')
        self.ply_win_rect = self.ply_win_surf.get_rect(center= (pos[0], pos[1]))
        self.display_surface.blit(self.ply_win_surf, self.ply_win_rect)

    def update(self):
        if self.show_msg_timer.run:
            self.show_msg_timer.update()

        if not self.map_game.draw_game and not self.map_game.win:
            self.map_game.update()
        else:
            if self.active_timer_once:
                self.show_msg_timer.active()
                self.active_timer_once = False





    '''def next_player(self):               ####### CONTROLLER #######
        # passa para o proximo player
        self.show_player_pieces = False
        self.show_piece_surf = self.show_piece_img[0]
        self.atual_player.piece_choosed = False
        if not self.check_win():
            is_draw = False
            if self.id_player == self.first_player:
                is_draw = self.check_draw()
            if not is_draw:
                self.atual_player.section = 0
                if self.id_player < len(self.players)-1:
                    self.id_player += 1
                else:
                    self.id_player = 0
                self.atual_player = self.players[self.id_player]'''

    '''def check_win(self):               ####### CONTROLLER #######
        # verifica se o atual jogador venceu
        if len(self.players[self.id_player].pieces) == 0:
            self.win = True
            self.winner = self.id_player
            return True
        return False'''

    '''def check_draw(self):               ####### CONTROLLER #######
        # verifica se deu empate
        if len(self.all_pieces) > 0:
            return False
        else:
            for player in self.players:
                for piece in player.pieces:
                    if self.is_playable(piece):
                        return False
        self.draw_game = True
        return True'''
    



    '''def distribuition_pieces(self):                ####### CONTROLLER + PLAYER #######
        for i, player in enumerate(self.players):
            for j in range(7):
                piece = self.buy_piece()
                if piece[0] == piece[1] and piece[0] > self.entry_piece[0]:
                    self.entry_piece = piece[:]
                    self.id_player = i
                    self.first_player = i
                    self.atual_player = self.players[self.id_player]
                player.buy_piece(piece[:])'''
    

    '''def buy_piece(self):                ####### CONTROLLER #######
        choosed = randint(0, len(self.all_pieces)-1)
        piece = self.all_pieces[choosed][:]
        self.all_pieces.pop(choosed)
        if len(self.all_pieces) == 0:
            self.buy_pass_surf = self.buy_pass_img[1]
        return piece'''
    
                
    '''def import_pieces_assets(self):                ####### CONTROLLER #######
        self.pieces_surf = {'up': [], 'down': [], 'left': [], 'right': []}
        for key in self.pieces_surf:
            pieces_surf = [pygame.image.load(f'img/pieces/{key}/{i}.png').convert() for i in range(7)]
            self.pieces_surf[key] = [pygame.transform.scale(pieces_surf[i], (tile_size/2, tile_size/2)) for i in range(7)]'''