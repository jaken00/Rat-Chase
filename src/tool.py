import pygame

class Tool:
    def __init__(self, x, y, name, imagePath):
        self.x = x
        self.y = y
        self.name = name
        self.image = pygame.image.load(imagePath)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.rect.width
        self.equipped = False


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def pickup(self):
        self.equipped = True

    def use(self):
        self.equipped = False