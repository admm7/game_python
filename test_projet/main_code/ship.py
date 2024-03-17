import pygame
import sys
import random
import time
import menu as menu

SHIP_IMAGE = pygame.image.load("image/ufo2.png")
SHIP_IMAGE = pygame.transform.scale(SHIP_IMAGE, (80, 80))
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.original_image = SHIP_IMAGE
        self.image = pygame.transform.scale(self.original_image, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed
        self.attack_cooldown = 0
        self.direction = 1

    def update(self,Rocket,rockets,all_sprites):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
        self.rect.y += self.speed * self.direction  # Déplacement vertical
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.direction *= -1  # Inverser la direction si le vaisseau atteint le haut ou le bas de l'écran
        self.attack_cooldown += 1
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 100
            new_rocket = Rocket(self.rect.centerx, self.rect.centery, -2 * self.direction)  # Vitesse et direction de la roquette
            rockets.add(new_rocket)
            all_sprites.add(new_rocket)
