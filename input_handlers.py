import pygame 
from typing import Optional
from actions import Action, EscapeAction, MovementAction


class EventHandler:
    """Class which handles events in the game loop."""
    
    def handle_events(self) -> Optional[Action]:
        """Processes events from Pygame's event queue."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit()
            
            elif event.type == pygame.KEYDOWN:
                return self.handle_keydown(event)
            
    def handle_keydown(self, event) -> Optional[Action]:
        """Handles key press events."""
        action: Optional[Action] = None
        key = event.key

        if key == pygame.K_RIGHT or event.key == pygame.K_d:
            action = MovementAction(dx=self.settings.player_speed, dy=0)
        elif key == pygame.K_LEFT or event.key == pygame.K_a:
            action = MovementAction(dx=-self.settings.player_speed, dy =0)
        elif key == pygame.K_UP or event.key == pygame.K_w:
            action = MovementAction(dx=0, dy=self.settings.player_speed)
        elif key == pygame.K_DOWN or event.key == pygame.K_s:
            action = MovementAction(dx=0, dy=self.settings.player_speed)
       
        elif key == pygame.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action 
    
    