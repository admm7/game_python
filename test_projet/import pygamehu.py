import pygame
import sys
import random
import time

# Initialisation de Pygame
pygame.init()

# Paramètres de l'écran
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jetpack Joyride")

# Chargement des images de fond
background_images = ["back.jpg", "ocean.png"]
current_background_index = 0
background_image = pygame.image.load(background_images[current_background_index])
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Chargement des images des sprites
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (100, 100))
missile_image = pygame.image.load("missile.png")
missile_image = pygame.transform.scale(missile_image, (30, 15))
rocket_warning_image = pygame.image.load("avert.png")
rocket_warning_image = pygame.transform.scale(rocket_warning_image, (30, 30))
rocket_image = pygame.image.load("rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (50, 20))
laser_image = pygame.image.load("zap.png")
laser_image2 = pygame.image.load("zap2.png")
laser_image = pygame.transform.scale(laser_image, (20, 80))  # Redimensionner si nécessaire
laser_image2 = pygame.transform.scale(laser_image2, (20, 80))
electrocuted_image = pygame.image.load("electrocuted.png")
electrocuted_image = pygame.transform.scale(electrocuted_image, (100, 100))  # Redimensionner si nécessaire

# Classe pour le joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.centery = screen_height // 2
        self.gravity = 1
        self.score = 0
        self.attack_cooldown = 0
        self.electrocuted = False  # Nouvelle variable pour suivre l'état d'électrocution du joueur
        self.electrocuted_start_time = 0  # Variable pour enregistrer le début de l'électrocution

    def update(self):
        if not self.electrocuted:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.rect.y -= 5
            elif keys[pygame.K_DOWN] and self.attack_cooldown <= 0:
                self.attack_cooldown = 30
                new_missile = Missile(self.rect.centerx, self.rect.bottom + 5, -5)
                missiles.add(new_missile)
                all_sprites.add(new_missile)
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
                self.image = player_image

    # Méthode pour déclencher l'animation d'électrocution
    def electrocute(self):
        if not self.electrocuted:
            self.electrocuted = True
            self.electrocuted_start_time = time.time()
            self.image = electrocuted_image  # Afficher l'image d'électrocution

# Classe pour les roquettes
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = rocket_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()

# Classe pour les missiles
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.right <= 0 or self.rect.left >= screen_width:
            self.kill()

# Classe pour les avertissements de roquettes
class RocketWarning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = rocket_warning_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        pass  # Les avertissements ne nécessitent pas de mise à jour

# Groupe de sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Groupe de missiles
missiles = pygame.sprite.Group()

# Groupe de roquettes
rockets = pygame.sprite.Group()

# Groupe d'avertissements de roquettes
rocket_warnings = pygame.sprite.Group()

clock = pygame.time.Clock()

# Timer pour changer le fond d'arrière-plan
background_change_timer = 0
background_change_interval = 3000   # en millisecondes

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Mise à jour des sprites
    all_sprites.update()

    # Génération aléatoire des missiles
    if random.randint(0, 100) < 1:
        new_missile = Missile(screen_width, random.randint(0, screen_height - 10), 3)
        missiles.add(new_missile)
        all_sprites.add(new_missile)

    # Génération aléatoire des roquettes avec avertissements
    if random.randint(0, 100) < 1:
        rocket_y = random.randint(0, screen_height - 20)
        new_warning = RocketWarning(screen_width, rocket_y)
        rocket_warnings.add(new_warning)
        all_sprites.add(new_warning)
    elif random.randint(0, 100) < 1:
        rocket_y = random.randint(0, screen_height - 20)
        new_rocket = Rocket(screen_width, rocket_y, 5)
        rockets.add(new_rocket)
        all_sprites.add(new_rocket)

    # Vérification des collisions avec les missiles
    if pygame.sprite.spritecollide(player, missiles, False):
        player.electrocute()  # Déclencher l'animation d'électrocution si le joueur touche un missile

    # Vérification des collisions avec les roquettes
    if pygame.sprite.spritecollide(player, rockets, False):
        player.electrocute()  # Déclencher l'animation d'électrocution si le joueur touche une roquette

    # Changement du fond d'arrière-plan à intervalles réguliers
    background_change_timer += clock.get_rawtime()
    if background_change_timer >= background_change_interval:
        current_background_index = (current_background_index + 1) % len(background_images)
        background_image = pygame.image.load(background_images[current_background_index])
        background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
        background_change_timer = 0

    # Affichage
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()