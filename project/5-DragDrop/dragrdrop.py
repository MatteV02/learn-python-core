# Simple pygame program

# Import and initialize the pygame library
import pygame
import os

# Ottieni la posizione della cartella in cui sto lavorando
current_dir = os.path.dirname(os.path.abspath(__file__))
# Imposta la cartella da cui importare le risorse come la cartella attuale
os.chdir(current_dir)

pygame.init()

class Label(pygame.sprite.Sprite):
    def __init__(self, text, center):
        super(Label, self).__init__()
        self.image = pygame.image.load('label.png')
        self.rect = self.image.get_rect(center = center)
        self.center = center
        self.number = -1
        font = pygame.font.Font('PressStart2P-vaV7.ttf', 12)
        rendered_text = font.render(text, True, 'black')
        self.image.blit(rendered_text, (10, 10))
        self.text = text

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)

    def touches(self, destination):
        if self.rect.colliderect(destination.rect):
            self.number = destination.number
            dx = destination.rect.x - self.rect.x
            dy = destination.rect.y - self.rect.y
            self.center = destination.rect.center
            self.move(dx, dy)
            return True
        return False


class Destination(pygame.sprite.Sprite):
    def __init__(self, number, center):
        super(Destination, self).__init__()
        self.image = pygame.image.load('destination.png')
        self.rect = self.image.get_rect(center = center)
        self.number = number

# Set up the drawing window (500x500 pixels)
screen = pygame.display.set_mode((500, 500))

# Create a game clock (used for precise timing calculations)
clock = pygame.time.Clock()
FPS = 30 # set game FPS

levels = [
    {
        'destinations': 3,
        'labels': {
            'Ciao': 0,
            'come': 1,
            'stai?': 2
        }
    },
    {
        'destinations': 3,
        'labels': {
            'trova un\ntesoro': 2,
            'Chi trova': 0,
            'un amico': 1,
        }
    },
]

background = pygame.image.load('background.png')

for i, level in enumerate(levels):
    visible_sprites = pygame.sprite.Group()

    destinations = []
    for i in range(level['destinations']):
        destination_sprite = Destination(i, (500 / len(level['labels']) - 80 + i*150, 200))
        destinations.append(destination_sprite) # TODO determine destination position
        visible_sprites.add(destination_sprite)

    labels = []
    for i, label in enumerate(level['labels'].keys()):
        label_sprite = Label(label, (500 / len(level['labels']) - 80 + i*150, 400))
        labels.append(label_sprite)
        visible_sprites.add(label_sprite)


    mouse_pressed = False

    # Run until the user asks to quit
    running = True
    while running:
        # Process user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ## Se l'utente vuole chiudere la finestra
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
                is_every_label_placed = True
                for label in labels:
                    if label.number < 0:
                        is_every_label_placed = False
                        break
                if is_every_label_placed:
                    running = False

        if mouse_pressed:
            for label in labels:
                if label.rect.collidepoint(pygame.mouse.get_pos()):
                    pos = pygame.mouse.get_pos()
                    dx = pos[0] - label.rect.centerx
                    dy = pos[1] - label.rect.centery
                    label.move(dx, dy)
                    for destination in destinations:
                        label.touches(destination)

        # Display update
        screen.blit(background)

        visible_sprites.draw(screen)

        ## Update (flip) the display
        pygame.display.flip()

        clock.tick(FPS) # Stop the game loop until it is time to generate the next frame

    win = True
    # risultato del gioco
    for label in labels:
        if label.number != level['labels'][label.text]:
            win = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('white')

        if win:
            text = "You Have Won"
        else:
            text = "You Lost"

        font = pygame.font.Font('PressStart2P-vaV7.ttf', 12)
        rendered_text = font.render(text, True, 'black')

        screen.blit(rendered_text, (250, 250))

        pygame.display.flip()

        clock.tick(FPS)

# Done! Time to quit.
pygame.quit()