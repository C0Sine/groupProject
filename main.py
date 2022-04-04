import pygame
import random
import sys

from pygame import QUIT

DISPLAY = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

tick = 0
linetick = 0
circleTick = 30
triangleTick = 0

class Player(pygame.sprite.Sprite):
    """Player Class: Creates player"""


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = pygame.image.load("boi.png")
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = [0, 0]
        self.currentChange = [0, 0]

    # method blit: blits player
    def blit(self):
        DISPLAY.blit(self.image, (self.pos[0], self.pos[1]))

    # method move: changes
    def move(self, newChange):
        self.currentChange = newChange

    # method update: blits player
    def update(self):
        self.pos[0] += self.currentChange[0]
        self.pos[1] += self.currentChange[1]







john=Player()

while True:
    for event in pygame.event.get():
        john.update()
        john.blit()
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                john.move([1,0])
            if event.key == pygame.K_s:
                john.move([-1,0])
            if event.key == pygame.K_a:
                john.move([0,-1])
            if event.key == pygame.K_d:
                john.move([0,1])

    pygame.display.update()
    fpsClock.tick(FPS)
