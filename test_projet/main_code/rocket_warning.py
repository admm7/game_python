import pygame
import sys
import random
import time
import menu as menu

class RocketWarning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ROCKET_WARNING_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
         # Check for collisions between RocketWarning and missiles
        missile_collisions = pygame.sprite.spritecollide(self, missiles, True)
        if missile_collisions:
            self.kill()  # Remove the RocketWarning sprite if it collides with a missile
