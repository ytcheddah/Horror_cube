import sys
import os
import pygame 
from SettingsClass import Settings
from player import Player 
from flare_gun import Flare

class HorrorCube:
    """Overall game class to manage the game assets and behavior."""

    def __init__(self):
        """Initialize the attributes of HorrorCube."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.player = Player(self)
        self.flares = pygame.sprite.Group()

        pygame.display.set_caption("Horror Cube")

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()
            self.player.update()
            self._update_flares()

            # Make the most recently drawn screen visible 
            pygame.display.flip()
            self._update_screen()
            self.clock.tick(60)
            

    def _check_events(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)

    def _check_keydown_event(self, event):
        """Responds to keypresses."""

        # Key presses to move the player with Boolean flags.
        if event.type == pygame.KEYDOWN:
           
            # Player movement
            if event.key == pygame.K_RIGHT:
                self.player.moving_right = True
                self.player.direction = 'right'
            elif event.key == pygame.K_LEFT:
                self.player.moving_left = True
                self.player.direction = 'left'
            elif event.key == pygame.K_UP:
                self.player.moving_up = True
                self.player.direction = 'up'
            elif event.key == pygame.K_DOWN:
                self.player.moving_down = True
                self.player.direction = 'down'
            # Shoot flare.
            elif event.key == pygame.K_SPACE:
                self._shoot_flare()
            # Exit
            elif event.key == pygame.K_q:
                sys.exit()
            
    def _check_keyup_event(self, event):
        """Responds to key releases."""

        # Key releases to move the player with Boolean flags.
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.player.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.player.moving_left = False
            elif event.key == pygame.K_UP:
                self.player.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.player.moving_down = False
            
    def _update_flares(self):
        """Update position of flares and remove old ones"""
        self.flares.update()
        
    def _shoot_flare(self):
        new_flare = Flare(self)
        self.flares.add(new_flare)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for flare in self.flares.sprites():
            flare.draw_flare()
        self.player.blitplayer()   

    

# image_path = os.path.join(os.path.dirname(__file__), 'images', 'MainCharacter', 'MC_Simpleton_SpritSheet.png')
# print("Image path:", image_path)  # Debug line


if __name__ == "__main__":
    hc = HorrorCube()
    hc.run_game()
        