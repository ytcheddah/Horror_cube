import pygame
import sys
import math
from settings import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSE = "pause"

# Initial state
game_state = MENU

# Screen display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horror Cube")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font("font/boldPixelFont.ttf", 74)
p_font = pygame.font.Font("font/pixelFont.ttf", 36)
pos_font = pygame.font.Font("font/pixelFont.ttf", 16)

# initialize Menu music 
pygame.mixer.music.load('sound/Cube_Hell_menu_music.mp3')
pygame.mixer.music.set_volume(DEFAULT_MUSIC_VOLUME)

# Menu items
menu_items = ['Start Game','Options','Exit']
selected_item = 0

# Pause Menu Items
pause_menu_items = ['Resume','Inventory','Options','Save Game','Return to Main Menu']
pause_selected_item = 0

# Load Images
background = pygame.transform.scale(pygame.image.load("images/test-image2.png").convert(), (WIDTH, HEIGHT))
zenba = pygame.image.load("images/zenba_sprites/zenba1.png").convert_alpha()


def draw_menu(selected_item):

    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        color = WHITE if index == selected_item else (100, 100, 100)
        label = font.render(item, True, color)
        label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 100))
        screen.blit(label, label_rect)
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
    bb = pygame.Surface(([WIDTH - (WIDTH * .4),HEIGHT - (HEIGHT * .4)]), pygame.SRCALPHA)
    bb.fill((105,125,250,100)) # RGBA - last number is Alpha value (aka ratio of transparency)
    bb.set_alpha(25)
    screen.blit(bb, ((WIDTH - (WIDTH * .8)),HEIGHT - (HEIGHT * .8)))
    # draws BLACK BORDER on top of box on the Pause Menu
    pygame.draw.rect(screen, BLACK, pygame.Rect((WIDTH - (WIDTH * .8),(HEIGHT - (HEIGHT * .8)), (WIDTH * .6), (HEIGHT * .6))), 10)    
    for index, item in enumerate(pause_menu_items):
        p_color = ((202, 122, 31)) if index == pause_selected_item else (10, 10, 100)
        p_label = p_font.render(item, True, p_color)
        p_label_rect = p_label.get_rect(center=(WIDTH // 2, HEIGHT // 4 + index * 90))
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

    def track_position(self):
        # Display the player's position on the screen
        position_text = pos_font.render(f"Position: ({int(self.pos.x)}, {int(self.pos.y)})", True, GREEN)
        screen.blit(position_text, (10, 10))  # Render position at the top-left corner

    def update(self):
        self.user_input()
        self.move()


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
        # screen.fill(WHITE)
        screen.blit(background, (0, 0))
        screen.blit(zenba, ((WIDTH//2) - 50, (HEIGHT//2) - 50))
        screen.blit(player.image, player.pos)
        player.track_position()
        pygame.display.flip()
        clock.tick(FPS)

    if game_state == PAUSE:
        while game_state == PAUSE:
            handle_pause_menu_input()  
            draw_pause_menu(pause_selected_item) 
            # pygame.display.flip()
            # clock.tick(FPS)
