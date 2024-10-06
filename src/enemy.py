
import pygame
import random

# Maybe make a base Entity class? Rather than having two seperate player and enemy classes?? 

class Enemy:
    def __init__(self, imagePath) -> None:
        self.x = random.uniform(0, 900) # need to be dynamically created at top of screen // Maybe have it start at -10 to build velocity??
        self.y =  random.uniform(-50, -200) # need to be dynamically created at top of screen
        self.velocity_y = 0
        self.velocity_x = 0
        self.speed = 5
        self.color = (255,0,255) 
        
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (27, 48))
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x  
        self.rect.y = self.y
        
    def tick_gravity(self, gravity):
            self.velocity_y += gravity
            
    def move(self):
            self.y += self.velocity_y
            self.rect.y = self.y
        
    def draw(self, screen):
            screen.blit(self.image, self.rect)