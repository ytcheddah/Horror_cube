import pygame 
from pygame.sprite import Sprite

class Flare(Sprite):
    """A class that manages flares fired from the player."""
    
    def __init__(self, hc_game):
        """Create a flare object at the player's current position."""
        super().__init__()
        self.screen = hc_game.screen
        self.settings = hc_game.settings 
        self.color = self.settings.flare_color
        self.direction = hc_game.player.direction

        # Create a flare rect at (0, 0) and then set the correct postion.

        self.rect = pygame.Rect(
            0, 0, self.settings.flare_height, self.settings.flare_width)
        # Set flare position based on the direction the player is facing
        if self.direction == "right":
            self.rect.midright = hc_game.player.rect.midright
        elif self.direction == "left":
            self.rect.midleft = hc_game.player.rect.midleft
        elif self.direction == "up":
            self.rect.midtop = hc_game.player.rect.midtop
        elif self.direction == "down":
            self.rect.midbottom = hc_game.player.rect.midbottom
        # Set rect pos for diagonal movement
        elif self.direction == "upright":
            self.rect.topright = hc_game.player.rect.topright
        elif self.direction == "upleft":
            self.rect.topleft = hc_game.player.rect.topleft
        elif self.direction == "downright":
            self.rect.bottomright = hc_game.player.rect.bottomright
        elif self.direction == "downleft":
            self.rect.bottomleft = hc_game.player.rect.bottomleft
        
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the flare on the screen based on direction of player."""
        if self.direction == "right":
            self.x += self.settings.flare_speed
        elif self.direction == "left":
            self.x -= self.settings.flare_speed
        elif self.direction == "up":
            self.y-= self.settings.flare_speed
        elif self.direction == "down":
            self.y += self.settings.flare_speed
        elif self.direction == "upright":
            self.x += self.settings.flare_speed
            self.y -= self.settings.flare_speed
        elif self.direction == "upleft":
            self.x -= self.settings.flare_speed
            self.y -= self.settings.flare_speed
        elif self.direction == "downright":
            self.x += self.settings.flare_speed
            self.y += self.settings.flare_speed
        elif self.direction == "downleft":
            self.x -= self.settings.flare_speed
            self.y += self.settings.flare_speed

        # Update rect position 
        self.rect.x = self.x 
        self.rect.y = self.y
            

    def draw_flare(self):
        """Draw the flare on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
