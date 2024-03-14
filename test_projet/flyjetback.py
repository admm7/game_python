import pygame
import sys

pygame.init()
pygame.mixer.init()

res = (800, 600)
screen = pygame.display.set_mode(res)

background_image = pygame.image.load("jtpk.jpg")
background_image = pygame.transform.scale(background_image, res)

font = pygame.font.SysFont('Corbel', 70)

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

    def draw(self):
        if self.is_hovered:
            # Modifier la transparence lors du survol
            self.image.set_alpha(128)
        else:
            self.image = self.original_image.copy()  # Restaurer l'image d'origine

        screen.blit(self.image, (self.rect.x, self.rect.y))

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

start_sound = pygame.mixer.Sound("neom.mp3")
start_music = pygame.mixer.music.load("gg.mp3")
pygame.mixer.music.set_volume(0.5)

start_button = Button("start2.png", 325, 250, 150, 50, sound=start_sound)
quit_button = Button("exit2.png", 325, 320, 150, 50)

buttons = [start_button, quit_button]

clock = pygame.time.Clock()

pygame.mixer.music.play(-1)

def menu_1():
    MENU = True
    while MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            for button in buttons:
                if button.handle_event(event):
                    if button.name == "start2.png":
                        pygame.mixer.music.load("gg.mp3")
                        pygame.mixer.music.play(-1)
                        print("Start button clicked")
                        MENU = False  # Modifier la valeur de MENU ici
                    elif button.name == "exit2.png":
                        pygame.quit()
                        sys.exit()

        screen.blit(background_image, (0, 0))

        for button in buttons:
            button.draw()

        pygame.display.flip()

        clock.tick(60)















 
