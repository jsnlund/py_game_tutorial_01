
#https://coderslegacy.com/python/pygame-level-generation/

import pygame
from pygame.locals import *
from numpy import sign
import random

from sys import exit

pygame.init()
vec = pygame.math.Vector2 

HEIGHT = 450
WIDTH = 400
ACC = 0.5
GROUND_FRIC = -.12
AIR_FRIC = -.08
FPS = 60
GRAVITY = 0.5

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
  
        self.pos = vec((10, 300))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    

    def move(self):
        self.acc = vec(0,GRAVITY)
        self.hits = pygame.sprite.spritecollide(self , platforms, False)
   
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC    

        if self.hits and self.pos.y == self.hits[0].rect.top + 1:
            self.motion(FRIC=GROUND_FRIC)
        else:
            self.motion(FRIC=AIR_FRIC)


        if self.pos.x > WIDTH:
            self.pos.x = 0
            # self.vel.x = -1*self.vel.x
        if self.pos.x < 0:
            self.pos.x = WIDTH
            # self.vel.x = -1*self.vel.x

        if self.pos.y > HEIGHT:
            self.pos.y = 0
            
        self.rect.midbottom = self.pos

    def motion(self, FRIC):
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

    def jump(self):
        self.vel.y = -15

    def long_jump(self):
        if self.vel.x != 0:
            print(self.vel.x)
            self.vel = vec(sign(self.vel.x)*30, -10)

    def update(self):
        # hits = pygame.sprite.spritecollide(self , platforms, False)
        if self.vel.y > 0:        
            if self.hits or self.pos.y > HEIGHT:
                self.vel.y = 0
                self.pos.y = self.hits[0].rect.top + 1


class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = random.randint(50, 100)
        R = int((self.width%2) * 255)
        G = int((self.width%7)/6 * 255)
        B = int((self.width%13)/12 * 255)
        self.surf = pygame.Surface((self.width, 12))
        self.surf.fill((R,G,B))
        self.rect = self.surf.get_rect(center = (random.randint(0, WIDTH-10), random.randint(0, HEIGHT - 30)))

    def move(self):
        pass


def move_platforms(P1, platforms):
    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    while len(platforms) < 7 :
        p  = platform()             
        p.rect.center = (random.randrange(0, WIDTH - p.width),
                             random.randrange(-50, 0))
        platforms.add(p)
        all_sprites.add(p)
    return P1, platforms
    

def gen_platforms(all_sprites = pygame.sprite.Group(), platforms = pygame.sprite.Group()):

    for x in range(random.randint(5, 6)):
        pl = platform()
        platforms.add(pl)
        all_sprites.add(pl)

    return all_sprites, platforms

all_sprites, platforms = gen_platforms()

PT1 = platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

platforms.add(PT1)
all_sprites.add(PT1)


P1 = Player()

all_sprites.add(P1)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                P1.jump()
            if event.key == pygame.K_SPACE:
                P1.long_jump()
            # TODO: setup destroy old platforms prior to generating new ones.
            # if event.key == pygame.K_r:
            #     all_sprites, platforms = gen_platforms()
            #     platforms.add(PT1)
            #     all_sprites.add(PT1)
            #     all_sprites.add(P1)
    
    displaysurface.fill((0,0,0))
    P1.update()
    P1, platforms = move_platforms(P1, platforms)

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)