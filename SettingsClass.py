class Settings:
    """Class to manage variable user settings"""
    def __init__(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (0, 0, 0)

        # Player settings 
        self.player_speed = 5

        # Flare settings 
        self.flare_color = (230, 5, 15)
        self.flare_width = 6 
        self.flare_height = 6
        self.flare_speed = 8
