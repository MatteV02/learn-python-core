# Per progettare un platformer correttamente hai bisogno di:
# - sfondo
# - piattaforme su cui il personaggio può appoggiarsi
# - ostacoli
# 
# solitamente ognuna di queste va in un file separato

import pygame
import os

########### WORKING DIRECTORY SETUP #############

# Ottieni la posizione della cartella in cui sto lavorando
current_dir = os.path.dirname(os.path.abspath(__file__))
# Imposta la cartella da cui importare le risorse come la cartella attuale
os.chdir(current_dir)


########### GLOBAL VARIABLES AND CLASSES #############

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# maggiore è questo numero e maggiore sarà la forza di gravità nel gioco
GRAVITY = 10

class Hero(pygame.sprite.Sprite):
    def __init__(self, center, speed, platforms):
        super(Hero, self).__init__()

        self.spawn_point = center

        self.image = pygame.image.load('hero.png')
        self.rect = self.image.get_rect(center = center)

        self.speed = speed
        self.jump_speed = 0 # Questa variabile è utilizzata durante i salti
        self.platforms = platforms # in questo parametro memorizzo le piattaforme con le quali lo sprite può interagire

    def update(self):
        # Ottieni i pulsanti premuti dall'utente
        pressed_keys = pygame.key.get_pressed()
        
        # lista delle piattaforme che lo sprite sta toccando
        touching_platforms = pygame.sprite.spritecollide(self, self.platforms, False)

        if pressed_keys[pygame.K_UP]:
            # freccia verso l'alto premuta --> faccio un salto
            
            # 1. controllo che l'eroe sia a contatto con almeno una piattaforma
            if len(touching_platforms) > 0:
                # 2. posso fare il salto
                self.jump_speed = GRAVITY * 4 # puoi aumentare questo valore per fare salti più ampi
                self.rect.move_ip(0, - self.jump_speed)

        # applico la forza di gravità allo sprite se sono in volo
        if len(touching_platforms) == 0:
            self.rect.move_ip(0, GRAVITY - self.jump_speed)
            # se sto saltando, aggiorno la velocità di salto in base alla forza di gravità
            self.jump_speed -= GRAVITY
            if self.jump_speed < 0:
                self.jump_speed = 0
        
        if pressed_keys[pygame.K_LEFT]:
            # freccia verso sinistra --> movimento verso sinistra
            self.rect.move_ip(-self.speed, 0)
        
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

    def respawn(self):
        self.rect = self.image.get_rect(center = self.spawn_point)

class Platform(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Platform, self).__init__()

        self.image = pygame.image.load('platform.png')
        self.rect = self.image.get_rect(center = center)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 30

# in questo punto definisco come è fatto un livello
# un livello è l'insieme di sfondo, piattaforme e spawn_point (punto di partenza) dell'eroe
level = {
    'background': pygame.image.load('background.png'),
    'platforms': pygame.sprite.Group(
        Platform((70, 400)),
        Platform((225, 400)),
        Platform((400, 425)),
    ),
    'spawn_point': (70, 350)
}

hero = Hero(level['spawn_point'], 5, level['platforms'])

active_sprites = pygame.sprite.Group()
active_sprites.add(hero)
active_sprites.add(level['platforms'])


# PRIMA SCHERMATA
win = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    active_sprites.update()

    if hero.rect.bottom >= SCREEN_HEIGHT:
        # l'eroe ha toccato il fondo dello schermo --> respawna allo starting point
        hero.respawn()

    if hero.rect.right >= SCREEN_WIDTH:
        # l'eroe ha raggiunto il bordo destro dello schermo --> vittoria
        win = True
        running = False

    screen.blit(level['background'])
    active_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)


# SECONDA SCHERMATA
# a seconda se ho vinto o perso nella schermata precedente carico lo sfondo corretto
background = None
if win: 
    background = pygame.image.load('background-win.png') 
else: 
    background = pygame.image.load('background-lose.png')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
