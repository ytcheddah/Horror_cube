import pygame
from main import *
import math
from settings import *
from cl_trap import *

pygame.init()

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
        
        self.show_mask = False
        self.mask = pygame.mask.from_surface(self.image)

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

        # Sprint logic
        if keys[pygame.K_LSHIFT] and not self.in_sprint_cooldown and not self.is_crouching:
            self.start_sprint()
        elif self.is_sprinting and not keys[pygame.K_LSHIFT]:
            self.stop_sprint()

        # Crouch logic
        if keys[pygame.K_LCTRL]:
            self.start_crouch()
        else:
            self.stop_crouch()

        # Handle spacebar to place trap
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.lastTrapTime >= self.trapCooldown:
                self.create_trap()
                self.lastTrapTime = current_time # Update the last trap to correct time    

    def start_sprint(self):

        if not self.is_sprinting and not self.in_sprint_cooldown:
            self.is_sprinting = True
            self.sprint_timer_start = pygame.time.get_ticks()
            self.speed = self.base_speed * 1.5
            self.sprint_factor = 2

    def stop_sprint(self):

        if self.is_sprinting:
            self.is_sprinting = False
            self.in_sprint_cooldown = True
            self.cooldown_timer_start = pygame.time.get_ticks()
            self.speed = self.base_speed  # Reset speed

    def start_crouch(self):

        if not self.is_crouching:
            self.is_crouching = True
            self.speed = self.base_speed * 0.6
            self.sprint_factor = 0.5
            # Stop sprinting if crouching
            if self.is_sprinting:
                self.speed = self.base_speed * 0.6
                self.stop_sprint()
                print('stop sprint')

    def stop_crouch(self):

        if self.is_crouching:
            self.is_crouching = False
            self.speed = self.base_speed  # Reset speed

    def update_cooldown(self):

        global sprint_factor
        # Handle sprint cooldown
        if self.is_sprinting:
            if pygame.time.get_ticks() - self.sprint_timer_start > self.sprint_duration:
                self.stop_sprint()

        # Handle cooldown duration
        if self.in_sprint_cooldown:
            if pygame.time.get_ticks() - self.cooldown_timer_start >= self.sprint_cooldown:
                self.in_sprint_cooldown = False  # Exit cooldown
                self.sprint_factor = 1  # Reset sprint factor

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
            trap.rect.x += -self.velocity_x
            trap.rect.y += -self.velocity_y

    def create_trap(self, player, trap_list):
        # Create a new "trap" (circle) under the player
        trap_x = (self.rect.x)  # center the circle horizontally
        trap_y = (self.rect.y) - 50 # place trap under player
        new_trap = Trap(player,trap_x,trap_y, trap_list[0]) # add more logic when new traps are made
        self.inventoryTraps.append(new_trap)

    def draw(self, screen, bg):
        global walkCount
        
        # layer stack
        screen.fill(WHITE) # init fill
        screen.blit(bg, self.bg_pos) # map
        # screen.blit(self.darkness_surf, (0, 0)) # darkness_surf
        # pygame.draw.rect(self.darkness_surf, (RED), self.darkness_rect.topleft)
       
        # pygame.draw.rect(screen, 'pink', self.rect)
        screen.blit(self.light_surf, (0, 0))
        pygame.draw.circle(self.light_surf, (0, 0, 0, self.light_power), self.rect.center, self.light_radius)

        # Draw Player
        if not self.show_mask:              
            screen.blit(self.image, ((self.rect.centerx - self.player_width , self.rect.centery - self.player_height)))
        else:
            screen.blit(self.mask.to_surface(unsetcolor=(0,0,0,0), setcolor=(155,255,255,255)), ((self.rect.centerx - self.player_width , self.rect.centery - self.player_height)))
                            
        # Draw Traps
        for trap in self.inventoryTraps:
            
            if not self.show_mask:
                trap.draw(screen)
            else:
                screen.blit(trap.mask.to_surface(unsetcolor=(0,0,0,0),
                     setcolor=(155,145,220,255)), (self.rect.x + 75, self.rect.y + 100))
                print('working')

    def update(self):
        self.user_input()
        self.update_cooldown()
        self.move()
        # Updates traps and remove any that have expired
        self.inventoryTraps = [trap for trap in self.inventoryTraps if trap.update()]
