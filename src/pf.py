import pygame

class Platform:
    def __init__(self, x, y, imagePath):
        self.x = x
        self.y = y
        self.is_drawn = False
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.rect.width


    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.is_drawn = True
        
    def move(self, worldShift):
        self.y += worldShift
        self.rect.y = self.y
    