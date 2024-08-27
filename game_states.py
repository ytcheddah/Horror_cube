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

# Font
font = pygame.font.Font("font/boldPixelFont.ttf", 74)

# Menu music
pygame.mixer.music.load('sound/Cube_Hell_menu_music.mp3')
pygame.mixer.music.set_volume(MUSIC_VOLUME)
pygame.mixer.music.play(-1)

# Menu items
menu_items = ['Start Game', 'Options', 'Exit']
selected_item = 0

# Load Images
background = pygame.transform.scale(pygame.image.load("images/test-image2.png").convert(), (WIDTH, HEIGHT))


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
            print(f"Key pressed: {pygame.key.name(event.key)}")  # Debug print
            if event.key in [pygame.K_UP, pygame.K_w]:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                if selected_item == 0:  # Start Game
                    game_state = PLAYING
                elif selected_item == 1:  # Options (implement if needed)
                    print("Options selected")
                elif selected_item == 2:  # Exit
                    pygame.quit()
                    sys.exit()


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


player = Player()

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_state == MENU:
        handle_menu_input()
        draw_menu(selected_item)

    elif game_state == PLAYING:
        player.update()
        screen.blit(background, (0, 0))
        screen.blit(player.image, player.pos)
        pygame.display.flip()
        clock.tick(FPS)

    elif game_state == PAUSE:
        handle_menu_input()  # Optionally handle input for pause state
        draw_menu(selected_item)  # Draw the menu in pause state
        pygame.display.flip()
        clock.tick(FPS)
