import pygame
import math
import random
import sys
from random import randint

import pygame.gfxdraw
from settings import *


# --- Put all classes in this file and then import them into the other files to improve readability ---
# actually just try to make monsters work here then copy it over, we can organize file types later lol

# Initialize Pygame
pygame.init()
pygame.mixer.init()

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
zenba_mon = pygame.image.load("images/zenba_sprites/zenba1.png").convert_alpha()
umo_mon = pygame.image.load("images/umo_Sprites/roam_chase/umo-rc-09.png").convert_alpha()
filth_mon = pygame.transform.rotozoom(pygame.image.load("images/anth_sprites/80x80/filth1.png").convert_alpha(), 0, 2)
louis_mon = pygame.image.load("images/anth_sprites/64x64/louis1.png").convert_alpha()
squihomie_mon = pygame.transform.rotozoom(pygame.image.load("images/anth_sprites/64x64/squihomie1.png").convert_alpha(), 0, 2)
thecarne_mon = pygame.image.load("images/anth_sprites/64x64/thecarne1.png").convert_alpha()

monster_list = [zenba_mon, umo_mon, filth_mon, louis_mon, squihomie_mon, thecarne_mon]
# MONSTER_IMAGES.append(zenba_mon,umo_mon,filth_mon,louis_mon,squihomie_mon,thecarne_mon)

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

# Button initialization
spawn_button = pygame.image.load('images/spawn_button1.png').convert_alpha()

# Object Initialization
game_objects = []

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # load the image and scale it
        self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0 , 2)
        # get_rect() gets the rectangular area of a given surface, the kwarg "center" creates a rectangle for the Surface centered at the given position
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pos = pygame.math.Vector2(self.rect.center) # where I am on the screen

        self.player_width = PLAYER_WIDTH
        self.player_height = PLAYER_HEIGHT
        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        self.velocity_x = 0
        self.velocity_y = 0

        # Glowstick attr
        self.light_radius = 100
        self.light_power = 10
        
        # creates transparent-capable surface for "light" (shapes) to draw to
        self.light_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # darkness surface, unique transparency value from light surface
        self.darkness_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.darkness_rect = self.darkness_surf.get_rect(center = (0, 0))

        # Background-related initialization
        self.bg_pos = pygame.math.Vector2(0,0) # Where the map is (objects should be pos here, render will be the sauce to make it seemless)
        self.bg_speed = PLAYER_SPEED
        self.coords = pygame.math.Vector2(self.bg_pos + self.rect.center)

        # Sprint Attributes
        self.is_sprinting = False
        self.in_sprint_cooldown = False  # Cooldown state
        self.sprint_duration = 2000  # Sprint duration (milliseconds)
        self.sprint_cooldown = 3000  # Cooldown duration (milliseconds)
        self.sprint_timer_start = 0  # Timer to track sprint duration
        self.cooldown_timer_start = 0  # Timer to track cooldown duration
        self.sprint_factor = 1  # Multiplier for sprinting speed
        self.shift_held = False  # Track if Shift is held

        # Crouch Attributes
        self.is_crouching = False

        # Trap Management
        self.inventoryTraps = []
        self.trapCooldown = 1000
        self.lastTrapTime = -self.trapCooldown # Ensures placing new Trap, checks time of old one

    def user_input(self):
        keys = pygame.key.get_pressed()
        global left, right, walkCount, sprint_factor, crouch_factor
        self.velocity_x = 0
        self.velocity_y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]: 
            self.velocity_y = -self.speed
            self.bg_y = self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: 
            self.velocity_y = self.speed
            self.bg_y = -self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
            self.velocity_x = -self.speed
            self.bg_x = self.speed
            left = True
            right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
            self.velocity_x = self.speed
            self.bg_x = -self.speed
            right = True
            left = False
        else:
            walkCount = 0

        # If no input, reset walkCount
        if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
            walkCount = 0

        if self.velocity_x != 0 and self.velocity_y != 0: # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if keys[pygame.K_ESCAPE]:
            global game_state
            game_state = PAUSE

        # Sprint logic (only sprint while Shift is held)
        if keys[pygame.K_LSHIFT] and not self.in_sprint_cooldown and not self.is_crouching:
            self.shift_held = True
            self.is_sprinting = True
            self.speed = self.base_speed * 1.5  # Increase speed by 50%
            sprint_factor = 2
        if (self.velocity_x and self.velocity_y) or self.velocity_x or self.velocity_y != 0: # checks for moving, seems buggy (could be keyboard)
            if not keys[pygame.K_LSHIFT] and not self.in_sprint_cooldown:
                self.sprint_timer_start = pygame.time.get_ticks()  # Start the sprint timer
                # print('multiple print = problem')
                self.shift_held = False
                if not self.shift_held:
                    # print('multiple print = problem')
                    self.in_sprint_cooldown

        # Handle Crouching
        if (self.velocity_x and self.velocity_y) or self.velocity_x or self.velocity_y != 0: # checks for moving
            if keys[pygame.K_LCTRL]:
                self.is_crouching = True
                self.speed = self.base_speed * .6 # Decrease to 60% speed
                if self.is_crouching:
                    crouch_factor = .5
                    # if self.is_sprinting:
                    #     self.in_sprint_cooldown = False
            else:
                self.is_crouching = False

        # Temporary check monster spawning
        if keys[pygame.K_k]:
            pass

        # Handle spacebar to place trap
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.lastTrapTime >= self.trapCooldown:
                self.create_trap()
                self.lastTrapTime = current_time # Update the last trap to correct time    

    def update_cooldown(self):

        global sprint_factor, crouch_factor
        # sprint duration management
        if self.is_sprinting:
            # Check if sprint duration has been exceeded
            if pygame.time.get_ticks() - self.sprint_timer_start > self.sprint_duration:  # or not self.shift_held:
                self.is_sprinting = False
                self.speed = self.base_speed  # Reset speed
                self.cooldown_timer_start = pygame.time.get_ticks()  # Start cooldown
                self.in_sprint_cooldown = True
        
        # Cooldown Management
        if self.in_sprint_cooldown:
            sprint_factor = 1
            if pygame.time.get_ticks() - self.cooldown_timer_start >= self.sprint_cooldown:
                self.in_sprint_cooldown = False # Exit Cooldown
        
        # Crouch Management
        if not self.is_crouching and not self.is_sprinting:
            crouch_factor = 1
            self.speed = self.base_speed

    def move(self):
       
        # Player movement
        self.rect.center += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.rect.center = self.pos

        # Map movement (caused by player input)
        self.bg_pos += pygame.math.Vector2(-self.velocity_x, -self.velocity_y)

        # position rel to map
        self.coords += pygame.math.Vector2(self.velocity_x, self.velocity_y)

        # Trap movement rel to player after placed
        for trap in self.inventoryTraps:
            trap.x += -self.velocity_x
            trap.y += -self.velocity_y
        
    def create_trap(self):
        # Create a new "trap" (circle) under the player
        trap_x = (self.rect.x)  # center the circle horizontally
        trap_y = (self.rect.y) - 50 # place trap under player
        new_trap = Trap(player,trap_x,trap_y)
        self.inventoryTraps.append(new_trap)

    def draw(self, screen):
        global walkCount
        
        # layer stack
        screen.fill(WHITE) # init fill
        screen.blit(bg, self.bg_pos) # map
        # screen.blit(self.darkness_surf, (0, 0)) # darkness_surf
        # pygame.draw.rect(self.darkness_surf, (RED), self.darkness_rect.topleft)
       
        # pygame.draw.rect(screen, 'pink', self.rect)
        screen.blit(self.light_surf, (0, 0))
        pygame.draw.circle(self.light_surf, (0, 0, 0, self.light_power), self.rect.center, self.light_radius)
        # screen.blit(zenba_monster, ((SCREEN_WIDTH//2) - 50, (SCREEN_HEIGHT//2) - 50))
        # Draw Player       
        screen.blit(self.image, ((self.rect.centerx - self.player_width , self.rect.centery - self.player_height)))
        # Draw Traps
        for trap in self.inventoryTraps:
            trap.draw(screen)

    def update(self):
        self.user_input()
        self.update_cooldown()
        self.move()
        # Updates traps and remove any that have expired
        self.inventoryTraps = [trap for trap in self.inventoryTraps if trap.update()]

class Trap:

    def __init__(self, player, x, y, radius=20, duration=5000):
        self.player = player
        self.x = x
        self.y = y
        self.radius = radius
        self.creation_time = pygame.time.get_ticks() # Correct reference to pygame.time.get_ticks
        self.duration = duration

    def update(self):
        # Check if the trap has expired (lifetime is over)
        if pygame.time.get_ticks() - self.creation_time > self.duration:
            return False
        return True
    
    def draw(self, screen):
        # pygame.draw.circle(screen, 'pink', (self.x + 100, self.y + 200), self.radius) # needs to be relative to the map
        screen.blit(spike_trap1, (self.x + 75, self.y + 150))


class Monster(object):

    def __init__(self, name, player, image, x, y, speed, agro_distance, pursue_range, attack_range):
        x = randint(0, SCREEN_WIDTH)
        y = randint(0, SCREEN_HEIGHT)
        self.name = name
        self.player = player
        self.image = image
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(x, y) # position on the screen
        self.coords = pygame.math.Vector2(x, y) # Position relative to the map
        # self.coords = pygame.math.Vector2(self.player.bg_pos.x + self.pos.x, self.player.bg_pos.y + self.pos.y)
        self.width = image.get_width()
        self.height = image.get_height()
        self.speed = speed
        self.agro_distance = agro_distance
        self.pursue_range = pursue_range
        self.attack_range = attack_range
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
        self.vel_x = 0
        self.vel_y = 0

        self.chase_duration = 5000 # miliseconds
        self.chase_cooldown = 1000 
        self.in_chase_cooldown = False

    def draw(self, screen):

        self.pos = self.coords
        self.rect.center = (self.pos.x, self.pos.y)
        # Adjusts monster position relative to player's map position
        screen.blit(self.image,self.rect.topleft)

    def move(self):
        # Location relative to map
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        self.pos += pygame.math.Vector2(-self.player.velocity_x, -self.player.velocity_y)

        # Movement logic
        # self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        # self.pos += pygame.math.Vector2(-self.player.velocity_x, -self.player.velocity_y)

    def behavior(self):
        
        # Chase player if within agro distance
        # Check distance between monster and player
        distance_to_player = self.pos.distance_to(self.player.pos)
        
        if distance_to_player <= self.pursue_range:
            if distance_to_player <= self.agro_distance:
                if distance_to_player > self.attack_range: # also prevents jittering and monst going directly on top of player
                    # checks time of the start of the chase
                    chasing_timer = pygame.time.get_ticks()
                    # Calculate direction towards player
                    direction = (self.player.pos - self.pos).normalize()
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
        
    def update(self): # player_pos, map_offset
        self.behavior()
        self.move()

class Button():

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale), (int(height * scale))))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # the list 0-2 is leftmouse, centermouse, rightmouse button
                self.clicked = True
                # print('CLICKED') # debug checker (already works tho)
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

class BaseGame:

    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.player = Player()
        self.button = Button((SCREEN_WIDTH//2 - 64), 10, spawn_button, 1)

        self.monsters = [
            Monster('Umo',self.player, umo_mon, 1000, 600, 1, 300, 500, 125),
            Monster('Louis',self.player, louis_mon, 1200, 500, 3, 250, 500, 75),
            Monster('Squihomie',self.player, squihomie_mon, 850, 700, 2, 300, 500, 100),
            Monster('the Carne',self.player, thecarne_mon, 1000, 300, 1.5, 250, 300, 75)
        ]
        
        self.game_objects = [self.player, self.button] + self.monsters

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
                f'-pos:(x:{int(monster.coords.x)}, y:{int(monster.coords.y)})',
                True, GREEN)
            self.screen.blit(monster_text, (10, 10 + i * 15))

        self.screen.blit(sprint_text, (SCREEN_WIDTH - 300, 32))
        self.screen.blit(crouch_text, (SCREEN_WIDTH - 300, 50))
        self.screen.blit(position_text, (SCREEN_WIDTH - 500, 10))
        self.screen.blit(speed_text, (SCREEN_WIDTH - 300, 10))
        self.screen.blit(x_text, (SCREEN_WIDTH - 500, 30))
        self.screen.blit(y_text, (SCREEN_WIDTH - 500, 45))

    def on_click_spawn(self):

        random_index = random.randint(0, len(monster_list) - 1)
        random_mon = monster_list[random_index] # make a monster_list dictionary in the future
        
        new_monster = Monster('added',self.player, random_mon, 900, 650, 2, 300, 500, 100)
        # last 3 paramters are generic because: no dict for monster_list, no subclasses for monster types
        if len(self.game_objects) < 14:
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

    # State Machine, always runs, checks which Game State we are in
    def run(self):
        global game_state
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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

# Create game instance and run the game
game = BaseGame()
game.run()
