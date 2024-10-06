import pygame

class Painter:
    """
    Provides static methods for drawing text and rectangles on the screen.
    """

    @staticmethod
    def blit_text(screen:pygame.display, text:str, color:str, pos:tuple[int,int], 
                  topright:bool=False, center:bool=False, font_size:int=42) -> None:
        """
        Renders and blits text onto the screen at the specified position.
        
        Args:
            screen (pygame.display): The surface to draw on.
            text (str): The text to render.
            color (str): The color of the text.
            pos (list): The position to place the text.
            topright (bool): If True, position text at the top right corner.
            center (bool): If True, center the text at the given position.
            font_size (int): The font size for the text.
        """
        font = pygame.font.Font('font/Pixeltype.ttf', font_size)
        txt = font.render(text, False, color)

        if topright: txt_rect = txt.get_rect(topright= pos)
        elif center: txt_rect = txt.get_rect(center= pos)
        else: txt_rect = txt.get_rect(topleft= pos)       

        screen.blit(txt, txt_rect)

    @staticmethod
    def blit_text_shadow(screen:pygame.display, text:str, color:str, pos:tuple[int,int], back_color:str='black', 
                         topright:bool=False, center:bool=False, font_size:int=42) -> None:
        """
        Renders and blits text with a shadow effect on the screen.
        
        Args:
            screen (pygame.display): The surface to draw on.
            text (str): The text to render.
            color (str): The color of the text.
            pos (list): The position to place the text.
            back_color (str): The color of the shadow.
            topright (bool): If True, position text at the top right corner.
            center (bool): If True, center the text at the given position.
            font_size (int): The font size for the text.
        """
        Painter.blit_text(screen, text, back_color, [pos[0] + 2, pos[1] + 2], topright, center, font_size)
        Painter.blit_text(screen, text, color, pos, topright, center, font_size)

    @staticmethod
    def draw_rect(screen:pygame.display, size:tuple[int,int], pos:tuple[int,int], d:int, 
                  f_color:str='black', b_color:str='white') -> None:
        """
        Draws a filled rectangle with a border on the screen.
        
        Args:
            screen (pygame.display): The surface to draw on.
            size (list): The size of the rectangle.
            pos (list): The position to draw the rectangle.
            d (int): The border thickness.
            f_color (str): The fill color of the rectangle.
            b_color (str): The border color of the rectangle.
        """
        pygame.draw.rect(screen, f_color, (pos[0], pos[1], size[0], size[1]), 0)
        pygame.draw.rect(screen, b_color, (pos[0] + d , pos[1]+ d, size[0] - d*2 , size[1] - d*2), 0)


