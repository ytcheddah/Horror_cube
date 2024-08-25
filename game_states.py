import pygame
import sys
import math
from settings import *

# initializes pygame
pygame.init() 

# initialize music

# game states
MENU = "menu"
PLAYING = "playing"
PAUSE = "pause"

# initial state
game_state = MENU

# screen display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horror Cube")

# font
font = pygame.font.Font("font/boldPixelFont.ttf", 74)

# colors imported from settings

# menu music

pygame.mixer.init()  # Initialize the mixer
pygame.mixer.music.load('sound/Cube_Hell_menu_music.mp3')  # Load the music file
pygame.mixer.music.set_volume(MUSIC_VOLUME)  # Set volume (optional)
pygame.mixer.music.play(-1)  # Play the music on a loop (-1 means loop indefinitely)

# menu items
menu_items = ['Start Game', 'Options', 'Exit']
selected_item = 0

def draw_menu(selected_item):
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        if index == selected_item:
            label = font.render(item, True, WHITE)
        else:
            label = font.render(item, True, (100, 100, 100))

        label_rect = label.get_rect(center=(640, 360 + index * 100))
        screen.blit(label, label_rect)

    pygame.display.flip()

def handle_menu_input():
    global game_state, selected_item
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if selected_item == 0:  # Start Game
                    game_state = PLAYING
                elif selected_item == 1:  # Options (implement if needed)
                    print("Options selected")
                elif selected_item == 2:  # Exit
                    pygame.quit()
                    sys.exit()
# Game loop
running = True
while running:
    if game_state == MENU:
        handle_menu_input()
        draw_menu(selected_item)
    elif game_state == PLAYING:

# stop music
        pygame.mixer.music.stop()

# Creating the window
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Horror Cube")
        clock = pygame.time.Clock()

# Loads Images

        background = pygame.transform.scale(pygame.image.load("images/test-image2.png").convert(), (WIDTH, HEIGHT))

        class Player(pygame.sprite.Sprite):

            def __init__(self):
                #this below calls the parent class' constructor, which is the sprite class
                super().__init__()
                self.sprites = []


                self.image = pygame.transform.rotozoom(pygame.image.load("images/umo_Sprites/idle/umo-idle-0.png").convert_alpha(), 0, 0.5)
                self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
                self.speed = PLAYER_SPEED
                
            def animate(self):

                self.is_animating = True


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

                # if keys[pygame.K_r]:
                #     self.current_sprite += 1


            def move(self):

                self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)


            def update(self):


                # if self.is_animating == True:

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

            # if game_state == PLAYING:
            #     # Example: Pressing ESC pauses the game and returns to the menu
            #     for event in pygame.event.get():
            #         if event.type == pygame.KEYDOWN:
            #             if event.key == pygame.K_ESCAPE:
            #                 game_state = MENU

