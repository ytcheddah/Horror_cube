import pygame 

import os

class Player:
    """A class that manages the player character"""

    def __init__(self, hc_game):
        """Initialize the player class and sets its starting position"""
        self.screen = hc_game.screen 
        self.screen_rect = hc_game.screen.get_rect()

        # Load the player image
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(__file__),'images', 'MainCharacter', 'MC_Simpleton_SpritSheet.png'))
        self.rect = self.image.get_rect()

        # Spawn the character in the middle of the screen 
        self.rect.center = self.screen_rect.center 

    def blitplayer(self):
        """Draw the player at it's current location"""
        self.screen.blit(self.image, self.rect)


