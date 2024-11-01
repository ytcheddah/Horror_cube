import pygame
from settings import *
pygame.init()

# Screen display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
percentage = 100
percentage_decay = (100 / 10_800)

class UserInterface:
    """
    A parent class which provides a framework for all classes 
    displayed on the user interface.
    """

    def __init__(self, x, y):
        """
        Initializes the attributes of the user interface. Where 
        things will be displayed, and the size of the item on the
        screen.
        """
        self.x = x
        self.y = y


        # width = image.get_width()
        # height = image.get_height()
        # self.image = pygame.transform.scale(image,(int(width * scale), (int(height * scale))))
        # self.rect = self.image.get_rect()
        # self.rect.topleft = (x, y)
    
    def draw(self, location, size):
        """Draws the item location and size."""

class PsycheBar(UserInterface):
    """Subclass of UserInterface simulating the psyche of the player."""
    def __init__(self, x, y, color):
        """Initialize the attributes of the psyche bar."""
        super().__init__(x, y)
        self.percentage = 100
        self.color = color
        
    def draw(self, percentage):
        """Draws the psyche bar and the base decay rate."""

        pygame.draw.rect(screen, BLACK, (BAR_X, BAR_Y, BAR_OUTLINE_WIDTH, BAR_OUTLINE_HEIGHT))

        inner_bar_width = int(BAR_WIDTH *(percentage / 100))
        
        pygame.draw.rect(screen, self.color, ((BAR_X + 6), (BAR_Y + 5), inner_bar_width, BAR_HEIGHT))

     # determine the color of the bar based on the percentage
        if percentage > 67:
            self.color = GREEN
        elif 33 <= percentage <= 67:
            self.color = YELLOW
        else:
            self.color = RED

    def update(self):
        percentage -= percentage_decay
        

class HealthBar(UserInterface):
    def __init__(self, x, y, image, scale):
        """Initialize the attributes of the player's health"""
        super.__init__(x, y, image, scale)

    def adjust_health(self, percentage):
        """
        Defines a function which adjusts the health bar by given increments.
        """

    def death(self):
        """Defines a function simulating the death of the player."""

class HotMenu(UserInterface):
    def __init__(self, x, y, image, scale):
        """Initialize the attributes of an interactable menu while playing."""
        super.__init__(x, y, image, scale)

    def cycle_menu(self):
        """
        Defines a function for cycling left and right through items in
        the player's hotbar.
        """
    
    def use_item(self):
        """
        Defines a function which uses the selected item in the player's
        hotbar.
        """
# class Button(UserInterface):

#     def __init__(self, x, y, image, scale):
#         """Initialize the button"""
#         super.__init__(x, y, image, scale)
#         width = image.get_width()
#         height = image.get_height()
#         self.image = pygame.transform.scale(image,(int(width * scale), (int(height * scale))))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.clicked = False

#     def draw(self, screen):
#         # draw button on screen
#         screen.blit(self.image, (self.rect.x, self.rect.y))
    
#     def update(self):
#         action = False
#         # get mouse position
#         pos = pygame.mouse.get_pos()

#         # check mouseover and clicked conditions
#         if self.rect.collidepoint(pos):
#             if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # the list 0-2 is leftmouse, centermouse, rightmouse button
#                 self.clicked = True
#                 # print('CLICKED') # debug checker (already works tho)
#                 action = True
#         if pygame.mouse.get_pressed()[0] == 0:
#             self.clicked = False

#         return action
