map = [
    [22,   21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10],
    [23,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9],
    [24,   25, 26, 27,  0,  0,  0,  0,  0,  0,  0,  0,  8],
    [0,     0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  7],
    [-6,   -5, -4, -3, -2, -1,  0,  1,  2,  3,  4,  5,  6],
    [-7,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [-8,    0,  0,  0,  0,  0,  0,  0,  0,-27,-26,-25,-24],
    [-9,    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,-23],
    [-10, -11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22]]

import pygame
from settings import *
from random import randint
from timer import Timer

class Map:
    def __init__(self, blit_shadow_text):
        self.display_surface = pygame.display.get_surface()
        # manage all pieces in map and receive pieces from players or give it to them
        self.map = map
        self.all_pieces = domino_pieces[:]
        self.players = None
        self.atual_player = None
        self.id_player = 0
        self.first_player = 0
        self.dual = False
        self.show_player_pieces = False
        self.win = False
        self.winner = 0
        self.draw_game = False
        # peças colocadas na mesa
        self.placed_pieces = []
        self.last_piece = [[0, 0], [0, 0]] #L/R
        self.next_place = [0, 0] # L/R
        self.entry_piece = [-1, -1]

        self.surf = pygame.Surface((tile_size, tile_size))
        background = pygame.image.load('img/background.jpg').convert() # <- site: https://wallpapercave.com/wood-wallpapers
        self.background = pygame.transform.scale(background, (screen_width, screen_height))
        self.background_rect = self.background.get_rect(topleft= (0, 0))
        # table player
        table_player = pygame.image.load('img/baixo.png').convert()
        self.table_ply = pygame.transform.scale(table_player, (screen_width, table_player.get_height()))
        self.table_ply_rect = self.table_ply.get_rect(topleft= (0, screen_height - self.table_ply.get_height())) 
        # collisions
        y_pos = screen_height - self.table_ply.get_height() + 10
            # buy or pass
        self.buy_pass_img = [pygame.image.load('img/buy.png').convert(), pygame.image.load('img/pass.png').convert()]
        self.buy_pass_surf = self.buy_pass_img[0]
        self.buy_pass_rect = self.buy_pass_surf.get_rect(topleft= (12, y_pos + 2))
            # choose piece
        self.choose_piece_surf = [pygame.Surface((55, 90)) for i in range(7)]
        self.choose_piece_rect = [self.choose_piece_surf[i].get_rect(topleft= (155 + (i*86), y_pos + 2)) for i in range(7)]
            # next section
        next_section_surf = pygame.image.load('img/next.png')
        self.next_section_surf = pygame.transform.scale(next_section_surf, (35, 35))
        self.next_section_rect = self.next_section_surf.get_rect(topleft= (screen_width - 40, y_pos + 30))
            # previous section
        self.prev_section_surf = pygame.transform.rotate(self.next_section_surf, 180)
        self.prev_section_rect = self.prev_section_surf.get_rect(topleft= (107, y_pos + 30))
            # place piece (*wasd*)
        self.place_piece_surf = [pygame.Surface((30, 30)) for i in range(2)]
        self.place_piece_rect = [self.place_piece_surf[i].get_rect(topleft= (0, 0)) for i in range(2)]
        self.place_piece_surf[0].fill('purple')
        self.place_piece_surf[1].fill('green')
            # show piece
        self.show_piece_img = [pygame.image.load('img/show0.png').convert(), pygame.image.load('img/show1.png').convert()]
        self.show_piece_surf = self.show_piece_img[0]
        self.show_piece_rect = self.show_piece_surf.get_rect(topleft= (screen_width - 35, y_pos))
        # mouse
        self.mouse_surf = pygame.Surface((5,5))
        self.mouse_rect = self.mouse_surf.get_rect(center= (0, 0))
        self.mouse_timer = Timer(0.5)
        # blit_text
        self.blit_shadow_text = blit_shadow_text

    def game_assets(self, players, dual):
        self.all_pieces = domino_pieces[:]
        self.show_player_pieces = False
        self.win = False
        self.winner = 0
        self.draw_game = False
        # peças colocadas na mesa
        self.placed_pieces = []
        self.last_piece = [[0, 0], [0, 0]] #L/R
        self.next_place = [0, 0] # L/R
        self.entry_piece = [-1, -1]

        self.players = players
        self.dual = dual
        self.distribuition_pieces()
        self.import_pieces_assets()

    def distribuition_pieces(self):
        for i, player in enumerate(self.players):
            for j in range(7):
                piece = self.buy_piece()
                if piece[0] == piece[1] and piece[0] > self.entry_piece[0]:
                    self.entry_piece = piece[:]
                    self.id_player = i
                    self.first_player = i
                    self.atual_player = self.players[self.id_player]
                player.buy_piece(piece[:])
                
    def import_pieces_assets(self):
        self.pieces_surf = {'up': [], 'down': [], 'left': [], 'right': []}
        for key in self.pieces_surf:
            pieces_surf = [pygame.image.load(f'img/pieces/{key}/{i}.png').convert() for i in range(7)]
            self.pieces_surf[key] = [pygame.transform.scale(pieces_surf[i], (tile_size/2, tile_size/2)) for i in range(7)]

    def buy_piece(self):
        choosed = randint(0, len(self.all_pieces)-1)
        piece = self.all_pieces[choosed][:]
        self.all_pieces.pop(choosed)
        if len(self.all_pieces) == 0:
            self.buy_pass_surf = self.buy_pass_img[1]
        return piece

    def next_player(self):
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
                self.atual_player = self.players[self.id_player]

    def check_win(self):
        # verifica se o atual jogador venceu
        if len(self.players[self.id_player].pieces) == 0:
            self.win = True
            self.winner = self.id_player
            return True
        return False

    def check_draw(self):
        # verifica se deu empate
        if len(self.all_pieces) > 0:
            return False
        else:
            for player in self.players:
                for piece in player.pieces:
                    if self.is_playable(piece):
                        return False
        self.draw_game = True
        return True
        
    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if not self.show_player_pieces:
                    if self.mouse_rect.colliderect(self.show_piece_rect):
                        self.show_player_pieces = not self.show_player_pieces
                        self.show_piece_surf = self.show_piece_img[self.show_player_pieces]
                else:
                    if self.mouse_rect.colliderect(self.buy_pass_rect):
                        if len(self.all_pieces) > 0: # compra
                            if self.next_place[0] != self.next_place[1]:
                                self.atual_player.buy_piece(self.buy_piece())
                        else:
                            self.next_player()
                    elif (self.atual_player.section + 1) * 7 < len(self.atual_player.pieces) and self.mouse_rect.colliderect(self.next_section_rect):
                                self.atual_player.section += 1
                    elif self.atual_player.section > 0 and self.mouse_rect.colliderect(self.prev_section_rect):
                        self.atual_player.section -= 1
                    else:
                        self.choose_piece()       
                        # place local
                        if self.atual_player.piece_choosed:
                            if self.next_place[0] == self.next_place[1]: # first_piece
                                place = self.check_place_piece()
                                if place[0]:
                                    self.add_piece_placed(first= True)
                            else:    
                                place = self.check_place_piece()
                                for i, place_rect in enumerate(self.place_piece_rect):
                                    if place[i] and self.mouse_rect.colliderect(place_rect):
                                        self.add_piece_placed(right= (True if i == 1 else False))

                self.mouse_timer.active()

    def add_piece_placed(self, right=False, first=False):
        # adiciona a peça jogada (pelo player) a mesa
        piece = self.atual_player.pieces[self.atual_player.choose_piece]
        if first: 
            info = domino_pieces_posR[self.next_place[1]]
            self.next_place[0] -= 1
            self.next_place[1] += 1
            self.last_piece[0] = piece
            self.last_piece[1] = piece
        else:
            if right:
                if piece[0] == self.last_piece[1][1]:
                    pass
                else:
                    piece = [piece[1], piece[0]]
                info = domino_pieces_posR[self.next_place[1]]
                self.next_place[1] += 1
                self.last_piece[1] = piece
            else:
                if piece[0] == self.last_piece[0][1]:
                    pass
                else:
                    piece = [piece[1], piece[0]]
                info = domino_pieces_posL[abs(self.next_place[0])]
                self.next_place[0] -= 1
                self.last_piece[0] = piece

        self.atual_player.remove_piece()
        self.atual_player.piece_choosed = False
        self.placed_pieces.append([piece, info[0], info[1]])
        self.next_player()
                
    def choose_piece(self):
        # o player escolhe a peça desejada
        if not self.atual_player.piece_choosed:
            len_pieces = (len(self.atual_player.pieces)-1) - (7 * self.atual_player.section)
            for i, piece_rect in enumerate(self.choose_piece_rect):
                if i <= len_pieces and self.mouse_rect.colliderect(piece_rect):
                    self.atual_player.choose_piece = i + (7 * self.atual_player.section) 
                    self.atual_player.piece_choosed = True
        else:
            index = self.atual_player.choose_piece - (7 * self.atual_player.section) 
            if self.mouse_rect.colliderect(self.choose_piece_rect[index]):
                self.atual_player.piece_choosed = False

    def is_playable(self, piece):
        # verifica se a peça pode ser jogada ou não
        if self.next_place[0] == self.next_place[1]: # first_piece
            if piece[0] == piece[1] and piece == self.entry_piece:
                return True
        else:
            for last_piece in self.last_piece:
                if piece[0] == last_piece[1] or piece[1] == last_piece[1]:
                    return True
        return False
        
    def check_place_piece(self):
        # verifica qual lado (L/R) pode ser jogada a peça
        piece = self.atual_player.pieces[self.atual_player.choose_piece]
        place = [False, False]
        if self.next_place[0] == self.next_place[1]:
            if piece[0] == piece[1] and piece == self.entry_piece:
                place = [True, True]
        else:
            for i, last_piece in enumerate(self.last_piece):
                if piece[0] == last_piece[1] or piece[1] == last_piece[1]:
                    place[i] = True
        return place

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        self.input()

    def draw_ply_pieces(self, section_pieces):
        y_pos = screen_height - self.table_ply.get_height() + 12
        for i, piece in enumerate(section_pieces):
            x_pos = 155 + (i * 86)
            # background piece
            if self.atual_player.piece_choosed:
                if self.atual_player.choose_piece - (7 * self.atual_player.section) == i:
                    color = 'red'
                else:
                    color = 'white'
            else: 
                color = 'green' if self.is_playable(piece) else 'white' 
            self.choose_piece_surf[i].fill(color)
            self.display_surface.blit(self.choose_piece_surf[i], self.choose_piece_rect[i])
            # piece
            piece_surf_up = pygame.transform.scale(self.pieces_surf['up'][piece[0]], (50, 40))
            piece_surf_down = pygame.transform.scale(self.pieces_surf['down'][piece[1]], (50, 40))
            self.display_surface.blit(piece_surf_up, (x_pos + 3, y_pos + 5)) 
            self.display_surface.blit(piece_surf_down, (x_pos + 3, y_pos + 45))

    def draw_bottom_elements(self):
        # desenha a parte inferior da tela
        self.display_surface.blit(self.table_ply, self.table_ply_rect)
        self.display_surface.blit(self.buy_pass_surf, self.buy_pass_rect)
        # player pieces
        if self.show_player_pieces:
            limit_pieces = [self.atual_player.section * 7, (self.atual_player.section + 1) * 7]
            if limit_pieces[1] > len(self.atual_player.pieces):
                limit_pieces = [self.atual_player.section * 7, len(self.atual_player.pieces)]
            section_pieces = self.atual_player.pieces[limit_pieces[0]:limit_pieces[1]]
            self.draw_ply_pieces(section_pieces)
            # next//previous section
            if (self.atual_player.section + 1) * 7 < len(self.atual_player.pieces):
                self.display_surface.blit(self.next_section_surf, self.next_section_rect)
            if self.atual_player.section > 0:
                self.display_surface.blit(self.prev_section_surf, self.prev_section_rect)
        # show//player_id
        self.display_surface.blit(self.show_piece_surf, self.show_piece_rect)
        self.blit_shadow_text(f'P{self.id_player + 1}', (screen_width - 23, screen_height - 15))

    def draw_pieces_table(self, piece, pos, type_piece):
        # desenha as peças que foram jogadas/estão na mesa
        x = pos[0]
        y = pos[1]        
        if type_piece == 'mid': #mid center
            self.display_surface.blit(self.pieces_surf['up'][piece[0]], (x + tile_size/4, y)) 
            self.display_surface.blit(self.pieces_surf['down'][piece[1]], (x + tile_size/4, y + tile_size/2))
        elif type_piece == 'right': #right
            self.display_surface.blit(self.pieces_surf['left'][piece[0]], (x - tile_size/4, y + tile_size/4))
            self.display_surface.blit(self.pieces_surf['right'][piece[1]], (x + tile_size/4, y + tile_size/4))
        elif type_piece == 'left': #left
            self.display_surface.blit(self.pieces_surf['right'][piece[0]], (x + 3*tile_size/4, y + tile_size/4))
            self.display_surface.blit(self.pieces_surf['left'][piece[1]], (x + tile_size/4, y + tile_size/4))
        elif type_piece == 'up': #up right/left
            self.display_surface.blit(self.pieces_surf['up'][piece[1]], (x + tile_size/4, y + tile_size/4))
            self.display_surface.blit(self.pieces_surf['down'][piece[0]], (x + tile_size/4, y + 3*tile_size/4))
        elif type_piece == 'down': #down right/left
            self.display_surface.blit(self.pieces_surf['up'][piece[0]], (x + tile_size/4, y - tile_size/4))
            self.display_surface.blit(self.pieces_surf['down'][piece[1]], (x + tile_size/4, y + tile_size/4))

    def draw_next_piece_place(self):
        # desenha os proximos locais para jogar as peças
        if self.atual_player.piece_choosed:
            place = self.check_place_piece()
            if place[0]:
                pos_l = domino_pieces_posL[abs(self.next_place[0])][0]
                self.place_piece_rect[0].topleft = [pos_l[0] * tile_size + 15, pos_l[1] * tile_size + 15]
                self.display_surface.blit(self.place_piece_surf[0], self.place_piece_rect[0])
            if place[1]:
                pos_r = domino_pieces_posR[self.next_place[1]][0]
                self.place_piece_rect[1].topleft = [pos_r[0] * tile_size + 15, pos_r[1] * tile_size + 15]
                self.display_surface.blit(self.place_piece_surf[1], self.place_piece_rect[1])

    def draw(self):
        self.display_surface.blit(self.background, self.background_rect)
        self.draw_bottom_elements()
        self.draw_next_piece_place()
        for piece in self.placed_pieces:
            self.draw_pieces_table(piece[0], [piece[1][0] * tile_size, piece[1][1] * tile_size], piece[2])