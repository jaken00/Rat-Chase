import pygame
from player import Player
from pf import Platform
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRAVITY = 0.1

score = 0

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

MAX_PLAYER_HEIGHT = SCREEN_HEIGHT / 4




PLATFORM_MIN_WIDTH = 100
PLATFORM_MAX_WIDTH = 200
PLATFORM_HEIGHT = 20

platforms = [
]


platforms.append(Platform(300, 800, 'lundumGame/platform_image.png'))
platforms.append(Platform(0, 700, 'lundumGame/platform_image.png'))
platforms.append(Platform(150, 600, 'lundumGame/platform_image.png'))
platforms.append(Platform(300, 500, 'lundumGame/platform_image.png'))
platforms.append(Platform(400, 400, 'lundumGame/platform_image.png'))
platforms.append(Platform(200, 375, 'lundumGame/platform_image.png'))
platforms.append(Platform(200, 300, 'lundumGame/platform_image.png'))
platforms.append(Platform(200, 200, 'lundumGame/platform_image.png'))
platforms.append(Platform(200, 100, 'lundumGame/platform_image.png'))

world_shift = 0

def generate_platforms():
    if(len(platforms) < 7):
        x = random.uniform(100, (SCREEN_WIDTH - 100))
        y = random.uniform((player.y - 100), (player.y - 50))
        platforms.append(Platform(x,y,'lundumGame/platform_image.png'))
    

def check_platform_collision():
    for platform in platforms:
        if ((player.y + 60) >= platform.rect.y - platform.rect.height and
            (player.y + 60) <= platform.rect.y - platform.rect.height + 15):
                if ((player.x > platform.rect.x and player.x < platform.rect.x + platform.rect.width) or
                    ((player.x + 90)> platform.rect.x and (player.x + 90) < platform.rect.x + platform.rect.width)):
                    if player.velocity_y > 0:
                            #print("collision!")
                        #collision with platform
                        player.y - 5
                        player.velocity_y = -5


    


# initialize pygame
pygame.init()
screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Rat Chase")

# clock is used to set a max fps
clock = pygame.time.Clock()

#Player in
player = Player('lundumGame/tile000.png')

# create a demo surface, and draw a red line diagonally across it
surface_size = (25, 45)
test_surface = pygame.Surface(surface_size)
test_surface.fill(WHITE)

GAME_FONT = pygame.font.Font(None, 30)

pygame.draw.aaline(test_surface, RED, (0, surface_size[1]), (surface_size[0], 0))

backgroundImage = pygame.image.load('lundumGame/tilesetOpenGameBackground.png')
backgroundImage = pygame.transform.scale(backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    
    check_platform_collision()
    generate_platforms()
    
    #print(platforms[1].y)
    #print(len(platforms))
    
    player.handleKeys()
    player.tick_gravity(GRAVITY)
    player.move()
    
    world_shift += 1.5 # Shift the world down by the speed
    #player.rect.y = MAX_PLAYER_HEIGHT # Keep player at center until the world shift is reset at end of frame

    if player.velocity_y < 0:
        score += round(player.velocity_y * -1)
    
    screen.blit(backgroundImage, (0,0))

    for platform in platforms:
        platform.move(world_shift) 

    platforms = [platform for platform in platforms if platform.rect.y < SCREEN_HEIGHT]
    
    for platform in platforms:
        platform.draw(screen)
        
    
    player.draw(screen)
    text_surface = GAME_FONT.render(f'Velocity Y: {player.velocity_y:.2f}', True, WHITE)
    text_surface2 = GAME_FONT.render(f'World Shift : {world_shift}', True, WHITE)
    text_surface3 = GAME_FONT.render(f'Platform Count : {len(platforms)}', True, WHITE)
    score_surface = GAME_FONT.render(f'Score : {score}', True, WHITE)
    screen.blit(text_surface, (10, 10))
    screen.blit(text_surface2, (10, 50))
    screen.blit(text_surface3, (10, 90))
    screen.blit(score_surface, (400, 10))

    

    pygame.display.flip()

    world_shift = 0
    clock.tick(60)

pygame.quit()