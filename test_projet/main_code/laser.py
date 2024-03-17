import pygame
import sys
import random
import time
import menu as menu

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, ):
        super().__init__()
        self.image = pygame.image.load("image/zap.png")
        self.image = pygame.transform.scale(self.image, (50, 120))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
