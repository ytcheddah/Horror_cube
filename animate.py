import pygame 
from spritesheet import SpriteSheet
import os

pygame.init() 

# Screen setup
SCREEN_WIDTH = 500 
SCREEN_HEIGHT = 500 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

# Background color
BG = (50, 50, 50)

# Load sprite sheet
sprite_sheet_path =  os.path.join(
    os.path.dirname(__file__),'images', 'MainCharacter', 'MC_Simpleton_SpriteSheet.png'
    )
sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()

# Animation parameters
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
SCALE = 1
FRAME_COUNT = 4

def get_image(sheet, frame, width, height, scale, color):
    """Extracts an image from the sprite sheet."""
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image 

# Prepare animation frames 
frames = [get_image(sprite_sheet_image, i, SPRITE_WIDTH, SPRITE_HEIGHT, SCALE, BG) for i in range(FRAME_COUNT)]

clock = pygame.time.Clock()
frame_index = 0
run = True 

while run:

    # Update background.
    screen.fill(BG)

    # Draw current frame
    screen.blit(frames[frame_index], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Update frame index 
    frame_index = (frame_index + 1) % FRAME_COUNT


    # Event handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
    clock.tick(6)