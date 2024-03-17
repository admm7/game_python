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
from ship import Ship
from ennemy_missile import EnemyMissile




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

ROCKET_WARNING_IMAGE = pygame.image.load("image/avert.png")
ROCKET_WARNING_IMAGE = pygame.transform.scale(ROCKET_WARNING_IMAGE, (30, 30))
ROCKET_IMAGE = pygame.image.load("image/rocket.png")
ROCKET_IMAGE = pygame.transform.scale(ROCKET_IMAGE, (50, 20))

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

clock = pygame.time.Clock()


# Groupe de missiles
missiles = pygame.sprite.Group()

# Groupe de vaisseaux
ships = pygame.sprite.Group()


# Groupe de missiles des vaisseaux ennemis
enemy_missiles = pygame.sprite.Group()

# Groupe de sprites
all_sprites = pygame.sprite.Group()
player = Player(CHARACTER3, ELECTROCUTED_IMAGE, PLAYER_AFTER_ELECTROCUTED, SCREEN_HEIGHT)
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
    all_sprites.update(Missile, missiles, all_sprites, MISSILE_SOUND)

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








 
