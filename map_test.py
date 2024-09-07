import pygame, sys
from settings import *
from pytmx.util_pygame import load_pygame



pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
tmx_data = load_pygame("map_test.tmx")

