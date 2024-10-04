import pygame
from player import Player
from pf import Platform
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRAVITY = 0.0

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

MAX_PLAYER_HEIGHT = SCREEN_HEIGHT / 4

PLATFORM_MIN_WIDTH = 100
PLATFORM_MAX_WIDTH = 200
PLATFORM_HEIGHT = 20

platforms = []
world_shift = 0

def generate_platforms():
    x = random.randInt(0, SCREEN_WIDTH)

def check_platform_collision():
    for platform in platforms:
        if (player.y == platform.rect.y and
            player.x > platform.rect.x and
            player.x < platform.rect.x + platform.rect.width):
            print("collision!")
            if player.velocity_y > 0:
        #collision with platform
                player.velocity_y = player.velocity_y - 2


    


# initialize pygame
pygame.init()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Rat Chase")

# clock is used to set a max fps
clock = pygame.time.Clock()

#Player in
player = Player('tile000.png')

# create a demo surface, and draw a red line diagonally across it
surface_size = (25, 45)
test_surface = pygame.Surface(surface_size)
test_surface.fill(WHITE)

GAME_FONT = pygame.font.Font(None, 30)

pygame.draw.aaline(test_surface, RED, (0, surface_size[1]), (surface_size[0], 0))

backgroundImage = pygame.image.load('tilesetOpenGameBackground.png')
backgroundImage = pygame.transform.scale(backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

text_surface = GAME_FONT.render(str(player.velocity_y), True, BLACK)
text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.blit(text_surface, dest=(10,10))

    
    check_platform_collision()

    platforms.append(Platform(300, 800, 'platform_image.png'))
    
    player.handleKeys()
    player.tick_gravity(GRAVITY)
    player.move()
    
    if player.rect.y < MAX_PLAYER_HEIGHT: # if above middle of screen
        world_shift += player.speed # Shift the world down by the speed
        player.rect.y = MAX_PLAYER_HEIGHT # Keep player at center until the world shift is reset at end of frame
    
    
    
    screen.blit(backgroundImage, (0,0))

    for platform in platforms:
        platform.rect.y += world_shift
        if platform.is_drawn == False:
            platform.draw(screen)

    player.draw(screen)
    text_surface = GAME_FONT.render(f'Velocity Y: {player.velocity_y:.2f}', True, WHITE)
    screen.blit(text_surface, (10, 10))

    

    
    pygame.display.flip()

    world_shift = 0
    clock.tick(60)

pygame.quit()