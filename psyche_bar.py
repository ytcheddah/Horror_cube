import pygame 

class PsycheBar:
    """Models a psyche bar of the player character."""

    def __init__(self, hc_game):
        """Initialize attributes of the psyche bar."""
        self.screen = hc_game.screen
        self.settings = hc_game.settings 
        self.color = 'GREEN'
        self.percentage = self.settings.percentage


    def draw_psyche_bar(self, percentage):
        """Draws the psyche bar on the screen and updates the size and color."""
        
        # Calculate dynamic width of the inner bar based on current percentage
        self.bar_width = float(self.settings.bar_width * percentage / 100)

        # Rectangle for the outer bar
        self.outer_rect = pygame.Rect(
            0, 0, self.settings.outer_bar_width, self.settings.outer_bar_height)
        # Rectangle for the inner bar
        self.inner_rect = pygame.Rect(
            0, 0, self.bar_width, self.settings.bar_height)

        # Position of the bar
        self.outer_rect.center, self.inner_rect.center = (
            self.settings.bar_x, self.settings.bar_y), (self.settings.bar_x, self.settings.bar_y)
        
        # Color logic
        if percentage > 67:
            self.color = 'GREEN'
        elif 33 <= percentage <= 67:
            self.color = 'YELLOW'
        else:
            self.color = 'RED'

        if percentage == 0:
            self.bar_width = 0
        
        pygame.draw.rect(self.screen, 'BLACK', self.outer_rect)
        pygame.draw.rect(self.screen, self.color, self.inner_rect)

    def update(self):
        self.settings.percentage = max(0, self.settings.percentage - self.settings.percentage_decay)
