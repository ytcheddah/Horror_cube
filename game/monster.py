import pygame
from game.main import *
from random import randint
from game.settings import *

# Screen display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HC_CLASSES")
clock = pygame.time.Clock()

# # Initialize Enemy Sprites
# angremlin_mon = pygame.image.load("images/_angremlin/angremlin1test.png").convert_alpha()
# thecarne_mon = pygame.image.load("images/anth_sprites/64x64/thecarne1.png").convert_alpha()
# filth_mon = pygame.transform.rotozoom(pygame.image.load("images/anth_sprites/80x80/filth1.png").convert_alpha(), 0, 2)
# louis_mon = pygame.image.load("images/anth_sprites/64x64/louis1.png").convert_alpha()
# squihomie_mon = pygame.transform.rotozoom(pygame.image.load("images/anth_sprites/64x64/squihomie1.png").convert_alpha(), 0, 2)
# umo_mon = pygame.image.load("images/umo_Sprites/roam_chase/umo-rc-09.png").convert_alpha()
# zenba_mon = pygame.image.load("images/zenba_sprites/zenba1.png").convert_alpha()

class Monster(object):

    def __init__(self, name, player, image, x, y, speed, agro_distance, pursue_range, attack_range):
        x = randint(0, SCREEN_WIDTH)
        y = randint(0, SCREEN_HEIGHT)
        self.name = name
        self.player = player
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

        self.rect = self.image.get_rect(center = (x + self.width//2, y + self.width//2))
        self.pos = pygame.math.Vector2(x, y) # position on the screen
        self.coords = pygame.math.Vector2(x, y) # Position relative to the map

        self.mask = pygame.mask.from_surface(self.image)

        self.speed = speed
        self.agro_distance = agro_distance
        self.pursue_range = pursue_range
        self.attack_range = attack_range
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        self.vel_x = 0
        self.vel_y = 0

        self.chase_duration = 4000 # miliseconds
        self.chase_cooldown = 1000 
        self.in_chase_cooldown = False

    def draw(self, screen):

        self.rect.center = (self.pos.x , self.pos.y)
        # Adjusts monster position relative to player's map position
        # pygame.draw.rect(screen, 'pink', self.rect, width=self.width)
        if not self.player.show_mask:
            screen.blit(self.image, self.rect.topleft)
        else:
            screen.blit(self.mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(155,245,120,255)), self.rect.topleft)

    def move(self):
        # Location relative to map
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        self.pos += pygame.math.Vector2(-self.player.velocity_x, -self.player.velocity_y)

        self.coords += pygame.math.Vector2(self.vel_x, self.vel_y)

    def behavior(self):     

        # Check distance between monster and player
        distance_to_player = self.pos.distance_to(self.player.pos)
        # Calculate direction towards player
        direction = (self.player.pos - self.pos).normalize()
        
        if distance_to_player <= self.pursue_range:
            if distance_to_player <= self.agro_distance:
                if distance_to_player > self.attack_range: # also prevents jittering and monst going directly on top of player                
                    # Set velocity towards player
                    self.vel_x = direction.x * self.speed
                    self.vel_y = direction.y * self.speed

                    if distance_to_player <= self.attack_range: # also prevents jittering and monst going directly on top of player
                        self.vel_x = 0
                        self.vel_y = 0

                else: # stops approaching player when within attack range
                    self.vel_x = 0
                    self.vel_y = 0

        else: # stops chasing when outside pursue range
            self.vel_x = 0
            self.vel_y = 0          
        
    def update(self):
        self.behavior()
        self.move()