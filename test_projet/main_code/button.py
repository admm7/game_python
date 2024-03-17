import pygame
import sys
import random
import time
import menu as menu

class Button:
    def __init__(self, image_path, x, y, width, height, sound=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.original_image = self.image.copy()  # Copie de l'image d'origine pour restaurer la couleur
        self.is_hovered = False
        self.is_clicked = False
        self.sound = sound
        self.name = image_path
        self.is_chosen = False  # Ajouter un attribut pour suivre si le personnage est choisi

    def draw(self):
        if self.is_hovered:
            # Modifier la transparence lors du survol
            self.image.set_alpha(128)
        elif self.is_chosen:
            self.image.set_alpha(128)  # Rendre le bouton transparent s'il est choisi
        else:
            self.image = self.original_image.copy()  # Restaurer l'image d'origine

        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
            else:
                self.is_hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_clicked = True
                if self.sound:
                    self.sound.play()
                return True  # Renvoyer True si le bouton a été cliqué
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_clicked and self.rect.collidepoint(event.pos):
                self.is_clicked = False
            else:
                self.is_clicked = False
        return False  # Renvoyer False si le bouton n'a pas été cliqué
