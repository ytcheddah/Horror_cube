
import pygame
import sys
from settings import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spritesheets")

# 320 x 320 px BUT image only is 280 x 280
sprite_sheet = pygame.image.load("images/MC-SpriteSheet.png").convert_alpha()
sprite_sheet_image = pygame.transform.rotozoom(sprite_sheet, 0, 0.2)


BG = (100, 100, 100)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def get_image(sheet, frame, width, height, scale, color):

    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image

frame_0 = get_image(sprite_sheet_image, 0, 64, 64, 1, GREEN)
frame_1 = get_image(sprite_sheet_image, 1, 64, 64, 1, GREEN)
frame_2 = get_image(sprite_sheet_image, 2, 64, 64, 1, GREEN)
frame_3 = get_image(sprite_sheet_image, 3, 64, 64, 1, GREEN)



run = True
while run:

    # update background
    screen.fill(BG)

    # show frame image
    screen.blit(frame_0, (0, 0))
    screen.blit(frame_1, (70, 0))
    screen.blit(frame_2, (140, 0))
    screen.blit(frame_3, (210, 0))

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    pygame.display.update()

pygame.quit()

