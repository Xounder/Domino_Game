import pygame
from settings import *
from timer import Timer

class StartWindow:
    def __init__(self, active_game):
        self.display_surface = pygame.display.get_surface()
        self.active_game = active_game
        self.qnt_ply = 2
        self.dual_mode = False
        # image
        start_surf = pygame.image.load(f'img/start_window.png').convert()
        self.start_surf = pygame.transform.scale(start_surf, (screen_width, screen_height))
        self.start_rect = self.start_surf.get_rect(topleft = (0, 0))
        # rects contacts
        self.players_rect = [pygame.Surface((200, 125)) for i in range(3)]
        self.players_rect_pos = [[screen_width/2 - 328, screen_height/2 - 222], [screen_width/2 - 100, screen_height/2 - 222], [screen_width/2 + 130, screen_height/2 - 222]]
        self.players_rect_rect = [self.players_rect[i].get_rect(topleft= (self.players_rect_pos[i])) for i in range(3)]
        # dual_mode
        dual_bar_surf = pygame.image.load('img/dual.png').convert()
        self.dual_bar_surf = pygame.transform.scale(dual_bar_surf, (dual_bar_surf.get_width()*1.2, dual_bar_surf.get_height()*1.2))
        self.dual_bar_rect = self.dual_bar_surf.get_rect(topleft= (screen_width - 240, screen_height/2 - 70))
        self.dual_circ_surf = pygame.Surface((15, 15))
        self.dual_circ_rect = self.dual_circ_surf.get_rect(center= (screen_width - 228, screen_height/2 - 55))

        self.start_button = pygame.Surface((255, 75))
        self.start_button_rect = self.start_button.get_rect(center= (screen_width/2 - 22, screen_height - 73))
        self.start_button.fill('gray')
        # mouse
        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center = (0, 0))
        self.mouse_timer = Timer(0.5)

    def draw(self):
        self.display_surface.blit(self.start_surf, self.start_rect)
        # players_surf
        for i in range(3):
            color_rect = 'purple' if i == self.qnt_ply - 2 else 'black'
            pygame.draw.rect(self.display_surface, color_rect, [self.players_rect_pos[i][0] - 1, self.players_rect_pos[i][1], 199, 125], 3)
        # start_button
        pygame.draw.rect(self.display_surface, 'red', [self.start_button_rect[0] - 1, self.start_button_rect[1], 256, 75], 3)
        if self.qnt_ply == 4:
            self.display_surface.blit(self.dual_bar_surf, self.dual_bar_rect)
            if self.dual_mode:
                pygame.draw.circle(self.display_surface, 'black', [self.dual_circ_rect[0] + 7, self.dual_circ_rect[1] + 7], 7)

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        self.input()

    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if self.mouse_rect.colliderect(self.start_button_rect):
                    self.active_game(self.qnt_ply, self.dual_mode)
                    self.dual_mode = False
                    self.qnt_ply = 2
                elif self.qnt_ply == 4 and self.mouse_rect.colliderect(self.dual_circ_rect):
                    self.dual_mode = not self.dual_mode
                else:
                    for i, player_rect in enumerate(self.players_rect_rect):
                        if self.mouse_rect.colliderect(player_rect):
                            self.qnt_ply = 2 + i
                            break
                self.mouse_timer.active()