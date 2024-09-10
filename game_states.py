import pygame
import sys
import math
from settings import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()


# Initial state
game_state = MENU

# Screen display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Horror Cube")
clock = pygame.time.Clock()

# Fonts
menu_font = pygame.font.Font("font/boldPixelFont.ttf", 74)
p_font = pygame.font.Font("font/pixelFont.ttf", 36)
pos_font = pygame.font.Font("font/pixelFont.ttf", 16)
speed_font = pygame.font.Font("font/pixelFont.ttf", 18)
xy_font = pygame.font.Font("font/pixelFont.ttf", 14)

# initialize Menu music 
pygame.mixer.music.load('sound/Cube_Hell_menu_music.mp3')
pygame.mixer.music.set_volume(DEFAULT_MUSIC_VOLUME)

# Menu items
menu_items = ['Start Game','Options','Exit']
selected_item = 0
mouse_pos = pygame.mouse.get_pos()

# Pause Menu Items
pause_menu_items = ['Resume','Inventory','Options','Save Game','Return to Main Menu']
pause_selected_item = 0

# Initialize and Load Images
background = pygame.transform.scale(pygame.image.load("images/test-image2.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))
zenba = pygame.image.load("images/zenba_sprites/zenba1.png").convert_alpha()
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

def draw_menu(selected_item):

    screen.fill(BLACK)
    
    label = menu_font.render(item, True, color)
    label_rect = label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + index * 100))
    screen.blit(label, label_rect)

    for index, item in enumerate(menu_items):
        # color = WHITE if index == selected_item else (100, 100, 100)
        if index or label_rect.collidepoint(mouse_pos) == selected_item:
            color = WHITE
            print(pygame.mouse.get_pressed)
        else: 
            color = (100, 100, 100)
        # if label_rect.collidepoint(mouse_pos): 
        #     print(pygame.mouse.get_pressed())
        

    pygame.display.flip()

def handle_menu_input():

    global game_state, selected_item
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # print(f"Key pressed: {pygame.key.name(event.key)}")  # Debug print
            if event.key in [pygame.K_UP, pygame.K_w]:
                selected_item = (selected_item - 1) % len(menu_items)
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                selected_item = (selected_item + 1) % len(menu_items)
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                if selected_item == 0:  # Start Game
                    pygame.mixer.music.stop()
                    game_state = PLAYING
                if selected_item == 1:  # Options
                    print("Options selected")
                if selected_item == 2:  # Exit
                    pygame.quit()
                    sys.exit()

def draw_pause_menu(pause_selected_item):

    # draws a semi-transparent BLUEish BOX (bb) for the Pause Menu Text to be on
    bb = pygame.Surface(([SCREEN_WIDTH - (SCREEN_WIDTH * .4),SCREEN_HEIGHT - (SCREEN_HEIGHT * .4)]), pygame.SRCALPHA)
    bb.fill((105,125,250,100)) # RGBA - last number is Alpha value (aka ratio of transparency)
    bb.set_alpha(25)
    screen.blit(bb, ((SCREEN_WIDTH - (SCREEN_WIDTH * .8)),SCREEN_HEIGHT - (SCREEN_HEIGHT * .8)))
    # draws BLACK BORDER on top of box on the Pause Menu
    pygame.draw.rect(screen, BLACK, pygame.Rect((SCREEN_WIDTH - (SCREEN_WIDTH * .8),(SCREEN_HEIGHT - (SCREEN_HEIGHT * .8)), (SCREEN_WIDTH * .6), (SCREEN_HEIGHT * .6))), 10)    
    for index, item in enumerate(pause_menu_items):
        p_color = ((202, 122, 31)) if index == pause_selected_item else (10, 10, 100)
        p_label = p_font.render(item, True, p_color)
        p_label_rect = p_label.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + index * 90))
        screen.blit(p_label, p_label_rect)
    pygame.display.flip()

def handle_pause_menu_input():

    global game_state, pause_selected_item
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # print(f"Key pressed: {pygame.key.name(event.key)}")  # Debug print
            if event.key in [pygame.K_UP, pygame.K_w]:
                pause_selected_item = (pause_selected_item - 1) % len(pause_menu_items)
            if event.key in [pygame.K_DOWN, pygame.K_s]:
                pause_selected_item = (pause_selected_item + 1) % len(pause_menu_items)
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                if pause_selected_item == 0:  # Resume Game
                    game_state = PLAYING
                if pause_selected_item == 1:  # Inventory
                    print("Inventory selected")
                if pause_selected_item == 2:  # Options
                    print("Options selected")
                if pause_selected_item == 3:  # Save Game
                    print("Save Game selected")
                if pause_selected_item == 4:  # Return to Main Menu
                    pygame.mixer.music.play(-1)
                    game_state = MENU
            if event.key in [pygame.K_ESCAPE]: # can close menu with escape as well as hitting enter on resume
                print('Close Pause Menu')
                game_state = PLAYING
                pygame.time.wait(200) # this fixes a bug where escape doesnt accept game state change and keeps you in pause menu, prolly not suffiecient lol
                    
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0, 2)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.base_speed = PLAYER_SPEED
        self.speed = self.base_speed
        self.velocity_x = 0
        self.velocity_y = 0

        # Sprint Attributes
        self.is_sprinting = False
        self.in_cooldown = False  # New attribute to track cooldown state
        self.sprint_duration = 2000  # Sprint lasts 2 seconds (2000 milliseconds)
        self.sprint_cooldown = 7000  # Cooldown of 3 seconds (3000 milliseconds)
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
        global left
        global right
        if keys[pygame.K_w] or keys[pygame.K_UP] and self.pos.y > 0 - 30 - PLAYER_SPEED:
            self.velocity_y = -self.speed
            if right:
                left = False
            if left:
                right = False
        if keys[pygame.K_s] or keys[pygame.K_DOWN] and self.pos.y < SCREEN_HEIGHT - 120 - PLAYER_SPEED:
            self.velocity_y = self.speed
            if right:
                left = False
            if left:
                right = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT] and self.pos.x > 0 - 30 - PLAYER_SPEED:
            self.velocity_x = -self.speed
            left = True
            right = False
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT] and self.pos.x < SCREEN_WIDTH - 150 - PLAYER_SPEED:
            self.velocity_x = self.speed
            right = True
            left = False
        else:
            right = False
            left = False
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
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def create_trap(self):
        # Create a new "trap" (circle) under the player
        trap_x = self.pos.x + self.image.get_width() // 2 # center the circle horizontally
        trap_y = self.pos.y + self.image.get_height() - 30 # place trap under player
        new_trap = Trap(trap_x,trap_y)
        self.inventoryTraps.append(new_trap)

    def track_stats(self): # meant to help us develop, not for game itself
        # Display the player's position on the screen
        position_text = pos_font.render(f"Position: ({int(self.pos.x)}, {int(self.pos.y)})", True, RED)
        speed_text = speed_font.render(f"FPS: ({FPS}) Speed: {self.speed}", True, RED)
        x_text = xy_font.render(f'x-vel(pixel): {self.velocity_x:.5f}', True, GRAY )
        y_text = xy_font.render(f'y-vel(pixel): {self.velocity_y:.5f}', True, GRAY )
        screen.blit(position_text, (10, 10))  # Render position at the top-left corner
        screen.blit(speed_text, (SCREEN_WIDTH - 200, 10))
        screen.blit(x_text,(10, 30))
        screen.blit(y_text,(10, 45))

    def draw(self, screen):
        global walkCount
        screen.fill(WHITE)
        screen.blit(zenba, ((SCREEN_WIDTH//2) - 50, (SCREEN_HEIGHT//2) - 50))
        # Draw Player
        if walkCount + 1 >= 60:
            walkCount = 0
        if left:
            screen.blit(pygame.transform.flip(walkRight[walkCount//5], True, False), (self.pos))
            walkCount += 1 * int(sprint_factor)
        elif right:
            screen.blit(walkRight[walkCount//5], (self.pos))
            walkCount += 1 * int(sprint_factor)
        else:
            screen.blit(self.image, self.pos)        
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

player = Player()

# State Machine, always runs, checks which Game State we are in
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == MENU:
        pygame.mixer.music.play(-1)
        while game_state == MENU:
            handle_menu_input()
            draw_menu(selected_item)

    if game_state == PLAYING:
        pause_selected_item = 0
        player.update()
        player.draw(screen)
        player.track_stats()
        pygame.display.flip()
        clock.tick(FPS)

    if game_state == PAUSE:
        while game_state == PAUSE:
            handle_pause_menu_input()  
            draw_pause_menu(pause_selected_item) 
            # pygame.display.flip()
            # clock.tick(FPS)
