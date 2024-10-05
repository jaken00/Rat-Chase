
import pygame

# Maybe make a base Entity class? Rather than having two seperate player and enemy classes?? 

class Enemy:
    def __init__(self, imagePath) -> None:
        self.x = -10 # need to be dynamically created at top of screen // Maybe have it start at -10 to build velocity??
        self.y = 600 # need to be dynamically created at top of screen
        self.velocity_y = 0
        self.velocity_x = 0
        self.speed = 5
        self.color = (255,0,255) 
        
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        
        def tick_gravity(self, gravity):
            self.velocity_y += gravity