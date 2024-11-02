import sys
import pygame 
from SettingsClass import Settings
from player import Player 
import os

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

        pygame.display.set_caption("Horror Cube")

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()
            self._update_screen()
            self.player.update()

            # Make the most recently drawn screen visible 
            pygame.display.flip()
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
            if event.key == pygame.K_RIGHT:
                self.player.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.player.moving_left = True
            elif event.key == pygame.K_UP:
                self.player.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.player.moving_down = True

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

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.player.blitplayer()
    

image_path = os.path.join(os.path.dirname(__file__), 'images', 'MainCharacter', 'MC_Simpleton_SpritSheet.png')
print("Image path:", image_path)  # Debug line


if __name__ == "__main__":
    hc = HorrorCube()
    hc.run_game()
        