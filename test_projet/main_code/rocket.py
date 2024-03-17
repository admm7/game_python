import pygame
# Classe pour les roquettes

ROCKET_IMAGE = pygame.image.load("image/rocket.png")
ROCKET_IMAGE = pygame.transform.scale(ROCKET_IMAGE, (50, 20))

class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = ROCKET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()