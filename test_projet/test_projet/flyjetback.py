import pygame
import sys

pygame.init()

pygame.mixer.init()

# Résolution de l'écran
res = (800, 600)

# Ouvre une fenêtre
screen = pygame.display.set_mode(res)

background_image = pygame.image.load("zap.png")
background_image = pygame.transform.scale(background_image, res)

# Couleurs
color_button_inactive = (0, 0, 0, 0)  # Couleur transparente pour l'état inactif
color_button_active = (100, 100, 100)  # Couleur pour l'état actif
color_button_hover = (170, 170, 170)
color_button_click = (50, 50, 50)
color_text = (255, 255, 255)
color_shadow = (30, 30, 30, 100)

font = pygame.font.SysFont('Corbel', 30)

class Button:
    def __init__(self, text, x, y, width, height, sound=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = font.render(text, True, color_text)
        self.is_hovered = False
        self.is_clicked = False
        self.is_active = False  # Ajout d'une variable pour suivre l'état actif/inactif
        self.shadow_offset = 5
        self.sound = sound

    def draw(self):
        shadow_rect = pygame.Rect(self.rect.x + self.shadow_offset, self.rect.y + self.shadow_offset,
                                  self.rect.width, self.rect.height)
        pygame.draw.rect(screen, color_shadow, shadow_rect)

        if self.is_active:  # Utilisation de la couleur active si le bouton est actif
            pygame.draw.rect(screen, color_button_active, self.rect)
        elif self.is_hovered:
            pygame.draw.rect(screen, color_button_hover, self.rect)
        else:
            pygame.draw.rect(screen, color_button_inactive, self.rect)

        screen.blit(self.text, (self.rect.x + self.rect.width // 2 - self.text.get_width() // 2,
                                self.rect.y + self.rect.height // 2 - self.text.get_height() // 2))

start_sound = pygame.mixer.Sound("neom.mp3")
start_music = pygame.mixer.music.load("gg.mp3")
pygame.mixer.music.set_volume(0.5)

start_button = Button("Press Space to Start", 250, 250, 300, 50, sound=start_sound)  # Modification ici
quit_button = Button("Quit", 325, 320, 150, 50)

buttons = [start_button, quit_button]

clock = pygame.time.Clock()

pygame.mixer.music.play(-1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            for button in buttons:
                if button.rect.collidepoint(event.pos) and not button.is_hovered:
                    button.is_hovered = True
                elif not button.rect.collidepoint(event.pos) and button.is_hovered:
                    button.is_hovered = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                if button.rect.collidepoint(event.pos):
                    button.is_clicked = True
                    if button.text.get_text() == "Press Space to Start":
                        pygame.mixer.music.load("start_music.mp3")
                        pygame.mixer.music.play(-1)
                    elif button.sound:
                        button.sound.play()

        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                if button.rect.collidepoint(event.pos) and button.is_clicked:
                    if button.text.get_text() == "Press Space to Start":
                        print("Start button clicked")
                    elif button.text.get_text() == "Quit":
                        pygame.quit()
                        sys.exit()
                    button.is_clicked = False

        if event.type == pygame.KEYDOWN:  # Vérifie si une touche est enfoncée
            if event.key == pygame.K_SPACE:  # Vérifie si la touche enfoncée est l'espace
                if start_button.is_active:  # Si le bouton "Start" est actif
                    print("Start button clicked")
                    # Ajoutez ici le code pour lancer le jeu

    screen.blit(background_image, (0, 0))

    for button in buttons:
        button.draw()

    pygame.display.flip()

    clock.tick(60)






 
