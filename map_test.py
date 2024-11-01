import pygame, sys
from settings import *
from pytmx.util_pygame import load_pygame

#class for the tiles in the map
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_data = load_pygame("map/main_map.tmx")
dsprite_group = pygame.sprite.Group() # group for the map

# cycle through all layers
# all tiles are looped here. no objects are looped in this for loop
for layer in tmx_data.visible_layers: # seperate tile layers from object groups
    # if layer.name in ('floor') # selects specific layers. 
    if hasattr(layer, 'data'): # if has the attribute 'layer'
        for x, y, surf in layer.tiles():
            pos = (x * 32, y * 32)
            Tile(pos = pos, surf = surf, groups = dsprite_group)

# this for loop will include all objects
for obj in tmx_data.objects:
    pos = obj.x, obj.y
    if obj.type in ('vegetation'):
        Tile(pos, surf = obj.image, groups = dsprite_group)

# object_layer = tmx_data.get_layer_by_name('bushes')
# for obj in object_layer:
#     print(obj)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    dsprite_group.draw(screen) # calling the group here
    pygame.display.update()