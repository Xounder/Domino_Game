import pygame

from managers.input_manager import InputManager
from utils.painter.inputs.click_input import ClickInput
from utils.painter.painter import Painter

class ClickCircle(ClickInput):
    """
    Represents a clickable circle with optional animation effects.
    """

    def __init__(self, size:int, rect_pos:tuple[2], colors:list[2], center:bool=True, topleft:bool=False) -> None:
        """
        Initializes the clickable circle with given dimensions and position.
        
        Args:
            surf_size (tuple): The size of the rectangle surface.
            rect_pos (tuple): The position to draw the rectangle.
            d (int): The distance for border thickness.
            r (int): The radius for circle effects.
            center (bool): If True, position the rectangle centered at rect_pos.
            topleft (bool): If True, position the rectangle at the top-left of rect_pos.
        """
        super().__init__((size, size), rect_pos, center, topleft)
        self.colors = colors
        self.radius = size
        self.pressed = False

    def draw_animated_circle(self, screen:pygame.display, back_color:str='black') -> None:
        """
        Draws animated circles with specified colors at the rectangle's center.
        
        Args:
            screen (pygame.display): The surface to draw on.
            colors (list): A list of colors for the circles.
            back_color (str): The center color if not pressed
        """
        color = self.colors[1] if self.pressed else back_color
        pygame.draw.circle(screen, self.colors[0], self.rect.center, self.radius, 3)
        pygame.draw.circle(screen, color, self.rect.center, int(self.radius/2))

    def draw_animated_circle_with_text(self, 
                                       screen:pygame.display,
                                       text:str,
                                       text_color:str,
                                       text_back_color:str='black',
                                       font_size:int=42,
                                       back_color='black'):
        """
        Draws animated circles with specified colors at the rectangle's center with text inside
        
        Args:
            screen (pygame.display): The surface to draw on.
            colors (list): A list of colors for the circles.
            back_color (str): The center color if not pressed
        """
        gap = [self.radius/2 + 5, font_size/3]
        pos = (self.rect.right + gap[0], self.rect.centery - gap[1])

        self.draw_animated_circle(screen, back_color=back_color)
        Painter.blit_text_shadow(screen, text, text_color, pos, back_color=text_back_color, font_size=font_size)

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