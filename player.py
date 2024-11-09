import pygame 
import math
import os
from character import Character

class Player(Character):
    """A class that manages the player character"""

    def __init__(self, hc_game):
        """Initialize the player class and sets its starting position"""
        self.screen = hc_game.screen
        self.screen_rect = hc_game.screen.get_rect()

        # Load the player image and its rect
        self.image = pygame.image.load(
            os.path.join(
                os.path.dirname(__file__),'images', 'MainCharacter', 'MC_Simpleton_SpriteSheet.png')
                )
        self.rect = self.image.get_rect()

        # Load player velocity 
        self.dx = 0 
        self.dy = 0

        # Load player settings 
        self.settings = hc_game.settings

        # Boolean flags for movement
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.moving_upright = False
        self.moving_downright = False
        self.moving_upleft = False
        self.moving_downleft = False

        # Bookean flags for direction player is facing
        self.direction = 'down'

        # Spawn the character in the middle of the screen 
        self.rect.center = self.screen_rect.center 

        # Store floats for the player's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.coords = pygame.math.Vector2(self.rect.center) # player relative to map
        self.pos = pygame.math.Vector2(self.screen_rect.center) # player relative to screen (always centered)

    def update(self):
        """Update the player's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.dx = self.settings.player_speed
            self.x += self.dx
        if self.moving_left and self.rect.left > 0:
            self.dx = self.settings.player_speed
            self.x -= self.dx
        if self.moving_up and self.rect.top > 0:
            self.dy = self.settings.player_speed
            self.y -= self.dy
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.dy = self.settings.player_speed
            self.y += self.dy

        # Diagonal movement 
        if self.dx != 0 and self.dy != 0:
            self.dx /= math.sqrt(2)
            self.dy /= math.sqrt(2)

        # Update the rect object
        self.rect.x = self.x
        self.rect.y = self.y

    def blitplayer(self):
        """Draw the player at it's current location"""
        self.screen.blit(self.image, self.rect)
