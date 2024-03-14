
import pygame
import sys
import random
import time
import flyjetback as menu

# Initialisation de Pygame
pygame.init()

# Paramètres de l'écran
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jetpack Joyride")

# Chargement des images de fond
background_images = ["back.jpg", "space_back.png", "universe.jpg","galaxyy.png"]
current_background_index = 0
background_image = pygame.image.load(background_images[current_background_index])
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
background_x = 0  # Position horizontale du fond d'écran

# Chargement des images des sprites
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (150, 150))
missile_image = pygame.image.load("missile2.png")
missile_image = pygame.transform.scale(missile_image, (30, 15))
rocket_warning_image = pygame.image.load("avert.png")
rocket_warning_image = pygame.transform.scale(rocket_warning_image, (30, 30))
rocket_image = pygame.image.load("rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (50, 20))
laser_image = pygame.image.load("zap.png")
laser_image2 = pygame.image.load("zap2.png")
laser_image = pygame.transform.scale(laser_image, (40, 200))  # Redimensionner si nécessaire
laser_image2 = pygame.transform.scale(laser_image2, (40, 120))
electrocuted_image = pygame.image.load("electrocuted.png")
electrocuted_image = pygame.transform.scale(electrocuted_image, (80, 80))  # Redimensionner si nécessaire
ship_image = pygame.image.load("spaceship10.png")
ship_image = pygame.transform.scale(ship_image, (60, 30))
meteorite_image = pygame.image.load("meteor.png")
meteorite_image = pygame.transform.scale(meteorite_image, (30, 30))

# Chargement des effets sonores
laser_sound = pygame.mixer.Sound("laser_sound.mp3")
coin_sound = pygame.mixer.Sound("coin_sound.wav")
missile_sound = pygame.mixer.Sound("explosion.mp3")

# Chargement de l'image pour les pièces
coin_image_path = "coineeee.png"
coin_image = pygame.image.load(coin_image_path).convert_alpha()
coin_image = pygame.transform.scale(coin_image, (60, 60))  # Redimensionner l'image des pièces

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
        self.velocity_y = 0  # Ajout de la vitesse verticale du joueur

    def update(self):
        if not self.electrocuted:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.rect.y -= 5
            elif keys[pygame.K_z] and self.attack_cooldown <= 0:
                self.attack_cooldown = 30
                new_missile = Missile(self.rect.centerx, self.rect.centery, 5)  # Les missiles sont tirés vers l'avant
                missiles.add(new_missile)
                all_sprites.add(new_missile)
                missile_sound.play()  # Jouer le son du missile
            elif keys[pygame.K_DOWN] and self.attack_cooldown <= 0:
                self.attack_cooldown = 30
                new_missile = Missile(self.rect.centerx, self.rect.bottom, 5)  # Les missiles sont tirés vers le bas
                missiles.add(new_missile)
                all_sprites.add(new_missile)
                missile_sound.play()  # Jouer le son du missile
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
                self.image = player_image

        # Ajout des vérifications pour empêcher le joueur de sortir de l'écran verticalement
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.velocity_y = 0
        elif self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

    # Méthode pour déclencher l'animation d'électrocution
    def electrocute(self):
        if not self.electrocuted:
            self.electrocuted = True
            self.electrocuted_start_time = time.time()
            self.image = electrocuted_image  # Afficher l'image d'électrocution

    # Méthode pour incrémenter le score lors de la collecte de pièces
    def collect_coin(self):
        self.score += 1

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
        self.rect.x += self.speed  # Les missiles se déplacent vers l'avant
        if self.rect.right <= 0 or self.rect.left >= screen_width:
            self.kill()

# Classe pour les vaisseaux
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.original_image = ship_image
        self.image = pygame.transform.scale(self.original_image, (90, 45))  # Redimensionner l'image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed
        self.attack_cooldown = 0

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
        self.attack_cooldown -= 1
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 100
            new_missile = EnemyMissile(self.rect.centerx, self.rect.centery, -5)
            enemy_missiles.add(new_missile)
            all_sprites.add(new_missile)

# Classe pour les météorites
class Meteorite(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.original_image = meteorite_image
        self.image = pygame.transform.scale(self.original_image, (45, 45))  # Redimensionner l'image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()

# Classe pour les missiles des vaisseaux
class EnemyMissile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x += self.speed  # Les missiles se déplacent vers l'arrière
        if self.rect.right <= 0 or self.rect.left >= screen_width:
            self.kill()

clock = pygame.time.Clock()

# Groupe de sprites
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Groupe de missiles
missiles = pygame.sprite.Group()

# Groupe de vaisseaux
ships = pygame.sprite.Group()

# Groupe de météorites
meteorites = pygame.sprite.Group()

# Groupe de missiles des vaisseaux ennemis
enemy_missiles = pygame.sprite.Group()

# Timer pour changer le fond d'arrière-plan
background_change_timer = 0
background_change_interval = 10000  # Changement de fond toutes les 10 secondes

# Variable pour stocker la position horizontale précédente du joueur
previous_player_x = 100

# Police de caractères pour le texte
font = pygame.font.Font(None, 36)

# Début du jeu
start_time = pygame.time.get_ticks()

# Arrêter la musique du menu
pygame.mixer.music.stop()

# Fonction pour changer le fond d'écran après 10 secondes
def change_background_after_delay():
    global background_image, current_background_index
    current_background_index = (current_background_index + 1) % len(background_images)
    background_image = pygame.image.load(background_images[current_background_index])
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Boucle principale
running = True
menu_start = True
while running:
    if menu_start: 
        menu_start = menu.menu_1(menu_start)
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # Convertit le temps en secondes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Mise à jour des sprites
    all_sprites.update()

    # Si 10 secondes se sont écoulées, changez le fond
    if elapsed_time >= 10:
        change_background_after_delay()
        start_time = current_time  # Réinitialise le temps de départ

        # Génération aléatoire des vaisseaux
        for _ in range(3):
            new_ship = Ship(screen_width, random.randint(0, screen_height - 20), random.randint(2, 4))
            ships.add(new_ship)
            all_sprites.add(new_ship)

        # Génération aléatoire des météorites
        for _ in range(3):
            new_meteorite = Meteorite(screen_width, random.randint(0, screen_height - 20), random.randint(2, 4))
            meteorites.add(new_meteorite)
            all_sprites.add(new_meteorite)

    # Génération aléatoire des missiles
    if random.randint(0, 200) < 1:
        new_missile = Missile(screen_width, random.randint(0, screen_height - 10), 3)
        missiles.add(new_missile)
        all_sprites.add(new_missile)

    # Détection de collision entre les missiles du joueur et les vaisseaux
    for missile in missiles:
        ship_hit_list = pygame.sprite.spritecollide(missile, ships, True)
        for ship in ship_hit_list:
            missile.kill()
            player.score += 1

    # Détection de collision entre les missiles du joueur et les météorites
    for missile in missiles:
        meteorite_hit_list = pygame.sprite.spritecollide(missile, meteorites, True)
        for meteorite in meteorite_hit_list:
            missile.kill()
            player.score += 1

    # Détection de collision entre les missiles ennemis et le joueur
    for missile in enemy_missiles:
        if pygame.sprite.collide_rect(player, missile):
            player.electrocute()  # Déclencher l'animation d'électrocution
            player.rect.centerx = 100  # Réinitialiser la position horizontale du joueur
            player.rect.centery = screen_height // 2  # Réinitialiser la position verticale du joueur
            missile.kill()  # Supprimer le missile après la collision
            laser_sound.play()  # Jouer le son du laser

    # Affichage
    background_x -= 1  # Déplacement horizontal des fonds d'écran
    if background_x <= -screen_width:
        background_x = 0

    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + screen_width, 0))

    all_sprites.draw(screen)

    # Affichage du score en haut de l'écran
    score_text = font.render("Score: " + str(player.score), True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Affichage du temps écoulé en haut de l'écran
    time_text = font.render("Time: " + "{:.2f}".format(elapsed_time), True, (255, 255, 255))
    screen.blit(time_text, (screen_width - 150, 20))

    pygame.display.flip()

    clock.tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()