import pygame
import math
import sys
from settings import *


# --- Put all classes in this file and then import them into the other files to improve readability ---

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSE = "pause"

# Initializa Monster variables and dictionaries

AGRO_TYPES = {1: "Sight", 2: "Sound", 3: "Proximity"}
MONSTER_IMAGES = []
x = "iamges/umo_Sprites/roam_chase/umo-rc-9.png"

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0, 2)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED
        self.velocity_x = 0
        self.velocity_y = 0

    def user_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        self.velocity_y = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed

        if self.velocity_x != 0 and self.velocity_y != 0:  # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if keys[pygame.K_ESCAPE]:
            global game_state
            game_state = PAUSE

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def update(self):
        self.user_input()
        self.move()

class Monster(pygame.sprite.Sprite):

    def __init__(self, name, image, pos_x, pos_y, health, attack, speed, agro_type, agro_ratio, agro_distance):
        super().__init__()
        self.name = name
        self.image = image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.health = health
        self.attack = attack
        self.speed = speed
        self.agro_type = agro_type
        self.agro_ratio = agro_ratio
        self.agro_distance = agro_distance
        self.velocity_x = 0
        self.velocity_y = 0

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def behavior(self, Player):
        pass
        """ if Player.pos.x > Monster.pos.x:
                Monster.velocity_x += speed
            if Player.pos.x < Monster.pos,x:
                Monster.velocity_x -= speed"""

    def update(self):
        self.behavior()
        self.move()

player = Player()
umo = Monster("Umo", x, 50, 50, 100, 10, 5, AGRO_TYPES[1-3], 1, 200)