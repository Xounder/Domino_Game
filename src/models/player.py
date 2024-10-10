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
        self.MAX_PIECES_ON_SCREEN = 7

        self.bottom_size_y = 120

        buy_pass_size = (120, 50)
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

        self.choose_piece_size = (55, 90)
        pos = (self.choose_piece_size[0] + 10, config.SCREEN_HEIGHT - self.bottom_size_y/2)
        self.choose_piece_button = [Button(self.choose_piece_size, (255 + i * pos[0], pos[1]), 3) 
                                                                    for i in range(7)]
        self.reset()

    def reset(self) -> None:
        self.section = 0
        self.selected_piece = -1
        self.is_selected_piece = False
        self.is_show_pieces = False
        self.is_next_section = False
        self.is_prev_section = False
        self.played = False

    def is_win(self) -> bool:
        return not self.pieces

    def add_piece(self, piece:Piece) -> None:
        self.pieces.append(piece)
    
    def play_piece(self) -> Piece:
        self.played = True
        return self.pieces.pop(self.selected_piece)

    def can_play(self, last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> bool:
        for i in range(len(self.pieces)):
            playable_sides = self.get_piece_playable_sides(piece_id=i, 
                                                           last_pieces=last_pieces, 
                                                           starting_double=starting_double)
            if any(playable_sides):
                return True
        return False
    
    def get_piece_playable_sides(self, piece_id:int, 
                                 last_pieces:dict[tuple[int, int]], 
                                 starting_double:tuple[int, int]) -> tuple[bool, bool]:
        return self.pieces[piece_id].is_playable(last_pieces, starting_double)
    
    def get_atual_piece_values(self) -> tuple[int, int]:
        return (-1, -1) if not self.pieces else self.pieces[self.selected_piece].values

    def get_visible_pieces_index(self) -> tuple[int, int]:
        start_index = self.section * self.MAX_PIECES_ON_SCREEN
        end_index = min(start_index + self.MAX_PIECES_ON_SCREEN, len(self.pieces))
        return (start_index, end_index)

    def get_section_index(self, pos:int) -> int:
        return pos + self.get_visible_pieces_index()[0]

    def get_visible_pieces(self) -> list[Piece]:
        start_index, end_index = self.get_visible_pieces_index()
        return self.pieces[start_index:end_index]
    
    def get_visible_pieces_size(self) -> int:
        return len(self.get_visible_pieces())

    def draw(self, can_buy:bool, last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> None:
        self.draw_bottom_elements(can_buy, last_pieces, starting_double)
    
    def draw_bottom_elements(self, can_buy:bool, 
                             last_pieces:dict[tuple[int, int]], 
                             starting_double:tuple[int, int]) -> None:
        Painter.draw_rect(screen=self.screen, size=(config.SCREEN_WIDTH, self.bottom_size_y), 
                          pos=(0, config.SCREEN_HEIGHT - self.bottom_size_y), dist=5, b_color='#A0522D')
        
        Painter.blit_text_shadow(screen=self.screen, text=f'P{self.id + 1}', 
                                color='red', pos=(10, config.SCREEN_HEIGHT - (self.bottom_size_y - 10)))
        
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

            self.draw_player_pieces(last_pieces, starting_double)
        
    def draw_player_pieces(self, last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> None:
        if self.pieces:
            for i, piece in enumerate(self.get_visible_pieces()):
                button_pos = self.choose_piece_button[i].get_rect(topleft=True)
                half_piece_height = self.choose_piece_size[1]/2

                first_pos = button_pos
                second_pos = (button_pos[0], button_pos[1] + half_piece_height)
                size = (self.choose_piece_size[0], half_piece_height)

                piece.draw(self.screen, first_pos, second_pos, config.PIECE_DIRECTION_DOWN, 
                           player=True, size=size)

                # Indicator Rects                
                piece_pos = (button_pos, self.choose_piece_size)
                piece_index = self.get_section_index(pos=i)
                if not self.is_selected_piece:
                    if any(self.get_piece_playable_sides(piece_id=piece_index, 
                                                         last_pieces=last_pieces, 
                                                         starting_double=starting_double)):
                        pygame.draw.rect(self.screen, 'green', piece_pos, 3)
                else:
                    if piece_index == self.selected_piece:
                        pygame.draw.rect(self.screen, 'red', piece_pos, 3)

    def update(self, can_buy:bool, buy_piece:Callable[[], Piece], 
               last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> None:
        self.validate_sections()
        self.input(can_buy, buy_piece, last_pieces, starting_double)

    def choose_piece(self):
        for i in range(self.get_visible_pieces_size()):
            if self.choose_piece_button[i].is_pressed():
                if self.get_section_index(pos=i) == self.selected_piece:
                    self.deselect_piece()
                    return
                
                self.select_piece(self.get_section_index(pos=i))

    def select_piece(self, pos:int) -> None:
        self.selected_piece = pos
        self.is_selected_piece = True

    def deselect_piece(self) -> None:
        self.is_selected_piece = False
        self.selected_piece = -1

    def validate_sections(self) -> None:
        qnt_pieces = self.get_visible_pieces_size()
        start_index, end_index = self.get_visible_pieces_index()
        size_pieces_list = len(self.pieces)

        if start_index == 0 and end_index == size_pieces_list:
            self.is_next_section = self.is_prev_section = False
        else:
            self.is_prev_section = start_index > 0
            self.is_next_section = qnt_pieces >= self.MAX_PIECES_ON_SCREEN and end_index != size_pieces_list
        
    def input(self, can_buy:bool, buy_piece:Callable[[], Piece], 
              last_pieces:dict[tuple[int, int]], starting_double:tuple[int, int]) -> None:
        if not self.is_show_pieces:
            self.is_show_pieces = self.show_button.is_pressed()
        else:
            if self.is_next_section and self.next_section_button.is_pressed():
                self.section += 1

            if self.is_prev_section and self.prev_section_button.is_pressed():
                self.section -= 1
            
            if not self.can_play(last_pieces, starting_double):
                if can_buy:
                    if self.buy_button.is_pressed():
                        self.deselect_piece()
                        self.add_piece(buy_piece())
                else:
                    if self.pass_button.is_pressed():
                        self.played = True

            self.choose_piece()
