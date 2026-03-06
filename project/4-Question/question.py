# Per progettare un platformer correttamente hai bisogno di:
# - sfondo
# - piattaforme su cui il personaggio può appoggiarsi
# - ostacoli
# 
# solitamente ognuna di queste va in un file separato

import pygame
import os

pygame.init() # inizializzo pygame

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

# In questi gruppi memorizzo domande e possibili risposte che sono mostrati sulla schermata
displayed_questions = pygame.sprite.Group()
displayed_options = pygame.sprite.Group()

class Hero(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Hero, self).__init__()

        self.image = pygame.image.load('hero.png').convert_alpha()
        self.rect = self.image.get_rect(center = center)

class Examiner(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Examiner, self).__init__()

        self.image = pygame.image.load('examiner.png').convert_alpha()
        self.rect = self.image.get_rect(center = center)

        self.center = center

    def ask(self, question, options):
        # in questa funzione vengono generati gli sprite con le domande
        # question è un dizionario fatto in questo modo:
        #   {'text': testo della domanda, 'top_left': angolo in alto a sinistra}
        #
        question = Question(question['text'], question['top_left'])
        question.rect.move_ip(self.center[0]+10, self.center[1]-200)
        displayed_questions.add(question)
        for i, key in enumerate(options.keys()):
            option = Option(key, options[key])
            option.rect.move_ip(self.center[0]+60, self.center[1]-90 + i * option.rect.height)
            displayed_options.add(option)

class Question(pygame.sprite.Sprite):
    def __init__(self, text, top_left):
        super(Question, self).__init__()
        self.image = pygame.image.load('question.png').convert_alpha()
        self.rect = self.image.get_rect()
        
        self.text = text

        font = pygame.font.Font('PressStart2P-vaV7.ttf', 10)
        rendered_text = font.render(text, True, 'black')
        self.image.blit(rendered_text, top_left)

class Option(pygame.sprite.Sprite):
    def __init__(self, text, is_right):
        # is_right è una variabile booleana usata per controllare se la risposta data è corretta o meno
        super(Option, self).__init__()
        self.image = pygame.image.load('option.png').convert_alpha()
        self.rect = self.image.get_rect()

        font = pygame.font.Font('PressStart2P-vaV7.ttf', 10)
        rendered_text = font.render(text, True, 'black')
        self.image.blit(rendered_text, (30, 25))
        self.is_right = is_right

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos[0], mouse_pos[1])


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 30

# in questo punto definisco come sono fatti i livelli
# un livello è una domanda e una serie di opzioni marcate come corretta (True) o sbagliata (False)
levels = [
    {
        'question': {
            'text': 'Di che colore è il\ncavallo bianco\ndi Napoleone?',
            'top_left': (75,40),
        },
        'options': {
            'A. Nero': False,
            'B. Marrone': False,
            'C. Bianco': True,
            'D. Grigio': False
        }
    },
    {
        'question': {
            'text': '7 x 8 = ?',
            'top_left': (75,40)
        },
        'options': {
            'A. 4': False,
            'B. 42': False,
            'C. 71': False,
            'D. 56': True
        }
    }
]

# in questo gruppo memorizzo i personaggi statici
displayed_characters = pygame.sprite.Group()

hero = Hero((420, 350))
displayed_characters.add(hero)

examiner = Examiner((70, 325))
displayed_characters.add(examiner)

background = pygame.image.load('background.png')
font = pygame.font.Font('PressStart2P-vaV7.ttf', 20)

score = 0

for level in levels:
    running = True

    examiner.ask(level['question'], level['options'])

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                for option in displayed_options:
                    if option.is_clicked():
                        if option.is_right:
                            score += 1
                            running = False
                        else:
                            running = False

        screen.blit(background)

        score_label = font.render(f'SCORE: {score}/{len(levels)}', True, 'black')
        score_rect = score_label.get_rect(center=(250, 53))
        screen.blit(score_label, score_rect)
        
        displayed_characters.draw(screen)
        displayed_questions.draw(screen)
        displayed_options.draw(screen)

        pygame.display.flip()

        clock.tick(FPS)


# SECONDA SCHERMATA
# a seconda se ho vinto o perso nella schermata precedente carico lo sfondo corretto
background = None
if score >= 2: 
    background = pygame.image.load('background-win.png') 
else: 
    background = pygame.image.load('background-lose.png')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(background)
    displayed_characters.draw(screen)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
