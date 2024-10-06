import pygame

class Bullet:
    def __init__(self, imagePath, x, y):
        self.speed = 5
        self.velocity_y = -5
        
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (44, 88))
        self.rect = self.image.get_rect()
        
        # Set the initial position of the bullet
        self.rect.centerx = x
        self.rect.bottom = y
        
    def move(self):
        self.rect.y += self.velocity_y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)