import pygame
import sys
import random
import time
import menu as menu

LASER_IMAGE = pygame.image.load("image/zap.png")
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (50, 120))

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = LASER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
