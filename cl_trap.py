import pygame
from main import *

class Trap:

    def __init__(self, player, x, y, image, radius=20, duration=15000):
        self.player = player
        self.x = x
        self.y = y
        self.width = image.get_width()
        self.height = image.get_height()
        self.radius = radius
        self.image = image
        self.creation_time = pygame.time.get_ticks() # Correct reference to pygame.time.get_ticks
        self.duration = duration
        self.rect = self.image.get_rect(center = (x + (self.width/2) + 75, y + (self.height/2) + 150))

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        # Check if the trap has expired (lifetime is over)
        if pygame.time.get_ticks() - self.creation_time > self.duration:
            return False
        
        return True
    
    def draw(self, screen):
        # pygame.draw.circle(screen, 'pink', (self.x + 100, self.y + 200), self.radius) # needs to be relative to the map
        if not self.player.show_mask:
            pygame.draw.rect(screen, 'pink', self.rect, width=self.width)
            screen.blit(self.image, (self.x + 75, self.y + 150))
        else:
            screen.blit(self.mask.to_surface(unsetcolor=(0,0,0,0),
                  setcolor=(155,145,220,255)), (self.x + 75, self.y + 150))
            print('working')
