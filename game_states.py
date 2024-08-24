import pygame
import sys

# initializes pygame
pygame.init() 

# game states
MENU = "menu"
PLAYING = "playing"
PAUSE = "pause"

#initial state
game_state = MENU

#sud
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Horror Cube")

#font
font = pygame.font.Font("Horror-Cube/font/boldPixelFont.ttf", 74)

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#menu items
menu_items = ['Start Game', 'Options', 'Exit']
selected_item = 0

def draw_menu(selected_item):
    screen.fill(BLACK)
    for index, item in enumerate(menu_items):
        if index == selected_item:
            label = font.render(item, True, WHITE)
        else:
            label = font.render(item, True, (100, 100, 100))

        label_rect = label.get_rect(center=(400, 300 + index * 100))
        screen.blit(label, label_rect)

    pygame.display.flip()

def handle_menu_input():
    global game_state, selected_item
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_item = (selected_item - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_item = (selected_item + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
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
        # Your existing game logic goes here
        # Example:
        screen.fill(WHITE)
        # Add your game drawing and update logic here
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Example: handle game controls here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Example: pause game
                    game_state = PAUSE

    elif game_state == PAUSE:
        # Add pause menu or logic here if necessary
        print("Game is paused")
        game_state = PLAYING  # Or handle pause logic

if game_state == PLAYING:
    # Example: Pressing ESC pauses the game and returns to the menu
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_state = MENU

