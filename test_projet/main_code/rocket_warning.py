import pygame
import sys
import random
import time
import menu as menu

ROCKET_WARNING_IMAGE = pygame.image.load("image/avert.png")
ROCKET_WARNING_IMAGE = pygame.transform.scale(ROCKET_WARNING_IMAGE, (30, 30))
ROCKET_IMAGE = pygame.image.load("image/rocket.png")
ROCKET_IMAGE = pygame.transform.scale(ROCKET_IMAGE, (50, 20))

class RocketWarning(pygame.sprite.Sprite):
    def __init__(self, x, y,ROCKET_WARNING_IMAGE):
        super().__init__()
        self.image = ROCKET_WARNING_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self,missiles):
         # Check for collisions between RocketWarning and missiles
        missile_collisions = pygame.sprite.spritecollide(self, missiles, True)
        if missile_collisions:
            self.kill()  # Remove the RocketWarning sprite if it collides with a missile
