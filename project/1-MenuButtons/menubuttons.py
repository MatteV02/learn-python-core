import pygame
import os

########### WORKING DIRECTORY SETUP #############

# Ottieni la posizione della cartella in cui sto lavorando
current_dir = os.path.dirname(os.path.abspath(__file__))
# Imposta la cartella da cui importare le risorse come la cartella attuale
os.chdir(current_dir)


############ SPRITES ###############

class Button(pygame.sprite.Sprite):
    """
    La classe può essere configurata con un centro
    """
    def __init__(self, center, text = ''):
        super(Button, self).__init__()

        # Faccio il rendering dell'etichetta del bottone
        font = pygame.font.Font('PressStart2P-vaV7.ttf', 22)
        text_rendered = font.render(text, True, 'white')

        # importo l'immagine del bottone
        self.image = pygame.image.load('button.png').convert_alpha()

        # scrivo al centro dell'immagine la scritta
        self.image.blit(text_rendered, text_rendered.get_rect(center = self.image.get_rect().center))

        # imposto il rettangolo dello sprite
        self.rect = self.image.get_rect(center=center)

    def is_clicked(self, point):
        return self.rect.collidepoint(point)


############## GAME SETUP ###############

pygame.init()
screen = pygame.display.set_mode((750, 409)) # stessa dimensione dell'immagine di sfondo (puoi controllarla su Piskel)

# Imposto un frame rate di 30 FPS
clock = pygame.time.Clock()
FPS = 30

# Creo gli sprite e gli aggiungo ad un gruppo
button_start = Button((150, 230), 'Start')
button_quit = Button((150, 300), 'Exit')

menu_sprites = pygame.sprite.Group()
menu_sprites.add(button_start)
menu_sprites.add(button_quit)

# Carico lo sfondo
background = pygame.image.load('background.png').convert_alpha()

# Carico il font per le scritte nel gioco
font = pygame.font.Font('PressStart2P-vaV7.ttf', 30)


############## GAME LOOP ###############
running = True
started = False # variabile che avvia il gioco dopo il menu iniziale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Lascio all'utente chiudere la finestra normalmente
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if button_start.is_clicked(event.pos):
                started = True
                pass
            if button_quit.is_clicked(event.pos):
                running = False

    # Disegna lo sfondo
    screen.blit(background)

    if not started:
        # Disegna gli sprites del menu
        menu_sprites.draw(screen)
    else:
        # Disegna una scritta per segnalare che il gioco è partito
        game_started_render = font.render('Game started', True, 'white')
        screen.blit(game_started_render, game_started_render.get_rect(center = (375, 300)))

    # Aggiorna il display
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
