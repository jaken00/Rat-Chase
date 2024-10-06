import pygame
from player import Player
from pf import Platform
import random
from tool import Tool
from enemy import Enemy
from item import Item
from scenebuilder import SceneBuilder
import sys
import os
from bullet import Bullet

#pyinstaller main.spec to reload EXE

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# CONSTANTS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GRAVITY = 0.1

PLATFORM_PATH = resource_path('assets/platform2_image.png')
SMALL_PLATFORM_PATH = resource_path('assets/small_platform_image.png')
MEDIUM_PLATFORM_PATH = resource_path('assets/medium_platform_image.png')
MOUSE_PATH = resource_path('assets/rat.png')
KITTY_PATH = resource_path('assets/flyingkitty.png')
BG_PATH = resource_path('assets/tilesetOpenGameBackground.png')
BG2_PATH = resource_path('assets/bg3.png')
BG3_PATH = resource_path('assets/bg2.png')
ROCKET_TOOL_PATH = resource_path('assets/rocket_boost_button.png')
CHEESE_ITEM_PATH = resource_path('assets/cheese.png')
SOUND_ITEM_PATH = resource_path('assets/boing.wav')
MENU_BACKGROUND_IMAGE = resource_path('assets/menu_background.png')
MENU_PLAY_BUTTON = resource_path('assets/play_button.png')
MAIN_MENU_BUTTON = resource_path('assets/main_menu_button.png')
BG_DEAD_PATH = resource_path('assets/bgdead.png')
DEAD_WINDOW_PATH = resource_path('assets/dead_window.png')
BULLET_IMAGE_PATH = resource_path('assets/bullet.png')
OST1_SONG = resource_path('assets/ost1.wav')
SOUND_JUMP_PATH = resource_path('assets/jump.wav')


menuScene = SceneBuilder(MENU_BACKGROUND_IMAGE)
gameScene = SceneBuilder(BG2_PATH)
deadScene = SceneBuilder(BG_DEAD_PATH)
currentScene = menuScene

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 900

MAX_PLAYER_HEIGHT = SCREEN_HEIGHT / 4

PLATFORM_MIN_WIDTH = 100
PLATFORM_MAX_WIDTH = 200
PLATFORM_HEIGHT = 20

maxCatCount = 2

#ARRAY INITS
platforms = []
items = []
cheese_collected = 0
bullet_count = 0
currentEnemies = []
bullets = []

#ENEMY COLLISION CHECK
def checkEnemyCollision():
    for enemy in currentEnemies:
        if player.rect.colliderect(enemy.rect):
            print("Collision with enemy!")
            return True
    return False

#ENEMY GENERATION
def generateEnemies():
    if(len(currentEnemies) < maxCatCount):
        if world_shift > 1.5:
            currentEnemies.append(Enemy(KITTY_PATH, -50, -200)) #Normalized Spawn for when below 2 speed 
        else:
            currentEnemies.append(Enemy(KITTY_PATH, -200, -400)) #Makes spawn higher

def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
        return image
    except pygame.error as e:
        print("ERROR LOADING IMAGE")
        sys.exit



def generate_platforms():
    if(len(platforms) < 7):
        
        last_platform = platforms[-1]
        
        last_platform_x = last_platform.rect.x
        last_platform_y = last_platform.rect.y
        
        x = random.uniform(SCREEN_WIDTH - 700, (SCREEN_WIDTH - 200)) 
        y = random.uniform((last_platform_y - 50), (last_platform_y - 200))
        rand = random.randint(0,100)
        if(rand > 90):
            platforms.append(Platform(x,y,SMALL_PLATFORM_PATH))
        elif(rand < 20):
            platforms.append(Platform(x,y,MEDIUM_PLATFORM_PATH))
        elif(rand > 20) and (rand < 30):
             moving_platform = Platform(x,y,SMALL_PLATFORM_PATH)
             moving_platform.moving = True
             moving_platform.speed = 1 
             platforms.append(moving_platform)
             print("spawned moving platform!")
        else:
            platforms.append(Platform(x,y,PLATFORM_PATH))

        
def generate_items():
    
    while len(items) < 1:
        last_platform = platforms[-1]
        last_platform_x = last_platform.rect.x
        last_platform_y = last_platform.rect.y
        
        x = random.uniform(last_platform_x, last_platform_x + last_platform.rect.width)
        y = random.uniform((last_platform_y - 50), (last_platform_y - 200))

        items.append(Item(x,y,"cheese",CHEESE_ITEM_PATH))

    

def check_platform_collision():
    for platform in platforms:
        if ((player.y + 60) >= platform.rect.y - platform.rect.height and
            (player.y + 60) <= platform.rect.y - platform.rect.height + 15):
                if ((player.x > platform.rect.x and player.x < platform.rect.x + platform.rect.width) or
                    ((player.x + 90)> platform.rect.x and (player.x + 90) < platform.rect.x + platform.rect.width)):
                    if player.velocity_y > 0:
                        pygame.mixer.Sound.play(jump)
                        player.y - 5
                        player.velocity_y = -5

def check_item_collision():
    global score
    global bullet_count
    for i in range(0,len(items)):
        if player.rect.colliderect(items[i].rect):
            if items[i].type == "cheese":
                items.pop(i)
                score += 200
                bullet_count += 1
                print(f'Bullet Count: {bullet_count}')
                pygame.mixer.Sound.play(item_get_sound)
                
def check_bullet_collision():
    for enemy in currentEnemies:
        for bullet in bullets:
            if bullet.rect.colliderect(enemy.rect):
                print("Collision detected!")
                bullets.remove(bullet)  
                currentEnemies.remove(enemy)  
                break  

world_shift = 0

# initialize pygame
pygame.init()
start_time = pygame.time.get_ticks()

#initialize audio mixer and audio files
pygame.mixer.init()
item_get_sound = pygame.mixer.Sound(SOUND_ITEM_PATH)
ost1 = pygame.mixer.music.load(OST1_SONG)
jump = pygame.mixer.Sound(SOUND_JUMP_PATH)

pygame.mixer.music.play(-1)

screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)

# create a window
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Rat Chase")

# clock is used to set a max fps
clock = pygame.time.Clock()

#Player in
player = Player(MOUSE_PATH)

#Item toolbar in
slot_count = 3
slot_width = 60
slot_height = 90
slot_margin = 10
toolbar_x, toolbar_y = 20, 20
toolbar = []

highscore = 0

GAME_FONT = pygame.font.Font(None, 30)
backgroundImage = pygame.image.load(BG2_PATH)
backgroundImage = pygame.transform.scale(backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))

menu_background = load_image(MENU_BACKGROUND_IMAGE)

dead_background = load_image(BG_DEAD_PATH)
dead_background = pygame.transform.scale(dead_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

play_button = pygame.image.load(MENU_PLAY_BUTTON)
play_button_rect = play_button.get_rect()
play_button_rect.x, play_button_rect.y, = 214,600

main_menu_button = pygame.image.load(MAIN_MENU_BUTTON)
main_menu_button_rect = main_menu_button.get_rect(center = (SCREEN_WIDTH // 2, 530))

dead_window = pygame.image.load(DEAD_WINDOW_PATH)
dead_window_rect = dead_window.get_rect()
dead_window_rect.x, dead_window_rect.y = 50,200

last_cat_spawn_time = 0
cat_spawn_interval = 15000
space_pressed = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    if currentScene == menuScene:
        
        author_text_surface = GAME_FONT.render('Created by Zan D and Jacob N', True, BLACK)

        screen.blit(menu_background, (0,0))
        screen.blit(play_button, (214,600))
        screen.blit(author_text_surface, (170, 700))
        pygame.display.flip()
        mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if play_button_rect.collidepoint(mouse_position):
                # reset map
                score = 0
                elapsed_time = 0
                minutes = 0
                seconds = 0
                bullet_count = 0
                start_time = pygame.time.get_ticks()
                player.rect.x = 350
                player.x = 350
                player.rect.y = 500
                player.y = 500
                maxCatCount = 2
                platforms = []
                platforms.append(Platform(300, 700, PLATFORM_PATH))
                items = []
                currentEnemies = []
                currentScene = gameScene
        #DRAW BUTTONS
    elif currentScene == deadScene:
        mouse_position = pygame.mouse.get_pos()
        dscore_surface = GAME_FONT.render(f'Score : {score}', True, WHITE)
        dtime_surface = GAME_FONT.render(f'Time survived: {minutes}:{seconds:02d}', True, WHITE)
        dscore_surface_rect = dscore_surface.get_rect(center = (SCREEN_WIDTH // 2, 430))
        dtime_surface_rect = dtime_surface.get_rect(center = (SCREEN_WIDTH // 2, 470))
        screen.blit(dead_background, (0,0))
        screen.blit(dead_window, (50,200))
        screen.blit(main_menu_button, main_menu_button_rect)
        screen.blit(dscore_surface, dscore_surface_rect)
        screen.blit(dtime_surface, dtime_surface_rect)
        pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if main_menu_button_rect.collidepoint(mouse_position):
                print("COLLIDE WORKING")
                currentScene = menuScene

    elif currentScene == gameScene:
        generate_platforms()
        generateEnemies()
        generate_items()
        check_platform_collision()
        check_item_collision()
        check_bullet_collision()
        
        if keys[pygame.K_SPACE]:
            if not space_pressed and bullet_count > 0:
                print("BULLET SHOOT")
                bullet_count -= 1
                bullet = Bullet(BULLET_IMAGE_PATH, player.x, player.y)
                bullets.append(bullet)
                space_pressed = True
            
        else:
            space_pressed = False
            
        player.handleKeys()
        player.tick_gravity(GRAVITY)
        player.move()
        
        #Scoring 
        if player.velocity_y < 0:
            score += round(player.velocity_y * -1)
        
        #PLAYER DEATH

        if(player.rect.y > 900):
            lastScore = score
            if lastScore > highscore:
                highscore = lastScore
            currentScene = deadScene
        
        if checkEnemyCollision():
            currentScene = deadScene
        #velocity x = 0
        
        #screen side teleport
        if player.rect.x > SCREEN_WIDTH + (player.rect.width / 2):
            player.rect.x = 0 - (player.rect.width / 2)
            player.x = 0 - (player.rect.width / 2)
            
        if player.rect.x < 0 - (player.rect.width / 2):
            player.rect.x = SCREEN_WIDTH - (player.rect.width / 2)
            player.x = SCREEN_WIDTH - (player.rect.width / 2)
            
        screen.blit(backgroundImage, (0,0))

        if player.rect.y < SCREEN_HEIGHT / 2:
            world_shift = 2
        else:
            world_shift = 1.5

        #world shifting
        for platform in platforms:
            platform.move(world_shift) 
        for item in items:
            item.move(world_shift)
        for bullet in bullets:
            bullet.move()
        
        #x-moving platforms
        for platform in platforms:
            if(platform.moving == True):
                platform.move_x(platform.speed)
                if platform.rect.x > SCREEN_WIDTH - platform.rect.width:
                    platform.speed = -1
                elif platform.rect.x < 0 + platform.rect.width:
                    platform.speed = 1

        platforms = [platform for platform in platforms if platform.rect.y < SCREEN_HEIGHT]
        bullets = [bullet for bullet in bullets if bullet.rect.y > 0]
        items = [item for item in items if item.rect.y < SCREEN_HEIGHT]
        currentEnemies = [enemy for enemy in currentEnemies if enemy.rect.y < SCREEN_HEIGHT]
        
        for bullet in bullets:
            bullet.draw(screen)
        
        
        for platform in platforms:
            platform.draw(screen)

        for item in items:
            item.draw(screen)
        
        for tool in toolbar:
            tool.draw(screen)

        for enemy in currentEnemies:
            enemy.draw(screen)
            enemy.tick_gravity(GRAVITY)
            enemy.move()
            
        
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        currentTime = pygame.time.get_ticks()
        
        if minutes > 0:
            world_shift += (minutes * 0.5) 
        if world_shift > 5:
            world_shift = 5 
        
        if currentTime - last_cat_spawn_time > cat_spawn_interval:
            print("adding cat!")
            maxCatCount += 1
            last_cat_spawn_time = currentTime
        
        
        player.draw(screen)
        score_surface = GAME_FONT.render(f'Score : {score}', True, WHITE)
        ammo_surface = GAME_FONT.render(f'Ammo : {bullet_count}, (Hit space to Shoot!)', True, WHITE)
        highscore_surface = GAME_FONT.render(f'High Score : {highscore}', True, WHITE)
        time_surface = GAME_FONT.render(f'Play Time: {minutes}:{seconds:02d}', True, WHITE)
        
        screen.blit(score_surface, (400, 10))
        screen.blit(highscore_surface, (400, 50))
        screen.blit(time_surface, (400, 90))
        screen.blit(ammo_surface, (10, 10))

        pygame.display.flip()

        clock.tick(60)


pygame.quit()