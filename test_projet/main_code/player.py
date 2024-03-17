import pygame
import sys
import random
import time
import menu as menu

class Player(pygame.sprite.Sprite):
    def __init__(self, selected_character="image/player.png"):
        super().__init__()
        self.selected_character = selected_character
        self.images = [CHARACTER3, ELECTROCUTED_IMAGE, PLAYER_AFTER_ELECTROCUTED]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = SCREEN_HEIGHT // 2
        self.gravity = 1
        self.score = 0
        self.attack_cooldown = 0
        self.electrocuted = False
        self.electrocuted_start_time = 0
        self.velocity_y = 0




    def update(self):
        if not self.electrocuted:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.rect.y -= 5
            elif keys[pygame.K_z] and self.attack_cooldown <= 0:
                self.attack_cooldown = 10
                new_missile = Missile(self.rect.centerx, self.rect.centery, 5)  # Les missiles sont tirés vers l'avant
                missiles.add(new_missile)
                all_sprites.add(new_missile)
                MISSILE_SOUND.play()  # Jouer le son du missile
            elif keys[pygame.K_DOWN] and self.attack_cooldown <= 0:
                self.attack_cooldown = 30
                new_missile = Missile(self.rect.centerx, self.rect.bottom, 5)  
                missiles.add(new_missile)
                all_sprites.add(new_missile)
                MISSILE_SOUND.play()  # Jouer le son du missile
            elif keys[pygame.K_UP]:  # Nouvelle condition pour déplacer le joueur vers le haut
                self.rect.y -= 5
            else:
                self.rect.y += self.gravity
                self.gravity += 0.2
                if self.gravity > 5:
                    self.gravity = 5
            self.attack_cooldown -= 1
        else:
            # Animation d'électrocution pendant 1 seconde
            if time.time() - self.electrocuted_start_time >= 1:
                self.electrocuted = False
                self.image = PLAYER_AFTER_ELECTROCUTED

        # Ajout des vérifications pour empêcher le joueur de sortir de l'écran verticalement
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
        elif self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0
            
        

    # Méthode pour déclencher l'animation d'électrocution
    def electrocute(self):
        if not self.electrocuted:
            self.electrocuted = True
            self.electrocuted_start_time = time.time()
            self.index = 1  # Indice de l'image d'électrocution
            self.image = self.images[self.index]  # Afficher l'image d'électrocution

    # Méthode pour incrémenter le score lors de la collecte de pièces
    def collect_coin(self):
        self.score += 1