import pygame
from pygame.locals import *
import random

white = (255, 255, 255)
black = (0, 0, 0)
salmon = (250, 128, 114)
red = (255, 0, 0)
blue = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.init()

pygame.font.init()

class Snake(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.body = []
        self.block_size = 20
        self.length = 4
        bs = self.block_size
        for i in range(self.length):
            self.body.append((SCREEN_WIDTH / 2 + i * bs, SCREEN_HEIGHT / 2))
        self.direction = (bs, 0)
        self.eat_food = False

    def die(self):
        n = len(self.body)
        loc = self.body[n - 1]
        bs = self.block_size
        if loc[0] < 0 or loc[0] > SCREEN_WIDTH - bs or loc[1] < 0 or loc[1] > SCREEN_HEIGHT - bs:
            return True
        elif loc in self.body[ : n - 1]:
            return True
        return False

    def turn(self, pressed_keys):
        bs = self.block_size
        if pressed_keys[K_UP] and self.direction != (0, bs):
            self.direction = (0, -bs)
        if pressed_keys[K_DOWN] and self.direction != (0, -bs):
            self.direction = (0, bs)
        if pressed_keys[K_LEFT] and self.direction != (bs, 0):
            self.direction = (-bs, 0)
        if pressed_keys[K_RIGHT] and self.direction != (-bs, 0):
            self.direction = (bs, 0)

    def update(self):
        if self.eat_food == False:
            self.body.pop(0)
        else:
            self.eat_food = False
            self.length += 1
        old_head = self.body[-1]
        dr = self.direction
        self.body.append((old_head[0] + dr[0], old_head[1] + dr[1]))

class Food(pygame.sprite.Sprite):
    
    def __init__(self, bs):
        super().__init__()
        self.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.range = (int(SCREEN_WIDTH / 2) // bs, int(SCREEN_HEIGHT / 2) // bs)
        self.block_size = bs
        c = self.center
        r = self.range
        self.loc = (c[0] + random.randint(-r[0]+ 1, r[0] - 2) * bs, c[1] + random.randint(-r[1] + 1, r[1] - 2) * bs)

    def update(self):
        c = self.center
        r = self.range
        bs = self.block_size
        self.loc = (c[0] + random.randint(-r[0]+ 1, r[0] - 2) * bs, c[1] + random.randint(-r[1] + 1, r[1] - 2) * bs)

def game_loop():

    clock = pygame.time.Clock()

    running = True

    playing = True

    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                else:
                    playing = True
                break
        
        snake = Snake()
        bs = snake.block_size
        food = Food(bs)
        surf = pygame.Surface((bs, bs))

        try:
            pygame.mixer.music.load("Play.mp3")
            die_sound = pygame.mixer.Sound("Die.mp3")
        except:
            try:
                pygame.mixer.music.load("Snake_demo/Play.mp3")
                die_sound = pygame.mixer.Sound("Snake_demo/Die.mp3")
            except:
                pygame.mixer.music.load("/Users/zephyr/Desktop/CS/SE/Snake_demo/Play.mp3")
                die_sound = pygame.mixer.Sound("/Users/zephyr/Desktop/CS/SE/Snake_demo/Die.mp3")

        die_sound.stop()
        pygame.mixer.music.play(loops = -1)
        

        while playing:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        playing = False
                        running = False
                    else:
                        pressed_keys = pygame.key.get_pressed()
                        snake.turn(pressed_keys)

            if food.loc in snake.body:
                snake.eat_food = True
                food.update()

            snake.update()

            if snake.die():
                playing = False
                pygame.mixer.music.pause()
                die_sound.play()

                clock.tick(1)
                screen.fill(black)
                font = pygame.font.Font("freesansbold.ttf", 32)
                text = font.render("Game Over", False, red)
                textRect = text.get_rect()
                textRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                screen.blit(text, textRect)
                pygame.display.update()

                clock.tick(0.5)
                screen.fill(black)
                text1 = font.render("Press Esc to exit", False, red)
                text2 = font.render("Press any other key to continue", False, red)
                textRect1 = text1.get_rect()
                textRect2 = text2.get_rect()
                d = 20
                textRect1.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - d)
                textRect2.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + d)
                screen.blit(text1, textRect1)
                screen.blit(text2, textRect2)
                pygame.display.update()

                clock.tick(0.5)
                playing = False
            
            else:

                screen.fill(white)

                surf.fill(red)
                for loc in snake.body:
                    screen.blit(surf, loc)

                surf.fill(black)
                screen.blit(surf, food.loc)

                caption = "Score: " + str(snake.length - 4)
                pygame.display.set_caption(caption)

                pygame.display.update()

                clock.tick(24 - 56 / snake.length) # number of frames

    pygame.quit()
    quit()

game_loop()