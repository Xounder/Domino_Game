from typing import Callable
import pygame

import resources.settings as config
from models.piece import Piece
from utils.screen import Painter, RectButton, Button

class Player:
    def __init__(self, id:int) -> None:
        self.screen = pygame.display.get_surface()
        self.id = id
        self.pieces = []
        self.section = 0
        self.MAX_PIECES_ON_SCREEN = 7
        self.selected_piece = 0
        self.is_selected_piece = False
        self.is_show_pieces = False
        self.is_next_section = False
        self.is_prev_section = False
        self.played = False

        self.bottom_size_y = 200

        buy_pass_size = (120, 70)
        gap = 20
        self.buy_button = RectButton(buy_pass_size, (buy_pass_size[0]/2 + gap, 
                                                     config.SCREEN_HEIGHT - self.bottom_size_y/2), 3)
        self.pass_button = RectButton(buy_pass_size, (buy_pass_size[0]/2 + gap, 
                                                      config.SCREEN_HEIGHT - self.bottom_size_y/2), 3)

        next_prev_size = (50, 50)
        self.next_section_button = RectButton(next_prev_size, (config.SCREEN_WIDTH - 60, 
                                                               config.SCREEN_HEIGHT - self.bottom_size_y/2), 3)
        self.prev_section_button = RectButton(next_prev_size, (180, 
                                                               config.SCREEN_HEIGHT - self.bottom_size_y/2), 3)

        self.show_button = RectButton((180, 100), (config.SCREEN_WIDTH/2, 
                                                   config.SCREEN_HEIGHT - self.bottom_size_y/2), 3)
        #Mudar para button
        choose_piece_size = (55, 90)
        self.choose_piece_button = [RectButton(choose_piece_size, (255 + i * (choose_piece_size[0] + 10), 
                                                                   config.SCREEN_HEIGHT - self.bottom_size_y/2), 3) 
                                                                   for i in range(7)]

    def add_piece(self, piece:Piece) -> None:
        self.pieces.append(piece)
    
    def remove_piece(self) -> None:
        self.pieces.pop(self.selected_piece)

    def get_visible_pieces_index(self) -> tuple[int, int]:
        start_index = self.section * self.MAX_PIECES_ON_SCREEN
        end_index = min(start_index + self.MAX_PIECES_ON_SCREEN, len(self.pieces))
        return (start_index, end_index)

    def get_visible_pieces(self) -> list[Piece]:
        start_index, end_index = self.get_visible_pieces_index()
        return self.pieces[start_index:end_index]
    
    def get_visible_pieces_size(self) -> int:
        return len(self.get_visible_pieces())

    def draw(self, can_buy:bool) -> None:
        self.draw_bottom_elements(can_buy)
    
    def draw_bottom_elements(self, can_buy:bool) -> None:
        Painter.draw_rect(screen=self.screen, size=(config.SCREEN_WIDTH, self.bottom_size_y), 
                          pos=(0, config.SCREEN_HEIGHT - self.bottom_size_y), dist=5, b_color='#A0522D')
        
        if not self.is_show_pieces:
            self.show_button.draw_text_button(screen=self.screen, text='S H O W', text_color='red', font_size=42)
        else:
            if can_buy:
                self.buy_button.draw_text_button(screen=self.screen, text='BUY', text_color='red', font_size=42)
            else:
                self.pass_button.draw_text_button(screen=self.screen, text='PASS', text_color='red', font_size=42)

            if self.is_next_section:
                self.next_section_button.draw_text_button(screen=self.screen, text='>', text_color='red', font_size=42)

            if self.is_prev_section:
                self.prev_section_button.draw_text_button(screen=self.screen, text='<', text_color='red', font_size=42)

            Painter.blit_text_shadow(screen=self.screen, text=f'P{self.id + 1}', 
                                    color='red', pos=(10, config.SCREEN_HEIGHT - (self.bottom_size_y - 10)))
            
            self.draw_player_pieces()
        
            for i in range(self.get_visible_pieces_size()): ## REMOVER
                self.choose_piece_button[i].draw_button(self.screen)

    def draw_player_pieces(self) -> None:
        if self.pieces:
            x_space = 0
            for piece in self.get_visible_pieces():
                pos = (20 + x_space, config.SCREEN_HEIGHT - self.bottom_size_y)
                #piece.draw(self.screen, pos, config.PIECE_DIRECTION_DOWN)
                #Modificar a cor da peça se ela é playable ou se está selecionada
                x_space += 10

        
    def update(self, can_buy:bool, buy_piece:Callable[[], Piece]) -> None:
        self.validate_sections()
        self.input(can_buy, buy_piece)

    def choose_piece(self):
        for i in range(self.get_visible_pieces_size()):
            if self.choose_piece_button[i].is_pressed():
                self.selected_piece = i + self.get_visible_pieces_index()[0]
    
    def validate_sections(self) -> None:
        qnt_pieces = self.get_visible_pieces_size()
        start_index, end_index = self.get_visible_pieces_index()
        size_pieces_list = len(self.pieces)

        if start_index == 0 and end_index == size_pieces_list:
            self.is_next_section = self.is_prev_section = False
        else:
            self.is_prev_section = start_index > 0
            self.is_next_section = qnt_pieces >= self.MAX_PIECES_ON_SCREEN and end_index != size_pieces_list
        
    def input(self, can_buy:bool, buy_piece:Callable[[], Piece]):
        if not self.is_show_pieces:
            self.is_show_pieces = self.show_button.is_pressed()
        else:
            if self.is_next_section and self.next_section_button.is_pressed():
                self.section += 1

            if self.is_prev_section and self.prev_section_button.is_pressed():
                self.section -= 1
            
            if can_buy:
                if self.buy_button.is_pressed():
                    self.add_piece(buy_piece())
            else:
                if self.pass_button.is_pressed():
                    self.played = True

            self.choose_piece()
