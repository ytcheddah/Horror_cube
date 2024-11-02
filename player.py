import pygame 
import math
import os

class Character:
    """A parent class which manages character in game."""
    def __init__(self):
        """Initialize the attributes of the character class."""

    def animate(self, spritesheet):
        """A function which takes any spritesheet and animates it."""
         



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
        self.velocity_x = 0 
        self.velocity_y = 0

        # Load player settings 
        self.settings = hc_game.settings

        # Boolean flags for movement
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

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
            self.velocity_x = self.settings.player_speed
            self.x += self.settings.player_speed
        if self.moving_left and self.rect.left > 0:
            self.velocity_x = -self.settings.player_speed
            self.x -= self.settings.player_speed
        if self.moving_up and self.rect.top > 0:
            self.velocity_y = self.settings.player_speed
            self.y -= self.settings.player_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.velocity_y = -self.settings.player_speed
            self.y += self.settings.player_speed
        
        # Diagonal movement 
        if self.velocity_x != 0 and self.velocity_y != 0:
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)


        # Update the rect object
        self.rect.x = self.x
        self.rect.y = self.y

    def blitplayer(self):
        """Draw the player at it's current location"""
        self.screen.blit(self.image, self.rect)
