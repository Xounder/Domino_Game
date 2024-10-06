import pygame

from managers.input_manager import InputManager
from utils.painter.inputs.button import Button
from utils.painter.painter import Painter

class CircleButton(Button):
    """
    Represents a clickable circle with optional animation effects.
    """

    def __init__(self, size:int, rect_pos:tuple[int, int], colors:list[str], 
                 center:bool=True, topleft:bool=False) -> None:
        super().__init__((size, size), rect_pos, center, topleft)
        self.colors = colors
        self.radius = size
        self.pressed = False

    def draw_button(self, screen:pygame.display, back_color:str='black') -> None:
        color = self.colors[1] if self.pressed else back_color
        pygame.draw.circle(screen, self.colors[0], self.rect.center, self.radius, 3)
        pygame.draw.circle(screen, color, self.rect.center, int(self.radius/2))

    def draw_text_button(self, screen:pygame.display, text:str, text_color:str,
                        text_back_color:str='black', font_size:int=42, back_color='black'):
        gap = [self.radius/2 + 5, font_size/3]
        pos = (self.rect.right + gap[0], self.rect.centery - gap[1])

        self.draw_button(screen, back_color=back_color)
        Painter.blit_text_shadow(screen, text, text_color, pos, 
                                 back_color=text_back_color, font_size=font_size)

    # Override
    def is_pressed(self) -> bool:
        """
            Checks if the button is pressed

            Returns:
                bool: True if the button is pressed, False otherwise.
        """
        if self.is_rect_collide_point(pygame.mouse.get_pos()) and InputManager.mouse_is_pressed():
            self.pressed = not self.pressed
            return True
        return False