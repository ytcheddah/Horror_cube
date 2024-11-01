import pygame 

from player import Player 

class HorrorCube:
    """Overall game class to manage the game assets and behavior."""

    def __init__(self):
        """Initialize the attributes of HorrorCube."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = 