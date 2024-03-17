import pygame
import sys
import random


pygame.init()
pygame.mixer.init()

RES = (800, 600)
SCREEN = pygame.display.set_mode(RES)

BACKGROUND_IMAGE = pygame.image.load("image/jtpk.jpg")
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, RES)

FONT = pygame.font.SysFont('Corbel', 70)

class Button:
    
    def __init__(self, image_path, x, y, width, height, sound=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.original_image = self.image.copy()  # Copy of the original image to restore color
        self.is_hovered = False
        self.is_clicked = False
        self.sound = sound
        self.name = image_path
        self.is_chosen = False  # Add an attribute to track if the character is chosen

    def draw(self):
        if self.is_hovered:
            # Adjust transparency on hover
            self.image.set_alpha(128)
        elif self.is_chosen:
            self.image.set_alpha(128)  # Make the button transparent if chosen
        else:
            self.image = self.original_image.copy()  # Restore original image

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
                return True  # Return True if the button is clicked
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_clicked and self.rect.collidepoint(event.pos):
                self.is_clicked = False
            else:
                self.is_clicked = False
        return False  # Return False if the button is not clicked

START_SOUND = pygame.mixer.Sound("sound/neom.mp3")
START_MUSIC = pygame.mixer.music.load("sound/gg.mp3")
pygame.mixer.music.set_volume(0.)

START_BUTTON = Button("image/start2.png", 325, 250, 150, 50, sound=START_SOUND)
QUIT_BUTTON = Button("image/exit2.png", 325, 320, 150, 50)
CHARACTER_BUTTONS = [Button("image/charachter1.png", 120, 250, 150, 100),  # Add buttons for 4 characters here
                     Button("image/charachter2.png", 230, 250, 150, 100),
                     Button("image/charachter3.png", 450, 250, 100, 100),
                     Button("image/transformation.png", 550, 250, 100, 100)]

BUTTONS = [START_BUTTON, QUIT_BUTTON] + CHARACTER_BUTTONS

CLOCK = pygame.time.Clock()

pygame.mixer.music.play(-1)

def menu_1():
    MENU = True
    while MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            for button in BUTTONS:
                if button.handle_event(event):
                    if button.name == "image/start2.png":  # Start the game
                        pygame.mixer.music.load("sound/gg.mp3")
                        pygame.mixer.music.play(-1)
                        print("Start button clicked")
                        MENU = False  # Start the game
                    elif button.name == "image/exit2.png":
                        pygame.quit()
                        sys.exit()
                    elif button.name.startswith("charachter"):
                        chosen_character = button.name  # Update the chosen character
                        button.is_chosen = True  # Mark the chosen button
                        print("Character selection button clicked")
                        # Disable other character buttons
                        for char_button in CHARACTER_BUTTONS:
                            if char_button != button:
                                char_button.is_chosen = True
                            else:
                                char_button.is_chosen = False  # Make the chosen button not transparent

        SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

        for button in BUTTONS:
            button.draw()

        pygame.display.flip()

        CLOCK.tick(120)























 
