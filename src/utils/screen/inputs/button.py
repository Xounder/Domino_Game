import pygame

from managers.input_manager import InputManager

class Button:
    """
    Represents a clickable
    """

    def __init__(self, surf_size:tuple[int, int], rect_pos:tuple[int, int], 
                 center:bool=True, topleft:bool=False) -> None:
        """
        Initializes the clickable with given dimensions and position.
        
        Args:
            surf_size (tuple[int, int]): The size of the rectangle surface.
            rect_pos (tuple): The position to draw the rectangle.
            center (bool): If True, position the rectangle centered at rect_pos.
            topleft (bool): If True, position the rectangle at the top-left of rect_pos.
        """
        self.surf = pygame.Surface(surf_size)
        if center:
            self.rect = self.surf.get_rect(center=rect_pos)
        if topleft:
            self.rect = self.surf.get_rect(topleft=rect_pos)

    def get_rect(self, center:bool=False, topleft:bool=False, 
                 size:bool=False, midright:bool=False) -> pygame.Rect:
        """
        Returns the rectangle's position or size based on specified flags.
        
        Args:
            center (bool): If True, return the center of the rectangle.
            topleft (bool): If True, return the top-left position of the rectangle.
            size (bool): If True, return the size of the rectangle.
            midright (bool): If True, return the mid-right position of the rectangle.
        
        Returns:
            pygame.Rect: The rectangle's position or size based on flags.
        """
        if center: return self.rect.center
        if topleft: return self.rect.topleft
        if size: return self.rect.size
        if midright: return self.rect.midright
        return self.rect
    
    def set_rect(self, pos:tuple[int, int], center=True, topleft=False):
        if center: self.rect.center = pos
        if topleft: self.rect.topleft = pos

    def is_rect_collide_point(self, point:tuple[int, int]) -> bool:
        """
        Checks if the given point collides with the rectangle.
        
        Args:
            point (tuple[int, int]): The point to check for collision.
        
        Returns:
            bool: True if the point collides with the rectangle, False otherwise.
        """
        return self.rect.collidepoint(point)
    
    def is_pressed(self) -> bool:
        """
            Checks if the button is pressed

            Returns:
                bool: True if the button is pressed, False otherwise.
        """
        return self.is_rect_collide_point(pygame.mouse.get_pos()) and InputManager.mouse_is_pressed()
