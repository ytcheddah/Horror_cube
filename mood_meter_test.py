import pygame
import sys
import math
from settings import *

# initialize pygame
pygame.init()

# Constants imported from settings
BAR_OUTLINE_WIDTH = 500
BAR_OUTLINE_HEIGHT = 25
BAR_WIDTH = 488
BAR_HEIGHT = 15
BAR_X = 250
BAR_Y = 250
YELLOW = (255, 255, 0)

# space bar to increase rate of percentage decay
# class Player():
    
#     def __init__(self):
#         self = True


#     def user_input(self):
        

#         keys = pygame.key.get_pressed()


#         if keys[pygame.K_space]:
#             percentage_decay = 0.05

            

# colors imported from settings

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Psyche Bar")

# function to draw the psyche bar
def draw_psyche_bar(percentage):
    # calculate the width of the inner bar
    inner_bar_width = int(BAR_WIDTH *(percentage / 100))

    # determine the color of the bar based on the percentage
    if percentage > 67:
        color = GREEN
    elif 33 <= percentage <= 67:
        color = YELLOW
    else:
        color = RED
    

    # draw the black outline
    pygame.draw.rect(screen, BLACK, (BAR_X, BAR_Y, BAR_OUTLINE_WIDTH, BAR_OUTLINE_HEIGHT))


    # draw the inner bar
    pygame.draw.rect(screen, color, ((BAR_X + 6), (BAR_Y + 5), inner_bar_width, BAR_HEIGHT))


# main loop
percentage = 100
clock = pygame.time.Clock()


percentage_decay = .01


while True:
    keys = pygame.key.get_pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # if event.type == pygame.KEYDOWN:
        #     Player.user_input()

    #gradually decrease the percentage
    percentage -= percentage_decay
    if percentage < 0:
        pygame.quit()
        sys.exit()

    # clear the screen
    screen.fill((255, 255, 255))

    # draw the psyche bar
    draw_psyche_bar(percentage)

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)




    