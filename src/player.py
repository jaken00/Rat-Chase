import pygame

class Player:
    def __init__(self, imagePath):
        self.x = 350
        self.y = 600
        self.velocity_y = 0
        self.velocity_x = 0
        self.speed = 5
        self.color = (255,0,255) 
        
        #rather than hard setting rect values, using rect vales for W+H as the image rect
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        
        #pygame.transform.scale_by()

    def tick_gravity(self, gravity):
        self.velocity_y += gravity
    
    def move(self):
        self.y += self.velocity_y
        self.rect.y = self.y
        
        self.x += self.velocity_x
        self.rect.x = self.x

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def handleKeys(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
        elif keys[pygame.K_UP]:
            self.velocity_y = -self.speed
        elif keys[pygame.K_DOWN]:
            self.velocity_y = +self.speed
        else:        
            self.velocity_x = 0