
import pygame
from sys import exit
import math
from settings import *


pygame.init()

# Creating the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Horror Cube")
clock = pygame.time.Clock()

# Loads Images

background = pygame.transform.scale(pygame.image.load("images/test-image2.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):

    def __init__(self):
        #this below calls the parent class' constructor, which is the sprite class
        super().__init__()

        self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0, 2)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED
        

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()


        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed

        if self.velocity_x != 0 and self.velocity_y != 0: # moving diagonally
                self.velocity_x /= math.sqrt(2)
                self.velocity_y /= math.sqrt(2)

    def move(self):

        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def update(self):

        self.user_input()
        self.move()


player = Player()
    

while True:

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            player.user_input()
    
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.pos)
    player.update()

    pygame.display.update()
    clock.tick(FPS)

