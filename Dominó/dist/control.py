import pygame
from settings import *
from map import Map
from player import Player
from timer import Timer

class Control:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.run_game = False
        self.active_timer_once = True
        self.map_game = Map(self.blit_shadow_text)
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
