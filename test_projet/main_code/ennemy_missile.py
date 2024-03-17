import pygame
import sys
import random
import time
import menu as menu

MISSILE_IMAGE = pygame.image.load("image/missile2.png")
MISSILE_IMAGE = pygame.transform.scale(MISSILE_IMAGE, (30, 15))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = MISSILE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x += self.speed  # Les missiles se déplacent vers l'arrière
        if self.rect.right <= 0 or self.rect.left >= SCREEN_WIDTH:
            self.kill()
