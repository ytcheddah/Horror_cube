import sys
import os
import pygame 
from SettingsClass import Settings
from player import Player
from actions import Action, EscapeAction, MovementAction
from input_handlers import EventHandler
from flare_gun import Flare
from psyche_bar import PsycheBar

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
        self.psyche_bar = PsycheBar(self)
        self.flares = pygame.sprite.Group()

        pygame.display.set_caption("Horror Cube")

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            self._check_events()
            self.player.update()
            self._update_flares()
            self.psyche_bar.draw_psyche_bar(self.settings.percentage)
            if self.settings.percentage > 0:
                self.psyche_bar.update()
            if self.settings.percentage < 0:
                self.settings.percentage = 0

            # Make the most recently drawn screen visible 
            pygame.display.flip()
            self._update_screen()
            self.clock.tick(60)
            print(self.player.velocity_x, self.player.velocity_y, self.player.moving_down)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        event_handler = EventHandler()
        for event in pygame.event.get():

            action = event_handler.handle_events 
            if action is None:
                continue

            if isinstance(action, MovementAction):
                player_x += action.dx
                player_y += action.dy

            elif isinstance(action, EscapeAction):
                raise SystemExit
            
            # if event.type == pygame.QUIT:
            #     sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            self._check_multiple()

    def _check_multiple(self):
        """Responds to simultaneous inputs."""
        
        # Two or four inputs
        if self.player.moving_right and self.player.moving_up:
            self.player.direction = 'upright'
        elif self.player.moving_right and self.player.moving_down:
            self.player.direction = 'downright'
        elif self.player.moving_left and self.player.moving_up:
            self.player.direction = 'upleft'
        elif self.player.moving_left and self.player.moving_down:
            self.player.direction = 'downleft'
        elif self.player.moving_right and self.player.moving_left or self.player.moving_up and self.player.moving_down:
            self.player.direction = None

        # Special cases for three simultaneous inputs.
        if self.player.direction == 'upright' and self.player.moving_left:
            self.player.direction = 'up'
        elif self.player.direction == 'downright' and self.player.moving_left:
            self.player.direction = 'down'
        elif self.player.direction == 'upleft' and self.player.moving_down:
            self.player.direction = 'left'
        elif self.player.direction == 'upright' and self.player.moving_down:
            self.player.direction = 'right'
        
    def _check_keydown_event(self, event):
        """Responds to keypresses."""

        # Key presses to move the player with Boolean flags.
        if event.type == pygame.KEYDOWN:
           
            # Player movement
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                action = MovementAction(dx=self.settings.player_speed, dy=0)
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                action = MovementAction(dx=-self.settings.player_speed, dy =0)
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                action = MovementAction(dx=0, dy=self.settings.player_speed)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                action = MovementAction(dx=0, dy=self.settings.player_speed)
            # Shoot flare.
            elif event.key == pygame.K_SPACE:
                self._shoot_flare()
            elif event.key == pygame.K_q:
                print('cycle left')
            elif event.key == pygame.K_e:
                print('cycle right')
            # Exit
            elif event.key == pygame.K_ESCAPE:
                sys.exit()
            
    def _check_keyup_event(self, event):
        """Responds to key releases."""

        # Key releases to move the player with Boolean flags.
        if event.type == pygame.KEYUP:
            # R, L, U, D movement
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.player.moving_right = False
                if self.player.direction == 'upright':
                    self.player.direction = 'up'
                elif self.player.direction == 'downright':
                    self.player.direction = 'down'
                # When the player presses both L and R directional keys
                elif self.player.direction == None:
                    self.player.direction = 'left'
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.player.moving_left = False
                if self.player.direction == 'upleft':
                    self.player.direction = 'up'
                elif self.player.direction == 'downleft':
                    self.player.direction = 'down' 
                # When the player presses both L and R directional keys
                elif self.player.direction == None:
                    self.player.direction = 'right'
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.player.moving_up = False
                if self.player.direction == 'upright':
                    self.player.direction = 'right'
                elif self.player.direction == 'upleft':
                    self.player.direction = 'left' 
                # When the player presses both U and D directional keys
                elif self.player.direction == None:
                    self.player.direction = 'down'
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.player.moving_down = False
                if self.player.direction == 'downright':
                    self.player.direction = 'right'
                elif self.player.direction == 'downleft':
                    self.player.direction = 'left' 
                # When the player presses both U and D directional keys
                elif self.player.direction == None:
                    self.player.direction = 'up'
                 
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

if __name__ == "__alpha__":
    hc = HorrorCube()
    hc.run_game()
        