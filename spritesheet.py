import pygame 

class SpriteSheet():
    """Class that manages sprite sheets."""
    def __init__(self, image_path, frame_width, frame_height): 
        """Initialize the sprite sheet class.
        
        Args:
            image_path (str): Path to the sprite sheet image.
            frame_width (int): Width of each frame in the sprite sheet.
            frame_height (int): Height of each frame in the sprite sheet.
            """
        # Load the sprite sheet image
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Store the dimensions of each frame
        self.frame_width = frame_width
        self.frame_height = frame_height

        # Determine the number of frames in the sprite sheet 
        self.sheet_width, self.sheet_height = self.sprite_sheet.get_size()
        self.columns = self.sheet_width // frame_width
        self.rows = self.sheet_height // frame_height
        self.total_frames = self.columns * self.rows

        # Store frames 
        self.frames = []
        self._load_frames()

        # Animation index and speed 
        self.current_frame_index = 0
        self.animation_speed = 0.1
        self.last_update_time = 0
    
    def _load_frames(self):
        """Extracts each frame from the sprite sheet and stores them in a list."""
        for row in range(self.rows):
            for col in range(self.columns):
                # Calculate the position of the frame 
                x = col * self.frame_width
                y = row * self.frame_height
                # Extract and store the frame 
                frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
                self.frames.append(frame)

    def get_image(self, frame, width, height, scale, color):
        """Extracts a frame from the sprite"""
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image 

    def animate_image(self, image):
        for frame in image:
            self.screen.blit(frame)