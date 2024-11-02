import pygame 
from spritesheet import SpriteSheet
import os

pygame.init() 

SCREEN_WIDTH = 500 
SCREEN_HEIGHT = 500 

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Spritesheets')

sprite_sheet_image = pygame.image.load(os.path.join(
    os.path.dirname(__file__),'images', 'MainCharacter', 'MC_Simpleton_SpriteSheet.png')
)
sprite_sheet = SpriteSheet(sprite_sheet_image)

BG = (50, 50, 50)


def get_image(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image 

frame_0 = sprite_sheet.get_image(0, 64, 64, 1.5, 'BLACK')

frame_1 = sprite_sheet.get_image(1, 64, 64, 1.5, 'BLACK')

frame_2 = sprite_sheet.get_image(2, 64, 64, 1.5, 'BLACK')

run = True 

while run:

    # Update background.
    screen.fill(BG)

    # Display image
    screen.blit(frame_0, (0, 0))

    # Event handler 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()