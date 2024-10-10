import pygame

from managers.input_manager import InputManager
from utils.screen.inputs import Button
from utils.screen.painter import Painter

class CircleButton(Button):
    """
    Represents a clickable circle button with optional text and animation effects.
    """

    def __init__(self, size:int, rect_pos:tuple[int, int], 
                 center:bool=True, topleft:bool=False) -> None:
        """
        Initializes the CircleButton instance.

        Args:
            size (int): The size of the button (diameter).
            rect_pos (tuple[int, int]): The position of the button on the screen.
            center (bool, optional): Whether the button is positioned at the center. Defaults to True.
            topleft (bool, optional): Whether the button is positioned at the top-left corner. Defaults to False.
        """
        super().__init__((size, size), rect_pos, center, topleft)
        self.radius = size
        self.pressed = False

    def draw_button(self, screen:pygame.display, back_color:str='black') -> None:
        """
        Draws the circular button on the screen.

        Args:
            screen (pygame.display): The surface to draw the button on.
            back_color (str, optional): The color of the button when pressed. Defaults to 'black'.
        """
        pygame.draw.circle(screen, 'black', self.rect.center, self.radius, 3)
        if self.pressed:
            pygame.draw.circle(screen, back_color, self.rect.center, int(self.radius/2))

    def draw_text_button(self, screen:pygame.display, text:str, text_color:str,
                        text_back_color:str='black', font_size:int=42, back_color='black'):
        """
        Draws the circular button with text on the screen, including a shadow effect.

        Args:
            screen (pygame.display): The surface to draw the button on.
            text (str): The text to display on the button.
            text_color (str): The color of the text.
            text_back_color (str, optional): The color of the text shadow. Defaults to 'black'.
            font_size (int, optional): The font size of the text. Defaults to 42.
            back_color (str, optional): The background color of the button. Defaults to 'black'.
        """
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