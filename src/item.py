import pygame

class Item:
    def __init__(self, x, y, type, imagePath):
        self.x = x
        self.y = y
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.rect.width
        self.type = type


    def draw(self, screen):
        screen.blit(self.image, self.rect)

            
    def move(self, worldShift):
        self.y += worldShift
        self.rect.y = self.y
    