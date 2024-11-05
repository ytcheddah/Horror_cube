import pygame

class Character(pygame.sprite.Sprite):
    """A parent class which manages character in game."""
    def __init__(self, sprite_sheet_path, width, height, scale, color, frames):
        """Initialize the attributes of the character class."""
        super().__init__()
        self.sprite_sheet = SpriteSheet(sprite_sheet_path)
        self.frames = [self.sprite_sheet.getimage(i, width, height, scale, color) for i in range(frames)]
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
    
    def update(self):
        """Update the character's animation and position."""
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.image = self.frames[self.frame_index]

         