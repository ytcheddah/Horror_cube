import pygame
import math
import random
import sys
from random import randint
from settings import *
from cl_button import *
from cl_monster import *
from cl_player import *
from cl_trap import *

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSE = "pause"

game_state = PLAYING

# Screen display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("HC_CLASSES")
clock = pygame.time.Clock()

# Fonts
menu_font = pygame.font.Font("font/boldPixelFont.ttf", 74)
p_font = pygame.font.Font("font/pixelFont.ttf", 36)
pos_font = pygame.font.Font("font/pixelFont.ttf", 18)
speed_font = pygame.font.Font("font/pixelFont.ttf", 18)
xy_font = pygame.font.Font("font/pixelFont.ttf", 14)
monster_font = pygame.font.Font("font/pixelFont.ttf", 14)

# initialize Menu music 
pygame.mixer.music.load('sound/Cube_Hell_menu_music.mp3')
pygame.mixer.music.set_volume(DEFAULT_MUSIC_VOLUME)

# Menu items
menu_items = ['Start Game','Options','Exit']
selected_item = 0

# Pause Menu Items
pause_menu_items = ['Resume','Inventory','Options','Save Game','Return to Main Menu']
pause_selected_item = 0

# Initialize and Load Images
bg = pygame.transform.scale(pygame.image.load("images/desert_map.png").convert(), (4000, 2000))
background = pygame.transform.scale(pygame.image.load("images/test-image2.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

# Initialize Enemy Sprites
angremlin_mon = pygame.image.load("images/_angremlin/angremlin1test.png").convert_alpha()
thecarne_mon = pygame.image.load("images/anth_sprites/64x64/thecarne1.png").convert_alpha()
filth_mon = pygame.transform.rotozoom(pygame.image.load("images/anth_sprites/80x80/filth1.png").convert_alpha(), 0, 2)
louis_mon = pygame.image.load("images/anth_sprites/64x64/louis1.png").convert_alpha()
squihomie_mon = pygame.transform.rotozoom(pygame.image.load("images/anth_sprites/64x64/squihomie1.png").convert_alpha(), 0, 2)
umo_mon = pygame.image.load("images/umo_Sprites/roam_chase/umo-rc-09.png").convert_alpha()
zenba_mon = pygame.image.load("images/zenba_sprites/zenba1.png").convert_alpha()

monster_list = [angremlin_mon, thecarne_mon, filth_mon, louis_mon, squihomie_mon, umo_mon, zenba_mon]

# Initialize Player Sprites
walkRight = [pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-00.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-01.png').convert_alpha(), 0, 2),
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-02.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-03.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-04.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-05.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-06.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-07.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-08.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-09.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-10.png').convert_alpha(), 0, 2), 
             pygame.transform.rotozoom(pygame.image.load('images/umo_Sprites/roam_chase/umo-rc-11.png').convert_alpha(), 0, 2)]
left = False
right = False
walkCount = 0
sprint_factor = 1
crouch_factor = 1

# Trap initialization
spike_trap1 = pygame.image.load('images/anth_sprites/64x64/spiketrap1.png').convert_alpha()

trap_list = [spike_trap1]

# Button initialization
spawn_button = pygame.image.load('images/spawn_button1.png').convert_alpha()

# Object Initialization
game_objects = []

class BaseGame:

    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.player = Player()
        self.button = Button()

        self.monsters = []
        self.game_objects = [self.player] + self.monsters

        # Fonts and other resources
        self.menu_font = menu_font
        self.p_font = p_font
        self.pos_font = pos_font
        self.speed_font = speed_font
        self.monster_font = monster_font
        self.xy_font = xy_font

        # game_objects.append(umo)

    # future function for making light outside of player class, will be needed eventually
    # def create_light(self, screen, x, y, radius, color, alpha_level):
    
    #     pygame.gfxdraw.filled_circle(screen, x ,y ,radius ,(color[0],color[1],color[2],alpha_level))
    def track_stats(self):

        bool_color1 = WHITE
        if self.player.is_sprinting:
            bool_color1 = (GREEN)
        if self.player.in_sprint_cooldown:
            bool_color1 = (RED)

        bool_color2 = WHITE
        if self.player.is_crouching:
            bool_color2 = (T_GREEN)
      
        position_text = self.pos_font.render(f"Pos: ({int(self.player.coords.x)}, {int(self.player.coords.y)})", True, RED)
        speed_text = self.speed_font.render(f"FPS: ({FPS}) Speed: {self.player.speed}", True, PURPLE)
        x_text = self.xy_font.render(f'x-vel(pixel): {self.player.velocity_x:.3f}', True, GRAY)
        y_text = self.xy_font.render(f'y-vel(pixel): {self.player.velocity_y:.3f}', True, GRAY)
        sprint_text = self.speed_font.render(f'SPRINT: {self.player.is_sprinting} CD: {self.player.in_sprint_cooldown} SF: {sprint_factor:.1f}', True, bool_color1)
        crouch_text = self.speed_font.render(f'CROUCH: {self.player.is_crouching} CD: N/A  CF: {crouch_factor:.1f}', True, bool_color2)
        
        for i, monster in enumerate(self.monsters):
            monster_text = self.monster_font.render(
                f'{monster.name}-vel:(x:{monster.vel_x:.3f}, y:{monster.vel_y:.3f}) '
                f'-pos:(x:{int(monster.coords.x)}, y:{int(monster.coords.y)}) (x:{int(monster.pos.x)}, y"{int(monster.pos.y)})',
                True, GREEN)
            self.screen.blit(monster_text, (20, 10 + i * 15))

        self.screen.blit(sprint_text, (SCREEN_WIDTH - 300, 32))
        self.screen.blit(crouch_text, (SCREEN_WIDTH - 300, 50))
        self.screen.blit(position_text, (SCREEN_WIDTH - 500, 10))
        self.screen.blit(speed_text, (SCREEN_WIDTH - 300, 10))
        self.screen.blit(x_text, (SCREEN_WIDTH - 500, 30))
        self.screen.blit(y_text, (SCREEN_WIDTH - 500, 45))

    def on_click_spawn(self):

        random_index = random.randint(0, len(monster_list) - 1)
        random_mon = monster_list[random_index] # make a monster_list dictionary in the future
        
        new_monster = Monster('dict-name',self.player, random_mon, 900, 650, 2, 300, 500, 100)
        # last 3 paramters and name are generic because: no dict for monster_list, no subclasses for monster types
        if len(self.monsters) < 15: # any starting monsters not in the list break this mob cap method from being accurate
            self.monsters.append(new_monster)
            self.game_objects.append(new_monster)
        else:
            print('Reached mob cap of 15')
        # print(f'{len(self.monsters)} in self.monsters list')

    def update(self):

        # iterates and updates all game objects
        for obj in self.game_objects:
            obj.update()
            if self.button.update(): # if "action = True" is returned
                self.on_click_spawn()

    def draw(self):
        # iterates and draws all objects
        for obj in self.game_objects:
            obj.draw(screen)
        self.button.draw(screen)

        if pygame.sprite.spritecollide(self.player, self.monsters, False, pygame.sprite.collide_mask) and self.player.show_mask:
            screen.blit(self.player.mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(155,55,55,255)), 
                ((self.player.rect.centerx - self.player.player_width , self.player.rect.centery - self.player.player_height)))    


    # State Machine, always runs, checks which Game State we are in
    def run(self):
        global game_state
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: # toggle keys
                    if event.key == pygame.K_m:
                        # toggle keys only
                        self.player.show_mask = not self.player.show_mask

            if game_state == PLAYING:
                self.update()
                self.draw()
                self.track_stats()
                pygame.display.flip()
                self.clock.tick(FPS)

            if game_state == PAUSE:     ###
                pygame.quit()       # TEMPORARY! DO NOT KEEP THIS LOL
                sys.exit()              ###

# player instance
player = Player()
button = Button((SCREEN_WIDTH//2 - 64), 10, spawn_button, 1)


# Create game instance and run the game
game = BaseGame()
game.run()