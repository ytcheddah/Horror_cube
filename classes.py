import pygame
import math
import sys
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
pygame.display.set_caption("Horror Cube")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font("font/boldPixelFont.ttf", 74)
p_font = pygame.font.Font("font/pixelFont.ttf", 36)
pos_font = pygame.font.Font("font/pixelFont.ttf", 16)
speed_font = pygame.font.Font("font/pixelFont.ttf", 18)
xy_font = pygame.font.Font("font/pixelFont.ttf", 14)
monster_font = pygame.font.Font("font/pixelFont.ttf", 16)

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
zenba_monster = pygame.image.load("images/zenba_sprites/zenba1.png").convert_alpha()
umo_monster = pygame.image.load("images/umo_Sprites/roam_chase/umo-rc-09.png")
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

# Object Initialization
game_objects = []

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0, 2)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.player_width = PLAYER_WIDTH
        self.player_height = PLAYER_HEIGHT
        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Screen and Background position initialization
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.bg_pos = pygame.math.Vector2(0,0)
        self.bg_speed = PLAYER_SPEED

        # "virtual" position, keeps me in the middle off the screen
        self.virt_pos = pygame.math.Vector2(self.screen_width//2, self.screen_height//2)

        # Sprint Attributes
        self.is_sprinting = False
        self.in_cooldown = False  # New attribute to track cooldown state
        self.sprint_duration = 2000  # Sprint (milliseconds)
        self.sprint_cooldown = 7000  # Cooldown (milliseconds)
        self.sprint_timer = 0
        self.cooldown_timer = 0

        # Trap Management
        self.inventoryTraps = []
        self.trapCooldown = 1000
        self.lastTrapTime = -self.trapCooldown # Ensures placing new Trap, checks time of old one

    def user_input(self):
        keys = pygame.key.get_pressed()
        self.velocity_x = 0
        self.velocity_y = 0
        global left
        global right
        global walkCount
        global sprint_factor
        if keys[pygame.K_w] or keys[pygame.K_UP]: # and self.pos.y > 0 - 30 - PLAYER_SPEED:
            self.velocity_y = -self.speed
            self.bg_y = self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: # and self.pos.y < HEIGHT - 120 - PLAYER_SPEED:
            self.velocity_y = self.speed
            self.bg_y = -self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: # and self.pos.x > 0 - 30 - PLAYER_SPEED:
            self.velocity_x = -self.speed
            self.bg_x = self.speed
            left = True
            right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: # and self.pos.x < WIDTH - 150 - PLAYER_SPEED:
            self.velocity_x = self.speed
            self.bg_x = -self.speed
            right = True
            left = False
        else:
            walkCount = 0

        if self.velocity_x != 0 and self.velocity_y != 0: # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if keys[pygame.K_ESCAPE]:
            global game_state
            game_state = PAUSE

        # Handle spacebar to place trap
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.lastTrapTime >= self.trapCooldown:
                self.create_trap()
                self.lastTrapTime = current_time # Update the last trap to correct time           

        # Handle sprinting
        if (self.velocity_x and self.velocity_y) or self.velocity_x or self.velocity_y != 0: # checks for moving, seems buggy (could be keyboard)
            if keys[pygame.K_LSHIFT] and not self.is_sprinting and not self.in_cooldown:
                self.is_sprinting = True
                self.speed = self.base_speed * 1.5  # Increase speed by 50%
                self.sprint_timer = pygame.time.get_ticks()  # Start sprint timer
                if self.is_sprinting:
                    sprint_factor = 2               
                    
        # Sprint duration management
        if self.is_sprinting:
            if pygame.time.get_ticks() - self.sprint_timer > self.sprint_duration:
                self.is_sprinting = False
                self.speed = self.base_speed  # Reset speed to normal
                self.cooldown_time_left = self.sprint_cooldown  # Set cooldown time
                self.cooldown_timer_start = pygame.time.get_ticks()  # Start cooldown timer
                self.in_cooldown = True  # Enter cooldown state

        # Cooldown management
        if self.in_cooldown:
            sprint_factor = 1
            elapsed_time = pygame.time.get_ticks() - self.cooldown_timer_start
            self.cooldown_time_left = max(self.cooldown_time_left - elapsed_time, 0)
            self.cooldown_timer_start = pygame.time.get_ticks()  # Update timer start to keep it consistent
            if self.cooldown_time_left <= 0:
                self.in_cooldown = False  # Exit cooldown state

    def move(self):
        # self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.virt_pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.bg_pos += pygame.math.Vector2(-self.velocity_x, -self.velocity_y)


    def create_trap(self):
        # Create a new "trap" (circle) under the player
        trap_x = self.virt_pos.x + self.image.get_width() // 2 # center the circle horizontally
        trap_y = self.virt_pos.y + self.image.get_height() - 30 # place trap under player
        new_trap = Trap(trap_x,trap_y)
        self.inventoryTraps.append(new_trap)

    def track_stats(self): # meant to help us develop, not for game itself
        position_text = pos_font.render(f"Pos: ({int(self.pos.x)}, {int(self.pos.y)})", True, RED)
        speed_text = speed_font.render(f"FPS: ({FPS}) Speed: {self.speed}", True, RED)
        x_text = xy_font.render(f'x-vel(pixel): {self.velocity_x:.5f}', True, GRAY )
        y_text = xy_font.render(f'y-vel(pixel): {self.velocity_y:.5f}', True, GRAY )
        monster_text = monster_font.render(f'mons-vel:(x:{umo.vel_x:.5f}, y:{umo.vel_y:.5f}) mons-pos:(x:{umo.pos.x:.2f}, y:{umo.pos.y:.2f})', True, GREEN)
        screen.blit(position_text, (10, 10))  # Render position at the top-left corner
        screen.blit(speed_text, (SCREEN_WIDTH - 200, 10))
        screen.blit(x_text, (10, 30))
        screen.blit(y_text, (10, 45))
        screen.blit(monster_text, (200, 10))

    def draw(self, screen):
        global walkCount
        screen.fill(WHITE)
        screen.blit(bg, self.bg_pos)
        # screen.blit(zenba_monster, ((SCREEN_WIDTH//2) - 50, (SCREEN_HEIGHT//2) - 50))
        # Draw Player
        if walkCount + 1 >= 60:
            walkCount = 0
        if left:
            # screen.blit(pygame.transform.flip(walkRight[walkCount//5], True, False), (self.pos))
            screen.blit(pygame.transform.flip(walkRight[walkCount//5], True, False), ((SCREEN_WIDTH//2) - (self.player_width//2), (SCREEN_HEIGHT//2) - self.player_height//2))
            walkCount += 1 * int(sprint_factor)
        elif right:
            # screen.blit(walkRight[walkCount//5], (self.pos))
            screen.blit(walkRight[walkCount//5], ((SCREEN_WIDTH//2) - (self.player_width//2), (SCREEN_HEIGHT//2) - self.player_height//2))
            walkCount += 1 * int(sprint_factor)
        else:
            # screen.blit(self.image, self.pos)        
            screen.blit(self.image, ((SCREEN_WIDTH//2) - (self.player_width//2), (SCREEN_HEIGHT//2) - self.player_height//2))
        # Draw Traps
        for trap in self.inventoryTraps:
            trap.draw(screen)


    def update(self):
        self.user_input()
        self.move()
        # Updates traps and remove any that have expired
        self.inventoryTraps = [trap for trap in self.inventoryTraps if trap.update()]

class Trap:

    def __init__(self, x, y, radius=20, duration=5000):
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
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

class Monster(object):

    def __init__(self, player, pos_x, pos_y, width, height, speed, agro_distance):
        self.player = player
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.width = width
        self.height = height
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.agro_distance = agro_distance

    def draw(self, screen):
        self.move()
        screen.blit(umo_monster,self.pos)

    def move(self):
        self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        
    def behavior(self):
        self.vel_x = 0
        self.vel_y = 0
        # Follow player if within agro distance
        if abs(self.pos.x - self.player.pos.x) < self.agro_distance:
            if abs(self.pos.y - self.player.pos.y) < self.agro_distance:
                if self.pos.x > self.player.pos.x:
                    self.vel_x = -self.speed            
                if self.pos.x < self.player.pos.x:
                    self.vel_x = self.speed
                if self.pos.y > self.player.pos.y:
                    self.vel_y = -self.speed        
                if self.pos.y < self.player.pos.y:
                    self.vel_y = self.speed
        
        if self.vel_x != 0 and self.vel_y != 0: # moving diagonally normilization
            self.vel_x /= math.sqrt(2)
            self.vel_y /= math.sqrt(2)

    def update(self):
        self.behavior()
        self.move()

#player and monster instances
player = Player()
umo = Monster(player, 1000, 600, 100, 100, 1, 400)

game_objects.append(player)
game_objects.append(umo)

# All non-player objects

# State Machine, always runs, checks which Game State we are in
class Game:

    def __init__(self):
        self.screen = screen
        self.clock = clock
        self.player = Player()
        self.monster = Monster(self.player, 1000, 600, 100, 100, 1, 400)
        self.game_objects = [self.player, self.monster]
        self.font = font
        self.xy_font = xy_font
        self.monster_font = monster_font

    def track_stats(self):
        position_text = self.font.render(f"Pos: ({int(self.player.pos.x)}, {int(self.player.pos.y)})", True, RED)
        speed_text = self.font.render(f"FPS: ({FPS}) Speed: {self.player.speed}", True, RED)
        x_text = self.xy_font.render(f'x-vel(pixel): {self.player.velocity_x:.5f}', True, GRAY)
        y_text = self.xy_font.render(f'y-vel(pixel): {self.player.velocity_y:.5f}', True, GRAY)
        monster_text = self.monster_font.render(f'mons-vel:(x:{self.monster.vel_x:.5f}, y:{self.monster.vel_y:.5f}) '
                                                f'mons-pos:(x:{self.monster.pos.x:.2f}, y:{self.monster.pos.y:.2f})', True, GREEN)

        self.screen.blit(position_text, (10, 10))
        self.screen.blit(speed_text, (SCREEN_WIDTH - 200, 10))
        self.screen.blit(x_text, (10, 30))
        self.screen.blit(y_text, (10, 45))
        self.screen.blit(monster_text, (200, 10))

    def update(self):
        self.player.update()
        for obj in self.game_objects:
            obj.update()
        self.track_stats()

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
                self.player.draw(self.screen)
                self.monster.draw(self.screen)
                pygame.display.flip()
                self.clock.tick(FPS)
                self.track_stats()

# Create game instance and run the game
game = Game()
game.run()


# class Player(pygame.sprite.Sprite):

#     def __init__(self):
#         super().__init__()
#         self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0, 2)
#         self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
#         self.player_width = PLAYER_WIDTH
#         self.player_height = PLAYER_HEIGHT
#         self.base_speed = PLAYER_SPEED
#         self.speed = self.base_speed
#         self.velocity_x = 0
#         self.velocity_y = 0
        
#         # Screen and Background position initialization
#         self.screen_width = SCREEN_WIDTH
#         self.screen_height = SCREEN_HEIGHT
#         self.bg_x = 0
#         self.bg_y = 0
#         self.bg_speed = PLAYER_SPEED

#         # Sprint Attributes
#         self.is_sprinting = False
#         self.in_cooldown = False
#         self.sprint_duration = 2000  # Sprint (milliseconds)
#         self.sprint_cooldown = 7000  # Cooldown (milliseconds)
#         self.sprint_timer = 0
#         self.cooldown_timer = 0

#     def user_input(self):
#         keys = pygame.key.get_pressed()
#         self.velocity_x = 0
#         self.velocity_y = 0
#         global left
#         global right
#         global walkCount
#         global sprint_factor
#         if keys[pygame.K_w]:
#             self.velocity_y = -self.speed
#         if keys[pygame.K_s]:
#             self.velocity_y = self.speed
#         if keys[pygame.K_a]:
#             self.velocity_x = -self.speed
#             left = True
#             right = False
#         if keys[pygame.K_d]:
#             self.velocity_x = self.speed
#             right = True
#             left = False
#         else:
#             walkCount = 0

#         if self.velocity_x != 0 and self.velocity_y != 0:
#             self.velocity_x /= math.sqrt(2)
#             self.velocity_y /= math.sqrt(2)

#         if keys[pygame.K_ESCAPE]:
#             global game_state
#             game_state = PAUSE

#     def move(self):
#         # Move player position
#         self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        
#         # Move background position to create the illusion of player movement
#         self.bg_x -= self.velocity_x
#         self.bg_y -= self.velocity_y

#     def draw(self, screen):
#         global walkCount
#         screen.fill(WHITE)
#         screen.blit(bg, (self.bg_x, self.bg_y))
        
#         if walkCount + 1 >= 60:
#             walkCount = 0
            
#         if self.velocity_x != 0 or self.velocity_y != 0:  # Player is moving
#             if left:
#                 screen.blit(pygame.transform.flip(walkRight[walkCount // 5], True, False), 
#                             (SCREEN_WIDTH // 2 - self.player_width // 2, SCREEN_HEIGHT // 2 - self.player_height // 2))
#                 walkCount += 1 * int(sprint_factor)
#             elif right:
#                 screen.blit(walkRight[walkCount // 5], 
#                             (SCREEN_WIDTH // 2 - self.player_width // 2, SCREEN_HEIGHT // 2 - self.player_height // 2))
#                 walkCount += 1 * int(sprint_factor)
#         else:
#             # If no movement, show idle
#             screen.blit(self.image, 
#                         (SCREEN_WIDTH // 2 - self.player_width // 2, SCREEN_HEIGHT // 2 - self.player_height // 2))

# class Monster:

#     def __init__(self, player, pos_x, pos_y, width, height, speed, agro_distance):
#         self.player = player
#         self.pos = pygame.math.Vector2(pos_x, pos_y)
#         self.width = width
#         self.height = height
#         self.speed = speed
#         self.vel_x = 0
#         self.vel_y = 0
#         self.agro_distance = agro_distance

#     def draw(self, screen):
#         self.move()
#         screen.blit(umo_monster, self.pos)

#     def move(self):
#         self.pos += pygame.math.Vector2(self.vel_x, self.vel_y)
        
#     def behavior(self):
#         self.vel_x = 0
#         self.vel_y = 0
#         if abs(self.pos.x - self.player.pos.x) < self.agro_distance:
#             if abs(self.pos.y - self.player.pos.y) < self.agro_distance:
#                 if self.pos.x > self.player.pos.x:
#                     self.vel_x = -self.speed            
#                 if self.pos.x < self.player.pos.x:
#                     self.vel_x = self.speed
#                 if self.pos.y > self.player.pos.y:
#                     self.vel_y = -self.speed        
#                 if self.pos.y < self.player.pos.y:
#                     self.vel_y = self.speed
        
#         if self.vel_x != 0 and self.vel_y != 0:
#             self.vel_x /= math.sqrt(2)
#             self.vel_y /= math.sqrt(2)

#     def update(self):
#         self.behavior()
#         self.move()

# class Game:

#     def __init__(self):
#         self.screen = screen
#         self.clock = clock
#         self.player = Player()
#         self.monster = Monster(self.player, 1000, 600, 100, 100, 1, 400)
#         self.game_objects = [self.player, self.monster]
#         self.font = font
#         self.xy_font = xy_font
#         self.monster_font = monster_font

#     def track_stats(self):
#         position_text = self.font.render(f"Pos: ({int(self.player.pos.x)}, {int(self.player.pos.y)})", True, RED)
#         speed_text = self.font.render(f"FPS: ({FPS}) Speed: {self.player.speed}", True, RED)
#         x_text = self.xy_font.render(f'x-vel(pixel): {self.player.velocity_x:.5f}', True, GRAY)
#         y_text = self.xy_font.render(f'y-vel(pixel): {self.player.velocity_y:.5f}', True, GRAY)
#         monster_text = self.monster_font.render(f'mons-vel:(x:{self.monster.vel_x:.5f}, y:{self.monster.vel_y:.5f}) '
#                                                 f'mons-pos:(x:{self.monster.pos.x:.2f}, y:{self.monster.pos.y:.2f})', True, GREEN)

#         self.screen.blit(position_text, (10, 10))
#         self.screen.blit(speed_text, (SCREEN_WIDTH - 200, 10))
#         self.screen.blit(x_text, (10, 30))
#         self.screen.blit(y_text, (10, 45))
#         self.screen.blit(monster_text, (200, 10))

#     def update(self):
#         self.player.update()
#         for obj in self.game_objects:
#             obj.update()
#         self.track_stats()

#     def run(self):
#         global game_state
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.quit()
#                     sys.exit()

#             if game_state == PLAYING:
#                 self.update()
#                 self.player.draw(self.screen)
#                 self.monster.draw(self.screen)
#                 pygame.display.flip()
#                 self.clock.tick(FPS)

# # Create game instance and run the game
# game = Game()
# game.run()
