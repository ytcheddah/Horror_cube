class Settings:
    """Class to manage variable user settings"""
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = 'WHITE'
        self.frame_rate = 60

        # Player settings 
        self.player_speed = 5

        # Flare settings 
        self.flare_color = (230, 5, 15)
        self.flare_width = 6 
        self.flare_height = 6
        self.flare_speed = 8

        # Mood meter settings 
        self.outer_bar_width = 500
        self.outer_bar_height = 25
        self.bar_width = 488
        self.bar_height = 15
        self.percentage_decay = (1000 / 10800) 
        self.percentage = 100
        self.bar_x = self.screen_width // 2 
        self.bar_y = self.screen_height - 35
