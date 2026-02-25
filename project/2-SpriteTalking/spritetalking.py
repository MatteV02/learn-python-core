import pygame
import os

########### WORKING DIRECTORY SETUP #############

# Ottieni la posizione della cartella in cui sto lavorando
current_dir = os.path.dirname(os.path.abspath(__file__))
# Imposta la cartella da cui importare le risorse come la cartella attuale
os.chdir(current_dir)


############ SPRITES ###############

class Dialogue(pygame.sprite.Sprite):
    def __init__(self, center, text):
        super(Dialogue, self).__init__()

        font = pygame.font.Font('PressStart2P-vaV7.ttf', 18)
        text_rendered = font.render(text, True, 'black')

        self.image = pygame.image.load('dialogue.png').convert_alpha()
        self.image.blit(text_rendered, text_rendered.get_rect(center = (80, 29)))

        self.rect = self.image.get_rect(center = center)

class TalkingSprite(pygame.sprite.Sprite):
    def __init__(self, center):
        super(TalkingSprite, self).__init__()

        self.center = center
        self.dialogue = None

        # importo l'immagine dello sprite
        self.image = pygame.image.load('sprite.png').convert_alpha()

        # imposto il rettangolo dello sprite
        self.rect = self.image.get_rect(center=center)

    def talk(self, text, group):
        # Creo uno sprite contenente il dialogo e lo aggiungo al gruppo specificato
        if self.dialogue is None:
            # crea il dialogo solo se non ce n'è già uno presente
            dialogue_center = (self.center[0] + 45, self.center[1] - 110)
            self.dialogue = Dialogue(dialogue_center, text)
            group.add(self.dialogue)

    def stop_talking(self, group):
        # rimuovo il dialogo dal gruppo specificato
        if self.dialogue is not None:
            # rimuovi il dialogo solo se ce n'è uno presente
            group.remove(self.dialogue)
            self.dialogue = None


############## GAME SETUP ###############

pygame.init()
screen = pygame.display.set_mode((500, 500)) # stessa dimensione dell'immagine di sfondo (puoi controllarla su Piskel)

# Imposto un frame rate di 30 FPS
clock = pygame.time.Clock()
FPS = 30

# Creo uno sprite e lo aggiungo al gruppo degli sprite stampati su schermo

talking_sprite = TalkingSprite((250, 225))

all_sprites = pygame.sprite.Group()
all_sprites.add(talking_sprite)

# Carico lo sfondo
background = pygame.image.load('background.png').convert_alpha()

# Carico il font per le scritte
font = pygame.font.Font('PressStart2P-vaV7.ttf', 15)

############## GAME LOOP ###############
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Lascio all'utente chiudere la finestra normalmente
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e:
                # se viene premuto il tasto e lo sprite parla
                talking_sprite.talk("Hello\nthere!", all_sprites)
            if event.key == pygame.K_q:
                # lo sprite smette di parlare
                talking_sprite.stop_talking(all_sprites)

    # Disegna lo sfondo
    screen.blit(background)

    # Stampo le indicazioni a schermo
    press_e_text = font.render('Press E to talk', True, 'white')
    press_q_text = font.render('Press Q to stop talking', True, 'white')
    screen.blit(press_e_text, press_e_text.get_rect(topleft = (10, 450)))
    screen.blit(press_q_text, press_q_text.get_rect(topleft = (10, 470)))

    # Disegna gli sprites del menu
    all_sprites.draw(screen)

    # Aggiorna il display
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
