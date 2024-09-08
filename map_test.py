import pygame, sys
from settings import *
from pytmx.util_pygame import load_pygame



pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_data = load_pygame("map/main_map.tmx")

object_layer = tmx_data.get_layer_by_name('bushes')
for obj in object_layer:
    print(obj)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    pygame.display.update()