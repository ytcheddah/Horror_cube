import pygame

# Initialize fonts
pygame.font.init()

# Load fonts
menu_font = pygame.font.Font("font/boldPixelFont.ttf", 74)
p_font = pygame.font.Font("font/pixelFont.ttf", 36)
pos_font = pygame.font.Font("font/pixelFont.ttf", 18)
speed_font = pygame.font.Font("font/pixelFont.ttf", 18)
xy_font = pygame.font.Font("font/pixelFont.ttf", 14)
monster_font = pygame.font.Font("font/pixelFont.ttf", 14)

# Dictionary of fonts for better organizatioin
fonts = {
    "menu_font": menu_font,
    "p_font": p_font,
    "pos_font": pos_font,
    "speed_font": speed_font,
    "xy_font": xy_font,
    "monster_font": monster_font,
}
