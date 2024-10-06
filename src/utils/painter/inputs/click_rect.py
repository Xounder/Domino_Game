import pygame

from utils.painter.inputs.click_input import ClickInput
from utils.painter.painter import Painter

class ClickRect(ClickInput):
    """
    Represents a clickable rectangle with optional animation effects.
    """

    def __init__(self, surf_size:tuple, rect_pos:tuple, dist:int=0, center:bool=True, topleft:bool=False) -> None:
        """
        Initializes the clickable rectangle with given dimensions and position.
        
        Args:
            surf_size (tuple): The size of the rectangle surface.
            rect_pos (tuple): The position to draw the rectangle.
            dist (int): The distance for border thickness.
            center (bool): If True, position the rectangle centered at rect_pos.
            topleft (bool): If True, position the rectangle at the top-left of rect_pos.
        """
        super().__init__(surf_size, rect_pos, center, topleft)
        self.dist = dist

    def draw_animated_rect(self, screen:pygame.display, f_color:str='black', b_color:list=['red', 'gray']) -> None:
        """
        Draws an animated rectangle with color changes based on mouse hover.
        
        Args:
            screen (pygame.display): The surface to draw on.
            f_color (str): The fill color of the rectangle.
            b_color (list): The background colors for hover effects.
        """
        b_c = b_color[0] if self.is_rect_collide_point(pygame.mouse.get_pos()) else b_color[1]
        Painter.draw_rect(screen, self.rect.size, self.rect.topleft, self.dist, f_color=f_color, b_color=b_c)

    def draw_animated_rect_with_text(self, 
                                     screen:pygame.display,
                                     text:str,
                                     text_color:str,
                                     font_size:int,
                                     text_back_color:str='black', 
                                     f_color:str='black', 
                                     b_color:list=['red', 'gray']) -> None:
        
        self.draw_animated_rect(screen, f_color, b_color)
        Painter.blit_text_shadow(screen, text, text_color, self.rect.center, 
                                 font_size=font_size, center=True, back_color=text_back_color)
