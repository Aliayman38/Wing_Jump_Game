import sys
import pygame
from pygame.locals import *
from sizee import *
import random

pygame.init()

# create by:
'''
ALI AYMAN QORA'AN 
'''

# GAME FPS
clock = pygame.time.Clock()
fps = 60

# create a game window and Title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WING JUMP")

# load images
background = pygame.image.load("background1.png")
background3 = pygame.image.load("background2.png")
moving_ground = pygame.image.load("ground.png")
losing_image = pygame.image.load('restart2.png')
start_image = pygame.image.load("startthegame.png")
heart_image = pygame.image.load("heart-removebg-preview2.png")

# load sounds
My_bird_sound = pygame.mixer.Sound("Flappy-Bird.wav")
scorevoice = pygame.mixer.Sound("scorevoice.wav")
dievoice = pygame.mixer.Sound("deadthebird.wav")

# my_font && coloer
FONT = pygame.font.SysFont('TrueType', 80)
WHITE = (255, 255, 255)

# game variables
ground_Animate = 0
Animate_speed = 3
starting = False
end_game = False
distance_between_pipe = 160
pipe_frequncy = 1300
last_pipe = pygame.time.get_ticks() - pipe_frequncy
score = 0
if_pipe_pase = False
sound_played = False
attempts = 3


def screen_text(string, font, string_color, x, y):
    if int(string) % 5 == 0 and int(string) != 0:
        string_color = (255, 0, 0)
    image = font.render(string, True, string_color)
    screen.blit(image, (x, y))


def reset_game():
    pipe_group.empty()
    My_bird.rect.x = 90
    My_bird.rect.y = HEIGHT // 2
    score = 0
    My_bird.Birdspeed = 0
    return score


def attemptss(attempts, x, y):
    for i in range(attempts):
        screen.blit(heart_image, (x + i * 40, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(1, 3):
            img = pygame.image.load(f'bird{i}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.Birdspeed = 0
        self.jump = False

    def update(self):
        # gravity
        if starting == True:
            self.Birdspeed += 0.4
            if self.Birdspeed > 8:
                self.Birdspeed = 8
            if self.rect.bottom < 500:
                self.rect.y += self.Birdspeed
        if end_game == False:
            # how to jump
            if self.jump:
                self.Birdspeed -= 10
                self.jump = False

            # handel the animation
            self.counter += 1
            cooldown = 13
            if self.counter > cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.Birdspeed * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect()
        # position 1 from the top , -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - distance_between_pipe)
        if position == -1:
            self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= Animate_speed
        if self.rect.right < 0:
            self.kill()


class losing():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        global sound_played
        action = False
        # mouse
        pos = pygame.mouse.get_pos()

        # check mouse
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
                sound_played = False
        # draw loseing image
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
My_bird = Bird(90, HEIGHT // 2)
bird_group.add(My_bird)

# create a restart button
button = losing(WIDTH // 2 - 75, HEIGHT // 2 - 72, losing_image)

while True:
    clock.tick(fps)

    # draw background
    if score < 15:
        screen.blit(background, (0, 0))
    elif score >= 15 and score < 30:
        screen.blit(background3, (0, 0))
    elif score >= 45 and score < 60:
        screen.blit(background3, (0, 0))
    else:
        screen.blit(background, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # draw ground
    screen.blit(moving_ground, (ground_Animate, 500))

    if starting == False and end_game == False:
        screen.blit(start_image, (WIDTH // 2 - 110, HEIGHT // 2 - 175))

    # score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and if_pipe_pase == False:
            if_pipe_pase = True
        if if_pipe_pase == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                scorevoice.play()
                if_pipe_pase = False

    screen_text(str(score), FONT, WHITE, WIDTH // 2, 30)
    # lives
    attemptss(attempts, 10, 10)

    # if bird touch the pipes
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or My_bird.rect.top < 0:
        attempts -= 1
        if not sound_played:
            dievoice.play()
            sound_played = True

        if attempts > 0:
            My_bird.rect.x = 90
            My_bird.rect.y = HEIGHT // 2
            My_bird.Birdspeed = 0
            pipe_group.empty()
            sound_played = False
            if_pipe_pase = False
        else:
            end_game = True

    # end the game if bird hit the ground
    if My_bird.rect.bottom > 500:
        if not sound_played:
            dievoice.play()
            sound_played = True
        attempts -= 1
        if attempts > 0:
            My_bird.rect.x = 90
            My_bird.rect.y = HEIGHT // 2
            My_bird.Birdspeed = 0
            pipe_group.empty()
            sound_played = False
            if_pipe_pase = False
        else:
            end_game = True
            starting = False

    if end_game == False and starting == True:
        # new pipes
        time = pygame.time.get_ticks()
        if time - last_pipe > pipe_frequncy:
            the_randodvalue = random.randint(-90, 90)
            My_pipe_btom = pipe(WIDTH, HEIGHT // 2 + the_randodvalue, -1)
            My_pipe_UP = pipe(WIDTH, HEIGHT // 2 + the_randodvalue, 1)
            pipe_group.add(My_pipe_btom)
            pipe_group.add(My_pipe_UP)
            last_pipe = time

        # animation the ground
        ground_Animate -= Animate_speed
        if abs(ground_Animate) > 30:
            ground_Animate = 0
        pipe_group.update()

    # check if game end
    if end_game == True:
        if button.draw() == True:
            end_game = False
            attempts = 3
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and starting:
                My_bird.jump = True
                My_bird_sound.play()
        if event.type == pygame.MOUSEBUTTONDOWN and starting == False and end_game == False:
            starting = True

    pygame.display.update()

