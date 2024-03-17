import pygame
import sys
import random
import time
import menu as menu
import math

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = COIN_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.initial_y = y
        self.speed = speed
        self.angle = 0

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
            
        # Adjust vertical position using a sine wave
        self.rect.centery = self.initial_y + int(10 * math.sin(self.angle))  # Use the initial y-position
        self.angle += 0.1  # Adjust the frequency of the wave motion

        # Add more coins periodically
        if random.randint(0, 300) == 0:  # Adjust the probability as needed
            new_coin = Coin(random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 50), random.randint(0, SCREEN_HEIGHT), self.speed)
            coins.add(new_coin)
            all_sprites.add(new_coin)

    def collect(self):
        COIN_SOUND.play()  # Play the sound of collected coin
        return 1  # Value of the coin to add to the player's score
