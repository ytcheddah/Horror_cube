import pygame 

class SpriteSheet():
    """Class that manages sprite sheets."""
    def __init__(self, image): 
        self.sheet = image

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