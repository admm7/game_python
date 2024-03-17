import pygame
import sys
import random
import time
import menu as menu
from player import Player 
from laser import Laser
from missile import Missile
from coin import Coin
from rocket_warning import RocketWarning
from rocket import Rocket



pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jetpack Joyride")

BACKGROUND_IMAGES = ["image/back.jpg", "image/galaxyy.png"]
CURRENT_BACKGROUND_INDEX = 0
BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGES[CURRENT_BACKGROUND_INDEX])
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND_X = 0  # Horizontal position of the background image

MUSIC_1 = "sound/gg.mp3"
MUSIC_2 = "sound/space_sound.mp3"

BACKGROUND_MUSIC = {
    "image/back.jpg": MUSIC_1,
    "image/galaxyy.png": MUSIC_2
}

def play_background_music():
    current_background = BACKGROUND_IMAGES[CURRENT_BACKGROUND_INDEX]
    music_file = BACKGROUND_MUSIC.get(current_background)
    if music_file:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

CHARACTER1 = pygame.image.load("image/charachter1.png")
CHARACTER1 = pygame.transform.scale(CHARACTER1, (100, 100))
CHARACTER2 = pygame.image.load("image/charachter2.png")
CHARACTER2 = pygame.transform.scale(CHARACTER2, (100, 100))
CHARACTER3 = pygame.image.load("image/charachter3.png")
CHARACTER3 = pygame.transform.scale(CHARACTER3, (100, 100))
PLAYER_IMAGE = pygame.image.load("image/transformation.png")
PLAYER_IMAGE = pygame.transform.scale(PLAYER_IMAGE, (100, 100))
MISSILE_IMAGE = pygame.image.load("image/missile2.png")
MISSILE_IMAGE = pygame.transform.scale(MISSILE_IMAGE, (30, 15))
ROCKET_WARNING_IMAGE = pygame.image.load("image/avert.png")
ROCKET_WARNING_IMAGE = pygame.transform.scale(ROCKET_WARNING_IMAGE, (30, 30))
ROCKET_IMAGE = pygame.image.load("image/rocket.png")
ROCKET_IMAGE = pygame.transform.scale(ROCKET_IMAGE, (50, 20))
LASER_IMAGE = pygame.image.load("image/zap.png")
LASER_IMAGE = pygame.transform.scale(LASER_IMAGE, (50, 120))
ELECTROCUTED_IMAGE = pygame.image.load("image/electrocuted.png")
ELECTROCUTED_IMAGE = pygame.transform.scale(ELECTROCUTED_IMAGE, (80, 80))
PLAYER_AFTER_ELECTROCUTED = pygame.image.load("image/charachter1.png")
PLAYER_AFTER_ELECTROCUTED = pygame.transform.scale(PLAYER_AFTER_ELECTROCUTED, (80, 80))
SHIP_IMAGE = pygame.image.load("image/ufo2.png")
SHIP_IMAGE = pygame.transform.scale(SHIP_IMAGE, (80, 80))

LASER_SOUND = pygame.mixer.Sound("sound/laser_sound.mp3")
COIN_SOUND = pygame.mixer.Sound("sound/coin_sound.wav")
MISSILE_SOUND = pygame.mixer.Sound("sound/explosion.mp3")

COIN_IMAGE_PATH = "image/coineeee.png"
COIN_IMAGE = pygame.image.load(COIN_IMAGE_PATH).convert_alpha()
COIN_IMAGE = pygame.transform.scale(COIN_IMAGE, (60, 60))

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

# Classe pour les missiles
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = MISSILE_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x += self.speed  # Les missiles se déplacent vers l'avant
        if self.rect.right <= 0 or self.rect.left >= SCREEN_WIDTH:
            self.kill()

# Classe pour les roquettes
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = ROCKET_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()
    

# Classe pour les avertissements de roquettes
class RocketWarning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = ROCKET_WARNING_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        


    def update(self):
         # Check for collisions between RocketWarning and missiles
        missile_collisions = pygame.sprite.spritecollide(self, missiles, True)
        if missile_collisions:
            self.kill()  # Remove the RocketWarning sprite if it collides with a missile

# Classe pour les lasers
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = LASER_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right <= 0:
            self.kill()

# Classe pour les pièces
import math

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = COIN_IMAGE
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.initial_y = y  # Store the initial y-position
        self.speed = speed
        self.angle = 0  # Initialize angle for wave motion

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

 
# Classe pour les vaisseaux
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.original_image = SHIP_IMAGE
        self.image = pygame.transform.scale(self.original_image, (120, 120))  # Redimensionner l'image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = speed
        self.attack_cooldown = 0
        self.direction = 1

    def update(self):
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





# Classe pour les missiles des vaisseaux
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

clock = pygame.time.Clock()


# Groupe de missiles
missiles = pygame.sprite.Group()

# Groupe de vaisseaux
ships = pygame.sprite.Group()


# Groupe de missiles des vaisseaux ennemis
enemy_missiles = pygame.sprite.Group()

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

# Groupe de lasers
lasers = pygame.sprite.Group()

# Groupe de pièces
coins = pygame.sprite.Group()

clock = pygame.time.Clock()

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
    global BACKGROUND_IMAGE, CURRENT_BACKGROUND_INDEX
    CURRENT_BACKGROUND_INDEX = (CURRENT_BACKGROUND_INDEX + 1) % len(BACKGROUND_IMAGES)
    BACKGROUND_IMAGE = pygame.image.load(BACKGROUND_IMAGES[CURRENT_BACKGROUND_INDEX])
    BACKGROUND_IMAGE= pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Boucle principale
running = True
menu_start = True
clock_tick_rate = 120
game_over = False

# Fonction pour charger et jouer la musique correspondant au fond d'écran actuel
# Déclaration des musiques de fond correspondant à chaque fond d'écran


while running:
    if menu_start: 
        menu_start = menu.menu_1()
        play_background_music()
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000  # Convertit le temps en secondes
    # Fonction pour charger et jouer la musique correspondant au fond d'écran actuel

     # Augmenter le taux de rafraîchissement après 10 secondes de jeu
    if elapsed_time >= 10:
        clock_tick_rate = 180

    clock.tick(clock_tick_rate) 
    
    
    
  
    
    pygame.mixer.music.play(-1)  # -1 pour jouer en boucle

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
        for _ in range(4):
            new_ship = Ship(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 20), random.randint(2, 4))
            ships.add(new_ship)
            all_sprites.add(new_ship)

        

    # Détection de collision entre le joueur et les vaisseaux
    
    for ship in ships:
        if pygame.sprite.collide_rect(player, ship):
            player.electrocute()  # Déclencher l'animation d'électrocution
            player.rect.centerx = 100  # Réinitialiser la position horizontale du joueur
            player.rect.centery = SCREEN_HEIGHT// 2  # Réinitialiser la position verticale du joueur
            ship.kill()  # Supprimer le vaisseau après la collision
            game_over = True  # Définir l'état du jeu sur "game over"
            
    # Détection de collision entre le joueur et les roquettes
    for rocket in rockets:
        if pygame.sprite.collide_rect(player, rocket):
            player.electrocute()  # Déclencher l'animation d'électrocution
            player.rect.centerx = 100  # Réinitialiser la position horizontale du joueur
            player.rect.centery = SCREEN_HEIGHT // 2  # Réinitialiser la position verticale du joueur
            rocket.kill()  # Supprimer la roquette après la collision
            game_over = True  # Définir l'état du jeu sur "game over"


    # Génération aléatoire des missiles
    if random.randint(0, 100) < 1:
        new_missile = Missile(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT- 10), 3)
        missiles.add(new_missile)
        all_sprites.add(new_missile)

    # Détection de collision entre les missiles du joueur et les vaisseaux
    for missile in missiles:
        ship_hit_list = pygame.sprite.spritecollide(missile, ships, True)
        for ship in ship_hit_list:
            missile.kill()
            player.score += 1

   

    # Détection de collision entre les missiles ennemis et le joueur
    for missile in enemy_missiles:
        if pygame.sprite.collide_rect(player, missile):
            player.electrocute()  # Déclencher l'animation d'électrocution
            player.rect.centerx = 100  # Réinitialiser la position horizontale du joueur
            player.rect.centery = SCREEN_HEIGHT // 2  # Réinitialiser la position verticale du joueur
            missile.kill()  # Supprimer le missile après la collision
            LASER_SOUND.play()  # Jouer le son du laser

    
    

    # Génération aléatoire des missiles
    if random.randint(0, 200) < 1:
        new_missile = Missile(SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - 10), 3)
        missiles.add(new_missile)
        all_sprites.add(new_missile)

    # Génération aléatoire des roquettes avec avertissements
    if random.randint(0, 200) < 1:
        rocket_y = random.randint(0, SCREEN_HEIGHT - 20)
        new_warning = RocketWarning(SCREEN_WIDTH, rocket_y)
        rocket_warnings.add(new_warning)
        all_sprites.add(new_warning)
    elif random.randint(0, 200) < 1:
        rocket_y = random.randint(0, SCREEN_HEIGHT - 20)
        new_rocket = Rocket(SCREEN_WIDTH, rocket_y, 5)
        rockets.add(new_rocket)
        all_sprites.add(new_rocket)

    # Génération aléatoire des lasers
    if random.randint(0, 200) < 1:
        laser_y = random.randint(0, SCREEN_HEIGHT- 80)  # Assurez-vous que le laser reste dans les limites de l'écran
        new_laser = Laser(SCREEN_WIDTH, laser_y, 5)  # Vitesse de déplacement des lasers
        lasers.add(new_laser)
        all_sprites.add(new_laser)

    # Génération aléatoire des pièces
    if random.randint(0, 300) < 1:
        coin_y = random.randint(50, SCREEN_HEIGHT - 50)
        new_coin = Coin(SCREEN_WIDTH, coin_y, 5)
        coins.add(new_coin)
        all_sprites.add(new_coin)

    # Détection de collision entre le joueur et le laser
    for laser in lasers:
        if pygame.sprite.collide_rect(player, laser):
            player.electrocute()  # Déclencher l'animation d'électrocution
            player.rect.centerx = 100  # Réinitialiser la position horizontale du joueur
            player.rect.centery = SCREEN_HEIGHT // 2  # Réinitialiser la position verticale du joueur
            LASER_SOUND.play()  # Jouer le son du laser

    # Détection de collision entre le joueur et les pièces
    for coin in coins:
        if pygame.sprite.collide_rect(player, coin):
            coin.collect()  # Appeler la méthode collect() de la pièce
            player.collect_coin()  # Appeler la méthode collect_coin() du joueur
            coin.kill()  # Supprimer la pièce après la collecte
            
    

    # Affichage
    BACKGROUND_X-= 1  # Déplacement horizontal des fonds d'écran
    if BACKGROUND_X <= -SCREEN_WIDTH:
        BACKGROUND_X = 0

    SCREEN.blit(BACKGROUND_IMAGE, (BACKGROUND_X, 0))
    SCREEN.blit(BACKGROUND_IMAGE, (BACKGROUND_X + SCREEN_WIDTH, 0))
   

    all_sprites.draw(SCREEN)

    # Affichage du score en haut de l'écran
    score_text = font.render("Score: " + str(player.score), True, (255, 255, 255))
    SCREEN.blit(score_text, (20, 20))
    
    


    # Affichage du temps écoulé en haut de l'écran
    time_text = font.render("Time: " + "{:.2f}".format(elapsed_time), True, (255, 255, 255))
    SCREEN.blit(time_text, (SCREEN_WIDTH - 150, 20))
    
     # Vérifier si le jeu est terminé
    if game_over:
        # Afficher un message de fin de jeu
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        SCREEN.blit(game_over_text, (SCREEN_WIDTH// 2 - 100, SCREEN_HEIGHT // 2))

        
    
        
        running = False
        
        
    
    

    pygame.display.flip()


# Quitter Pygame
pygame.quit()
sys.exit()








 
